"""
HeatingAnalyzer — Analyse économique des réseaux de chaleur urbains (RCU).
Calcule rentabilité, efficacité énergétique, comparaisons et projections.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error


class HeatingAnalyzer:
    """Analyse économique et énergétique des réseaux de chaleur urbains."""

    ENERGY_LABEL = {
        'Geothermie': 'ENR',
        'Solaire thermique': 'ENR',
        'Pompe chaleur': 'ENR',
        'Biomasse': 'ENR',
        'Cogénération biomasse': 'ENR-Mix',
        'Cogénération gaz': 'Fossile-Mix',
        'Gaz naturel': 'Fossile',
    }

    def __init__(self, networks_df: pd.DataFrame, economics_df: pd.DataFrame):
        self.networks = networks_df.copy()
        self.economics = economics_df.copy()
        self._merged = None

    def _get_merged(self) -> pd.DataFrame:
        if self._merged is None:
            self._merged = self.economics.merge(
                self.networks, on='id_reseau', how='left'
            )
            self._merged['marge_eur'] = (
                self._merged['recettes_eur'] - self._merged['charges_eur']
            )
            self._merged['marge_pct'] = (
                self._merged['marge_eur'] / self._merged['recettes_eur'] * 100
            )
            self._merged['pertes_pct'] = (
                self._merged['pertes_reseau_gwh'] /
                self._merged['energie_produite_gwh'] * 100
            )
            self._merged['cout_kwh_vente'] = self._merged['cout_production_kwh']
            self._merged['categorie_enr'] = self._merged['type_energie_principale'].map(
                self.ENERGY_LABEL
            )
        return self._merged

    def rentabilite(self) -> pd.DataFrame:
        """Marge nette par réseau et par année."""
        df = self._get_merged()
        return df.groupby(['id_reseau', 'nom_reseau', 'annee']).agg(
            recettes=('recettes_eur', 'sum'),
            charges=('charges_eur', 'sum'),
            marge=('marge_eur', 'sum'),
            marge_pct=('marge_pct', 'mean'),
        ).reset_index()

    def efficacite_energetique(self) -> pd.DataFrame:
        """Pertes réseau, rendement et ratio ENR par réseau."""
        df = self._get_merged()
        return df.groupby('id_reseau').agg(
            nom=('nom_reseau', 'first'),
            ville=('ville', 'first'),
            pertes_moy_pct=('pertes_pct', 'mean'),
            rendement_moy=('rendement_reseau_pct', 'mean'),
            enr_pct=('energie_renouvelable_pct', 'mean'),
            energie_type=('type_energie_principale', 'first'),
        ).reset_index().sort_values('rendement_moy', ascending=False)

    def classement_rentabilite(self) -> pd.DataFrame:
        """Classement des réseaux par marge cumulée sur toute la période."""
        df = self._get_merged()
        agg = df.groupby(['id_reseau', 'nom_reseau', 'ville']).agg(
            marge_totale=('marge_eur', 'sum'),
            recettes_totales=('recettes_eur', 'sum'),
            marge_pct_moy=('marge_pct', 'mean'),
            enr_pct=('energie_renouvelable_pct', 'mean'),
        ).reset_index()
        agg['rentable'] = agg['marge_totale'] > 0
        return agg.sort_values('marge_totale', ascending=False)

    def analyse_prix(self) -> pd.DataFrame:
        """Évolution du prix de vente vs coût de production par année."""
        df = self._get_merged()
        return df.groupby('annee').agg(
            prix_vente_moy=('prix_vente_kwh', 'mean'),
            cout_prod_moy=('cout_production_kwh', 'mean'),
            marge_kwh=('prix_vente_kwh', lambda x: x.mean() - df.loc[x.index, 'cout_production_kwh'].mean()),
        ).reset_index()

    def impact_enr(self) -> pd.DataFrame:
        """Corrélation entre taux ENR et rentabilité."""
        df = self._get_merged()
        return df.groupby('id_reseau').agg(
            nom=('nom_reseau', 'first'),
            enr_pct=('energie_renouvelable_pct', 'mean'),
            marge_pct_moy=('marge_pct', 'mean'),
            cout_moy=('cout_production_kwh', 'mean'),
        ).reset_index()

    def projection_recettes(self, annees_futures: int = 3) -> pd.DataFrame:
        """Projection linéaire des recettes sur N années futures."""
        df = self._get_merged()
        results = []
        for rid, group in df.groupby('id_reseau'):
            if len(group) < 2:
                continue
            X = group['annee'].values.reshape(-1, 1)
            y = group['recettes_eur'].values
            model = LinearRegression().fit(X, y)
            last_year = int(group['annee'].max())
            for i in range(1, annees_futures + 1):
                yr = last_year + i
                proj = model.predict([[yr]])[0]
                results.append({
                    'id_reseau': rid,
                    'nom_reseau': group['nom_reseau'].iloc[0],
                    'annee': yr,
                    'recettes_projetees': max(proj, 0),
                    'type': 'projection',
                })
        return pd.DataFrame(results)

    def score_performance(self) -> pd.DataFrame:
        """Score composite (0–100) combinant rentabilité, ENR et efficacité."""
        df = self._get_merged()
        agg = df.groupby(['id_reseau', 'nom_reseau', 'ville']).agg(
            marge_pct=('marge_pct', 'mean'),
            enr_pct=('energie_renouvelable_pct', 'mean'),
            rendement=('rendement_reseau_pct', 'mean'),
            taux_occ=('taux_occupation_pct', 'mean'),
        ).reset_index()

        scaler = StandardScaler()
        features = ['marge_pct', 'enr_pct', 'rendement', 'taux_occ']
        scores_norm = scaler.fit_transform(agg[features])
        weights = np.array([0.35, 0.25, 0.25, 0.15])
        agg['score_composite'] = (scores_norm * weights).sum(axis=1)
        agg['score_100'] = (
            (agg['score_composite'] - agg['score_composite'].min()) /
            (agg['score_composite'].max() - agg['score_composite'].min()) * 100
        ).round(1)
        return agg.sort_values('score_100', ascending=False)

    def summary(self) -> dict:
        df = self._get_merged()
        rentable = self.classement_rentabilite()
        return {
            'nb_reseaux': self.networks.shape[0],
            'periode': f"{int(df['annee'].min())}–{int(df['annee'].max())}",
            'recettes_totales_eur': int(df['recettes_eur'].sum()),
            'charges_totales_eur': int(df['charges_eur'].sum()),
            'marge_totale_eur': int(df['marge_eur'].sum()),
            'marge_pct_moyenne': round(df['marge_pct'].mean(), 1),
            'nb_reseaux_rentables': int((rentable['marge_totale'] > 0).sum()),
            'enr_pct_moyen': round(df['energie_renouvelable_pct'].mean(), 1),
            'rendement_moyen_pct': round(df['rendement_reseau_pct'].mean(), 1),
            'pertes_moy_pct': round(df['pertes_pct'].mean(), 1),
        }
