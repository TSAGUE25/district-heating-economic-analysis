"""
HeatingVisualizer — 8 figures pour l'analyse des réseaux de chaleur urbains.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
import numpy as np
import os

BG, BG2 = '#1E2235', '#252A3F'
ACC, ACC2, ACC3, ACC4 = '#00B0F0', '#FFC000', '#70AD47', '#FF4B4B'
TXT, TXT2, GRAY = '#FFFFFF', '#A8B2CC', '#3A4060'
COLORS = [ACC, ACC2, ACC3, ACC4, '#9B59B6', '#1ABC9C', '#E67E22', '#E91E63']


def _style():
    plt.rcParams.update({
        'figure.facecolor': BG, 'axes.facecolor': BG2,
        'axes.edgecolor': GRAY, 'text.color': TXT,
        'axes.labelcolor': TXT2, 'xtick.color': TXT2, 'ytick.color': TXT2,
        'grid.color': GRAY, 'grid.alpha': 0.4, 'axes.grid': True,
        'axes.spines.top': False, 'axes.spines.right': False,
        'font.family': 'DejaVu Sans', 'font.size': 9,
    })


def _header(fig, title, subtitle=''):
    fig.text(0.02, 0.97, title, fontsize=14, fontweight='bold', color=TXT, va='top')
    fig.text(0.02, 0.93, subtitle, fontsize=8, color=TXT2, va='top')
    fig.text(0.98, 0.97, 'District Heating Analytics', fontsize=8, color=ACC, va='top', ha='right')
    fig.add_artist(plt.Line2D([0.02, 0.98], [0.915, 0.915],
                              transform=fig.transFigure, color=ACC, lw=1.2, alpha=0.6))


class HeatingVisualizer:
    def __init__(self, analyzer, output_dir='figures'):
        self.a = analyzer
        self.out = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_all(self):
        _style()
        self.fig1_rentabilite()
        self.fig2_classement()
        self.fig3_prix_evolution()
        self.fig4_efficacite()
        self.fig5_enr_impact()
        self.fig6_pertes()
        self.fig7_score_composite()
        self.fig8_projection()

    def fig1_rentabilite(self):
        df = self.a.rentabilite()
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Rentabilité des Réseaux de Chaleur', 'Recettes vs charges par réseau — 2020–2023')
        top = df.groupby('nom_reseau')['marge'].sum().nlargest(8).index
        sub = df[df['nom_reseau'].isin(top)]
        pivot = sub.pivot_table(index='nom_reseau', columns='annee', values='marge', aggfunc='sum')
        pivot.plot(kind='bar', ax=axes[0], color=COLORS[:4], edgecolor=BG, width=0.7)
        axes[0].set_title('Marge nette par réseau (€)', color=TXT, fontweight='bold')
        axes[0].set_xlabel('')
        axes[0].tick_params(axis='x', rotation=35)
        axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)
        axes[0].axhline(0, color=ACC4, lw=1, linestyle='--')

        annual = df.groupby('annee').agg(rec=('recettes', 'sum'), ch=('charges', 'sum')).reset_index()
        x = np.arange(len(annual))
        axes[1].bar(x - 0.2, annual['rec'] / 1e6, 0.35, label='Recettes', color=ACC3, edgecolor=BG)
        axes[1].bar(x + 0.2, annual['ch'] / 1e6, 0.35, label='Charges', color=ACC4, edgecolor=BG)
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(annual['annee'].astype(str))
        axes[1].set_title('Recettes vs Charges — Parc total (M€)', color=TXT, fontweight='bold')
        axes[1].set_ylabel('Millions €')
        axes[1].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig1_rentabilite.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig2_classement(self):
        df = self.a.classement_rentabilite()
        fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
        _header(fig, 'Classement des Réseaux — Marge Cumulée 4 ans', 'Réseaux rentables vs déficitaires')
        colors = [ACC3 if v > 0 else ACC4 for v in df['marge_totale']]
        bars = ax.barh(df['nom_reseau'], df['marge_totale'] / 1e6, color=colors, edgecolor=BG)
        ax.axvline(0, color=TXT2, lw=1, linestyle='--')
        ax.set_xlabel('Marge cumulée (M€)')
        ax.set_title('Marge nette cumulée par réseau — 2020 à 2023', color=TXT, fontsize=11, fontweight='bold')
        for bar, v in zip(bars, df['marge_totale'] / 1e6):
            ax.text(v + 0.05 if v >= 0 else v - 0.05, bar.get_y() + bar.get_height() / 2,
                    f"{v:.1f}M€", va='center', ha='left' if v >= 0 else 'right', color=TXT, fontsize=8)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig2_classement.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig3_prix_evolution(self):
        df = self.a._get_merged()
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Évolution des Prix et Coûts', 'Prix de vente vs coût de production (€/kWh)')
        prix_yr = df.groupby('annee').agg(pv=('prix_vente_kwh', 'mean'), cp=('cout_production_kwh', 'mean')).reset_index()
        axes[0].plot(prix_yr['annee'], prix_yr['pv'] * 100, marker='o', color=ACC2, lw=2.5, label='Prix vente (c€/kWh)')
        axes[0].plot(prix_yr['annee'], prix_yr['cp'] * 100, marker='s', color=ACC4, lw=2.5, label='Coût production (c€/kWh)')
        axes[0].fill_between(prix_yr['annee'], prix_yr['cp'] * 100, prix_yr['pv'] * 100, alpha=0.2, color=ACC3, label='Marge')
        axes[0].set_title('Prix vs Coût moyen — Parc (c€/kWh)', color=TXT, fontweight='bold')
        axes[0].set_xlabel('Année'); axes[0].set_ylabel('c€/kWh')
        axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)

        prix_res = df.groupby('id_reseau').agg(
            nom=('nom_reseau', 'first'), pv=('prix_vente_kwh', 'mean'), cp=('cout_production_kwh', 'mean')
        ).reset_index().sort_values('pv', ascending=True)
        x = np.arange(len(prix_res))
        axes[1].barh(prix_res['nom'], (prix_res['pv'] - prix_res['cp']) * 100,
                     color=[ACC3 if v > 0 else ACC4 for v in prix_res['pv'] - prix_res['cp']], edgecolor=BG)
        axes[1].set_title('Marge unitaire par réseau (c€/kWh)', color=TXT, fontweight='bold')
        axes[1].set_xlabel('Marge (c€/kWh)')
        axes[1].axvline(0, color=TXT2, lw=1, linestyle='--')
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig3_prix_evolution.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig4_efficacite(self):
        df = self.a.efficacite_energetique()
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Efficacité Énergétique', 'Rendement réseau et taux de pertes par installation')
        df_s = df.sort_values('rendement_moy', ascending=True)
        colors = [ACC3 if v >= 90 else (ACC2 if v >= 85 else ACC4) for v in df_s['rendement_moy']]
        bars = axes[0].barh(df_s['nom'], df_s['rendement_moy'], color=colors, edgecolor=BG)
        axes[0].axvline(90, color=ACC3, lw=1.5, linestyle='--', alpha=0.7, label='Objectif 90%')
        axes[0].set_title('Rendement réseau (%) par installation', color=TXT, fontweight='bold')
        axes[0].set_xlabel('%'); axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)
        for bar, v in zip(bars, df_s['rendement_moy']):
            axes[0].text(v + 0.1, bar.get_y() + bar.get_height() / 2, f"{v:.1f}%",
                         va='center', color=TXT, fontsize=8)

        axes[1].scatter(df['enr_pct'], df['rendement_moy'],
                        c=[COLORS[i % len(COLORS)] for i in range(len(df))], s=120, edgecolors=BG, zorder=5)
        for _, row in df.iterrows():
            axes[1].annotate(row['nom'].split()[1], (row['enr_pct'], row['rendement_moy']),
                             fontsize=7, color=TXT2, xytext=(3, 3), textcoords='offset points')
        axes[1].set_title('ENR (%) vs Rendement réseau', color=TXT, fontweight='bold')
        axes[1].set_xlabel('Taux ENR (%)'); axes[1].set_ylabel('Rendement (%)')
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig4_efficacite.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig5_enr_impact(self):
        df = self.a.impact_enr()
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Impact des Énergies Renouvelables', 'Corrélation ENR — rentabilité et coût de production')
        axes[0].scatter(df['enr_pct'], df['marge_pct_moy'], s=100,
                        c=[ACC3 if v > 0 else ACC4 for v in df['marge_pct_moy']], edgecolors=BG)
        z = np.polyfit(df['enr_pct'], df['marge_pct_moy'], 1)
        p = np.poly1d(z)
        xr = np.linspace(df['enr_pct'].min(), df['enr_pct'].max(), 100)
        axes[0].plot(xr, p(xr), '--', color=ACC2, lw=1.5, alpha=0.8, label='Tendance')
        axes[0].set_title('Taux ENR vs Marge nette (%)', color=TXT, fontweight='bold')
        axes[0].set_xlabel('Taux ENR (%)'); axes[0].set_ylabel('Marge moy (%)')
        axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)

        axes[1].scatter(df['enr_pct'], df['cout_moy'] * 100, s=100,
                        c=[ACC if v >= 70 else ACC4 for v in df['enr_pct']], edgecolors=BG)
        z2 = np.polyfit(df['enr_pct'], df['cout_moy'] * 100, 1)
        p2 = np.poly1d(z2)
        axes[1].plot(xr, p2(xr), '--', color=ACC2, lw=1.5, alpha=0.8)
        axes[1].set_title('Taux ENR vs Coût de production (c€/kWh)', color=TXT, fontweight='bold')
        axes[1].set_xlabel('Taux ENR (%)'); axes[1].set_ylabel('Coût prod (c€/kWh)')
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig5_enr_impact.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig6_pertes(self):
        df = self.a._get_merged()
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Analyse des Pertes Réseau', 'Pertes thermiques par réseau et évolution temporelle')
        pertes = df.groupby('id_reseau').agg(
            nom=('nom_reseau', 'first'), pertes_pct=('pertes_pct', 'mean')
        ).reset_index().sort_values('pertes_pct', ascending=False)
        colors = [ACC4 if v > 15 else (ACC2 if v > 10 else ACC3) for v in pertes['pertes_pct']]
        bars = axes[0].barh(pertes['nom'], pertes['pertes_pct'], color=colors, edgecolor=BG)
        axes[0].axvline(10, color=ACC4, lw=1.5, linestyle='--', alpha=0.7, label='Seuil alerte 10%')
        axes[0].set_title('Pertes réseau moyennes (%)', color=TXT, fontweight='bold')
        axes[0].set_xlabel('Pertes (%)')
        axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)

        pertes_yr = df.groupby(['annee', 'id_reseau']).agg(
            pertes=('pertes_pct', 'mean'), nom=('nom_reseau', 'first')
        ).reset_index()
        for i, rid in enumerate(df['id_reseau'].unique()[:6]):
            sub = pertes_yr[pertes_yr['id_reseau'] == rid].sort_values('annee')
            if len(sub) > 0:
                axes[1].plot(sub['annee'], sub['pertes'], marker='o', color=COLORS[i],
                             lw=1.5, label=sub['nom'].iloc[0].split()[1], markersize=5)
        axes[1].set_title('Évolution des pertes — 6 réseaux (2020–2023)', color=TXT, fontweight='bold')
        axes[1].set_xlabel('Année'); axes[1].set_ylabel('Pertes (%)')
        axes[1].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY, fontsize=7)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig6_pertes.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig7_score_composite(self):
        df = self.a.score_performance()
        fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
        _header(fig, 'Score de Performance Composite', 'Combinaison : rentabilité (35%) + ENR (25%) + rendement (25%) + occupation (15%)')
        colors = [ACC3 if v >= 70 else (ACC2 if v >= 40 else ACC4) for v in df['score_100']]
        bars = ax.barh(df['nom_reseau'], df['score_100'], color=colors, edgecolor=BG)
        ax.axvline(70, color=ACC3, lw=1.5, linestyle='--', alpha=0.7, label='Score excellent (70)')
        ax.axvline(40, color=ACC2, lw=1.5, linestyle='--', alpha=0.7, label='Score correct (40)')
        ax.set_xlabel('Score composite (0–100)'); ax.set_xlim(0, 110)
        ax.set_title('Classement composite des réseaux de chaleur', color=TXT, fontsize=11, fontweight='bold')
        ax.legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)
        for bar, v in zip(bars, df['score_100']):
            ax.text(v + 1, bar.get_y() + bar.get_height() / 2, f"{v:.0f}/100",
                    va='center', color=TXT, fontsize=8)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig7_score_composite.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()

    def fig8_projection(self):
        df_hist = self.a._get_merged()
        df_proj = self.a.projection_recettes(annees_futures=3)
        fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=BG)
        _header(fig, 'Projection des Recettes 2024–2026', 'Régression linéaire par réseau — 3 ans')
        top5 = df_hist.groupby('id_reseau')['recettes_eur'].sum().nlargest(5).index
        for i, rid in enumerate(top5):
            hist = df_hist[df_hist['id_reseau'] == rid].sort_values('annee')
            proj = df_proj[df_proj['id_reseau'] == rid].sort_values('annee')
            nom = hist['nom_reseau'].iloc[0]
            axes[0].plot(hist['annee'], hist['recettes_eur'] / 1e6, marker='o',
                         color=COLORS[i], lw=2, label=nom.split()[1])
            axes[0].plot(proj['annee'], proj['recettes_projetees'] / 1e6,
                         marker='x', color=COLORS[i], lw=1.5, linestyle='--')
        axes[0].axvline(2023.5, color=TXT2, lw=1, linestyle=':', alpha=0.7)
        axes[0].set_title('Projection recettes — Top 5 réseaux (M€)', color=TXT, fontweight='bold')
        axes[0].set_xlabel('Année'); axes[0].set_ylabel('Recettes (M€)')
        axes[0].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY, fontsize=7)

        total_hist = df_hist.groupby('annee')['recettes_eur'].sum().reset_index()
        total_proj = df_proj.groupby('annee')['recettes_projetees'].sum().reset_index()
        axes[1].bar(total_hist['annee'].astype(str), total_hist['recettes_eur'] / 1e6,
                    color=ACC, edgecolor=BG, label='Réalisé')
        axes[1].bar(total_proj['annee'].astype(str), total_proj['recettes_projetees'] / 1e6,
                    color=ACC2, edgecolor=BG, alpha=0.7, label='Projeté')
        axes[1].set_title('Recettes totales parc — Réalisé vs Projeté (M€)', color=TXT, fontweight='bold')
        axes[1].set_ylabel('M€')
        axes[1].legend(facecolor=BG2, labelcolor=TXT, edgecolor=GRAY)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
        fig.savefig(f'{self.out}/fig8_projection.png', dpi=120, bbox_inches='tight', facecolor=BG)
        plt.close()
