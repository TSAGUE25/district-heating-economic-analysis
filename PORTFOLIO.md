# CAS D'USAGE 3 — Analyse Économique d'un Réseau de Chaleur Urbain
## Prioriser les raccordements rentables pour maximiser la valeur économique

> **Auteur :** Emmanuel TSAGUE — Data Scientist / Data Analyst  
> **Domaine :** Énergie, Analyse économique, Aide à la décision  
> **Repository GitHub :** `district-heating-economic-analysis`  
> **Statut :** Portfolio — données simulées  
> **Date :** Juin 2026

---

## 1. TITRE ET RÉSUMÉ EXÉCUTIF

**"Analyse économique d'un réseau de chaleur urbain pour prioriser les raccordements rentables et maximiser la valeur du réseau"**

> **Réseau de chaleur urbain :** infrastructure qui distribue de la chaleur (eau chaude sous pression) depuis une ou plusieurs sources centrales (cogénération, géothermie, biomasse, récupération d'énergie) vers des bâtiments raccordés. Alternatif aux chaudières individuelles, il mutualise la production et permet d'utiliser des énergies renouvelables ou de récupération.

> **Raccordement :** connexion physique d'un bâtiment au réseau de chaleur, impliquant des travaux de tranchée, une sous-station de livraison, et un contrat d'abonnement.

Un exploitant de réseau de chaleur doit décider quels bâtiments raccorder en priorité. Chaque raccordement a un coût d'infrastructure et génère des revenus sur 15-20 ans. Ce projet analyse la rentabilité, compare les scénarios et produit un classement des raccordements prioritaires.

**Résultats hypothétiques :** 23 raccordements rentables sur 50 candidats, VAN cumulée de 4,2 M€ sur 20 ans, payback moyen de 7,3 ans.

---

## 2. CONTEXTE MÉTIER

### Le réseau de chaleur en France

En France, plus de 800 réseaux de chaleur alimentent environ 2,5 millions d'équivalents logements. La transition énergétique pousse au développement de ces réseaux car ils permettent d'intégrer des énergies renouvelables et de récupération (ENR&R) à grande échelle.

> **Cogénération :** production simultanée d'électricité et de chaleur à partir d'un même combustible. La chaleur, qui serait sinon perdue, est injectée dans le réseau.

> **Taux EnR&R :** proportion d'énergie renouvelable et de récupération dans le mix du réseau. Un réseau > 50 % EnR&R bénéficie d'une TVA réduite à 5,5 %.

Un exploitant doit développer son réseau de façon rentable :
- Chaque nouveau raccordement augmente les revenus et améliore l'amortissement des investissements
- Mais chaque raccordement coûte (tranchées, sous-station, renforcement réseau)
- La distance au réseau existant, la consommation potentielle et la concurrence (fioul, gaz) déterminent la rentabilité

---

## 3. POURQUOI CE SUJET EXISTE

| Raison | Explication |
|--------|-------------|
| **Développement du réseau** | L'exploitant doit justifier ses investissements de développement devant ses actionnaires ou sa collectivité |
| **Ressources limitées** | Budget annuel de raccordement limité — besoin de prioriser |
| **Concurrence des énergies** | Un bâtiment déjà en gaz naturel est moins urgent qu'un bâtiment en fioul |
| **Réglementation** | Certaines zones obligent le raccordement (obligation de chaleur renouvelable) |
| **Rentabilité du réseau** | Plus le réseau est dense, plus les coûts fixes sont amortis |

---

## 4. PROBLÈME MÉTIER

> "Nous avons 50 bâtiments candidats au raccordement. Nous n'avons le budget que pour en raccorder 15 cette année. Lesquels choisir pour maximiser la valeur économique ?"

**Défis :**
1. Calculer la rentabilité de chaque raccordement (VAN, TRI, payback)
2. Tenir compte des contraintes réseau (capacité, distance, dénivelé)
3. Comparer des scénarios de développement (stratégie nord vs sud)
4. Identifier les synergies (raccorder un bâtiment ouvre la voie à 3 autres)
5. Communiquer les résultats aux décideurs non-financiers

---

## 5. OBJECTIFS DU PROJET

| Objectif | Livrable |
|----------|----------|
| Calculer rentabilité individuelle | Score rentabilité par bâtiment candidat |
| Optimiser le portefeuille | Sélection des N meilleurs raccordements sous contrainte budgétaire |
| Analyser les scénarios | Comparaison de 3-4 stratégies de développement |
| Visualiser le réseau | Carte des bâtiments et du réseau existant |
| Dashboard décisionnel | Power BI ou Python pour les décideurs |

---

## 6. DONNÉES UTILISÉES

> **Données simulées à titre pédagogique.**

**Table : `batiments_candidats.csv`**

| Variable | Type | Description | Utilité économique |
|----------|------|-------------|-------------------|
| `id_batiment` | Texte | Identifiant | Clé |
| `type_usage` | Catégorie | Résidentiel, tertiaire, industrie | Profil de consommation |
| `surface_m2` | Numérique | Surface chauffée | Estimation besoins |
| `conso_chaleur_mwh_an` | Numérique | Consommation annuelle estimée | Revenus potentiels |
| `energie_actuelle` | Catégorie | Fioul, gaz, élec, autre | Urgence de remplacement |
| `distance_reseau_m` | Numérique | Distance au réseau existant | Coût de tranchée |
| `denivele_m` | Numérique | Dénivelé topographique | Coût hydraulique |
| `nb_logements` | Entier | Pour résidentiel | Volume |
| `prix_chaleur_eur_mwh` | Numérique | Prix de vente proposé | Revenus |
| `cout_raccordement_eur` | Numérique | Coût estimé du raccordement | Investissement |
| `annee_construction` | Entier | Âge du bâtiment | Probabilité de raccordement |
| `statut_negociation` | Catégorie | Prospect, en cours, signé | Avancement |

---

## 7. PRÉPARATION DES DONNÉES

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 50  # 50 bâtiments candidats

# Génération des données simulées
types = ["Résidentiel","Tertiaire","Industrie","Éducation"]
energies = ["Fioul","Gaz naturel","Électricité","Réseau existant"]

df = pd.DataFrame({
    "id_batiment":          [f"BAT-{i:03d}" for i in range(1, n+1)],
    "type_usage":           np.random.choice(types, n, p=[0.5, 0.3, 0.1, 0.1]),
    "surface_m2":           np.random.uniform(500, 15000, n).round(),
    "conso_chaleur_mwh_an": np.random.uniform(50, 2000, n).round(1),
    "energie_actuelle":     np.random.choice(energies, n, p=[0.3, 0.4, 0.2, 0.1]),
    "distance_reseau_m":    np.random.uniform(20, 800, n).round(),
    "denivele_m":           np.random.uniform(0, 30, n).round(1),
    "nb_logements":         np.random.randint(0, 150, n),
    "prix_chaleur_eur_mwh": np.random.uniform(60, 110, n).round(2),
    "cout_raccordement_eur":np.random.uniform(15000, 200000, n).round(-3),
    "annee_construction":   np.random.randint(1950, 2015, n),
    "x_coord":              np.random.uniform(48.85, 48.92, n),  # Latitude simulée
    "y_coord":              np.random.uniform(2.30, 2.42, n),    # Longitude simulée
})

# Cohérence : coût proportionnel à la distance
df["cout_raccordement_eur"] = (
    df["distance_reseau_m"] * np.random.uniform(200, 400, n) +
    np.random.uniform(10000, 50000, n)
).round(-3)

df.to_csv("data_sample/batiments_candidats.csv", index=False)
```

---

## 8. MÉTHODES ET MODÈLES

### A. Calcul de la rentabilité — VAN, TRI, Payback

> **VAN (Valeur Actuelle Nette) :** somme des flux financiers futurs actualisés, diminuée de l'investissement initial. Une VAN positive signifie que le projet crée de la valeur. C'est l'indicateur de rentabilité de référence.

> **TRI (Taux de Rendement Interne) :** taux d'actualisation pour lequel la VAN est nulle. Un TRI supérieur au coût du capital signifie que l'investissement est rentable.

> **Payback (délai de récupération) :** nombre d'années nécessaires pour récupérer l'investissement initial grâce aux flux nets annuels.

> **Taux d'actualisation :** taux qui permet de "déprécier" les flux futurs pour les comparer à une dépense aujourd'hui. Un euro perçu dans 10 ans vaut moins qu'un euro perçu aujourd'hui.

```python
import numpy as np
import pandas as pd

def calculer_rentabilite(row, taux_actualisation=0.05, duree_ans=20,
                          taux_charges_fixes=0.03):
    """
    Calcule VAN, TRI et payback pour un raccordement.

    Hypothèses :
    - Revenus annuels = conso_mwh × prix_eur_mwh
    - Charges annuelles = taux_charges × investissement (maintenance)
    - Flux net annuel = revenus - charges
    - Investissement initial = cout_raccordement
    """
    investissement = row["cout_raccordement_eur"]
    revenu_annuel  = row["conso_chaleur_mwh_an"] * row["prix_chaleur_eur_mwh"]
    charges_annuelles = taux_charges_fixes * investissement
    flux_net_annuel = revenu_annuel - charges_annuelles

    # VAN
    van = -investissement + sum(
        flux_net_annuel / (1 + taux_actualisation) ** t
        for t in range(1, duree_ans + 1)
    )

    # Payback simple
    if flux_net_annuel <= 0:
        payback = float("inf")
    else:
        payback = investissement / flux_net_annuel

    # TRI (approximation par dichotomie)
    def van_at_rate(r):
        return -investissement + sum(
            flux_net_annuel / (1 + r) ** t for t in range(1, duree_ans + 1)
        )
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if van_at_rate(mid) > 0:
            lo = mid
        else:
            hi = mid
    tri = round((lo + hi) / 2 * 100, 2)

    return pd.Series({
        "revenu_annuel_eur":  round(revenu_annuel, 0),
        "flux_net_annuel":    round(flux_net_annuel, 0),
        "van_eur":            round(van, 0),
        "tri_pct":            tri,
        "payback_ans":        round(payback, 1)
    })

# Application sur tous les bâtiments
df_renta = df.apply(calculer_rentabilite, axis=1)
df = pd.concat([df, df_renta], axis=1)

# Score de rentabilité (classement)
df["rentable"] = df["van_eur"] > 0
df["score_priorite"] = (
    df["van_eur"].rank(pct=True) * 0.5 +
    (1 / df["payback_ans"]).rank(pct=True) * 0.3 +
    df["tri_pct"].rank(pct=True) * 0.2
)
df = df.sort_values("score_priorite", ascending=False)
```

### B. Optimisation sous contrainte budgétaire

```python
def optimiser_portefeuille(df, budget_total, methode="greedy"):
    """
    Sélectionne les raccordements maximisant la VAN totale
    sous contrainte de budget total.
    Méthode greedy : trier par VAN/coût décroissant, ajouter
    tant que le budget le permet.
    """
    df_candidats = df[df["rentable"]].copy()
    df_candidats["ratio_van_cout"] = (
        df_candidats["van_eur"] / df_candidats["cout_raccordement_eur"]
    )
    df_candidats = df_candidats.sort_values("ratio_van_cout", ascending=False)

    budget_restant = budget_total
    selectionnes = []

    for _, row in df_candidats.iterrows():
        if row["cout_raccordement_eur"] <= budget_restant:
            selectionnes.append(row["id_batiment"])
            budget_restant -= row["cout_raccordement_eur"]

    df_selection = df_candidats[df_candidats["id_batiment"].isin(selectionnes)]

    print(f"Budget total         : {budget_total:,.0f} €")
    print(f"Budget utilisé       : {budget_total - budget_restant:,.0f} €")
    print(f"Raccordements choisis: {len(selectionnes)}")
    print(f"VAN totale           : {df_selection['van_eur'].sum():,.0f} €")
    print(f"Revenu annuel total  : {df_selection['revenu_annuel_eur'].sum():,.0f} €")
    return df_selection

# Optimisation avec budget de 1,5 M€
df_optimal = optimiser_portefeuille(df, budget_total=1_500_000)
```

### C. Analyse de scénarios

```python
def comparer_scenarios(df):
    """Compare plusieurs stratégies de développement."""
    scenarios = {
        "S1_Proximité":   df[df["distance_reseau_m"] < 100],
        "S2_GrosVolumes": df[df["conso_chaleur_mwh_an"] > 500],
        "S3_Fioul_Only":  df[df["energie_actuelle"] == "Fioul"],
        "S4_Rentabilite": df[df["van_eur"] > 0].head(15)
    }
    resultats = []
    for nom, subset in scenarios.items():
        resultats.append({
            "Scénario":             nom,
            "Nb raccordements":     len(subset),
            "Investissement total": f"{subset['cout_raccordement_eur'].sum():,.0f} €",
            "VAN totale":           f"{subset['van_eur'].sum():,.0f} €",
            "Revenu annuel":        f"{subset['revenu_annuel_eur'].sum():,.0f} €",
            "Payback moyen (ans)":  round(subset['payback_ans'].mean(), 1)
        })
    return pd.DataFrame(resultats)

df_scenarios = comparer_scenarios(df)
print(df_scenarios.to_string(index=False))
```

### D. Visualisation — Carte et graphiques

```python
import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 1. Carte des bâtiments (scatter plot simulant une carte)
scatter = axes[0].scatter(
    df["y_coord"], df["x_coord"],
    c=df["van_eur"], cmap="RdYlGn",
    s=df["conso_chaleur_mwh_an"] / 10,
    alpha=0.7, edgecolors="white"
)
plt.colorbar(scatter, ax=axes[0], label="VAN (€)")
axes[0].set_title("Carte des bâtiments candidats\n(couleur = VAN, taille = consommation)")
axes[0].set_xlabel("Longitude simulée")
axes[0].set_ylabel("Latitude simulée")

# 2. Analyse rentabilité — scatter VAN vs coût
colors = ["green" if r else "red" for r in df["rentable"]]
axes[1].scatter(
    df["cout_raccordement_eur"] / 1000,
    df["van_eur"] / 1000,
    c=colors, alpha=0.7, s=50
)
axes[1].axhline(y=0, color="black", linestyle="--", linewidth=1)
axes[1].set_xlabel("Coût de raccordement (k€)")
axes[1].set_ylabel("VAN sur 20 ans (k€)")
axes[1].set_title("Rentabilité des raccordements candidats")
from matplotlib.patches import Patch
axes[1].legend(handles=[Patch(color="green", label="Rentable"),
                         Patch(color="red",   label="Non rentable")])

plt.tight_layout()
plt.savefig("figures/analyse_rentabilite.png", dpi=150, bbox_inches="tight")
```

---

## 9. DÉMARCHE ÉTAPE PAR ÉTAPE

```
ÉTAPE 1 : Constitution de la liste des bâtiments candidats
ÉTAPE 2 : Collecte des données (distance, conso, coût estimé)
ÉTAPE 3 : Calcul VAN / TRI / Payback par bâtiment
ÉTAPE 4 : Classement des bâtiments rentables
ÉTAPE 5 : Optimisation du portefeuille sous contrainte budgétaire
ÉTAPE 6 : Analyse de scénarios (4 stratégies)
ÉTAPE 7 : Cartographie et visualisation
ÉTAPE 8 : Rapport décisionnel et dashboard Power BI
```

---

## 10. MÉTRIQUES

| Métrique | Formule | Seuil rentabilité | Interprétation |
|----------|---------|-------------------|----------------|
| **VAN (€)** | ΣFlux/(1+r)^t - I | > 0 | Création de valeur |
| **TRI (%)** | VAN = 0 | > taux d'actualisation (5%) | Rendement du projet |
| **Payback (ans)** | I / Flux annuel net | < 12 ans | Récupération investissement |
| **Ratio VAN/Coût** | VAN / Investissement | > 0,5 | Efficacité de l'euro investi |
| **Revenu annuel (€)** | Conso × Prix | > Charges annuelles | Flux entrant |
| **Densité thermique (MWh/m)** | Conso / Distance réseau | > 1,5 | Efficacité du développement |

> **Densité thermique linéaire :** indicateur clé en développement de réseau. Une densité > 1,5 MWh/m de réseau signifie que la chaleur vendue par mètre de tranchée est suffisante pour rentabiliser le réseau.

---

## 11. RÉSULTATS SIMULÉS

| Indicateur | Valeur |
|-----------|--------|
| Bâtiments candidats analysés | 50 |
| Bâtiments rentables (VAN > 0) | 23 (46 %) |
| Budget optimisé (1,5 M€) | 15 raccordements |
| VAN totale portefeuille optimal | 4,2 M€ (simulé) |
| Revenu annuel additionnel | 485 000 €/an (simulé) |
| Payback moyen | 7,3 ans (simulé) |
| TRI moyen | 11,8 % (simulé) |

**Top 5 raccordements (hypothétiques) :**

| Rang | Bâtiment | Conso (MWh) | Coût (€) | VAN (€) | Payback |
|------|----------|-------------|----------|---------|---------|
| 1 | BAT-012 | 1 850 | 85 000 | 312 000 | 4,2 ans |
| 2 | BAT-031 | 1 420 | 72 000 | 245 000 | 4,8 ans |
| 3 | BAT-007 | 980 | 45 000 | 198 000 | 5,1 ans |
| 4 | BAT-044 | 1 100 | 95 000 | 187 000 | 6,3 ans |
| 5 | BAT-019 | 750 | 38 000 | 165 000 | 5,8 ans |

---

## 12. VALEUR MÉTIER

| Valeur | Description |
|--------|-------------|
| **Objectivation** | Les décisions de raccordement ne sont plus intuitives mais basées sur des calculs |
| **Priorisation** | Les équipes terrain concentrent leurs efforts sur les meilleurs prospects |
| **Budget** | L'investissement annuel génère la VAN maximale |
| **Argumentation** | Les commerciaux ont des chiffres pour convaincre les propriétaires |
| **Stratégie** | Les scénarios permettent de choisir une stratégie de développement cohérente |

---

## 13. LIMITES

| Limite | Description |
|--------|-------------|
| Estimations des coûts | Les coûts de raccordement sont estimés, pas chiffrés par un bureau d'études |
| Hypothèses de consommation | La consommation réelle peut différer de l'estimation |
| Taux d'actualisation | Le choix du taux (ici 5 %) influence fortement la VAN |
| Acceptation client | Un bâtiment rentable peut refuser de se raccorder |
| Synergies non modélisées | Raccorder un bâtiment peut rendre rentable le suivant |
| Graphes de réseau | Le modèle greedy ne capture pas la topologie du réseau |

---

## 14. AMÉLIORATIONS

- **Théorie des graphes (NetworkX)** : modéliser le réseau et optimiser les tracés
- **Programmation linéaire** : optimisation exacte (vs greedy) avec PuLP ou scipy
- **Monte Carlo** : simuler l'incertitude sur les consommations et coûts
- **SIG (Système d'Information Géographique)** : intégration Geopandas + Folium pour cartographie interactive
- **Optimisation multi-objectifs** : maximiser VAN ET minimiser CO₂

> **Programmation linéaire :** méthode mathématique d'optimisation pour trouver la meilleure solution (maximiser un objectif) sous des contraintes linéaires (budget, capacité). Plus précise que l'algorithme greedy.

> **Monte Carlo :** méthode qui simule des milliers de scénarios avec des paramètres tirés aléatoirement (dans leur plage d'incertitude) pour évaluer la robustesse d'une décision.

---

## 15. ARCHITECTURE GITHUB

```
district-heating-economic-analysis/
├── README.md
├── requirements.txt
├── data_sample/
│   ├── batiments_candidats.csv
│   └── generate_data.py
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   ├── 02_calcul_rentabilite.ipynb
│   ├── 03_optimisation_portefeuille.ipynb
│   ├── 04_scenarios.ipynb
│   └── 05_visualisation_carte.ipynb
├── src/
│   ├── economic_model.py
│   ├── portfolio_optimizer.py
│   └── scenario_analyzer.py
├── reports/
│   └── rapport_rentabilite.md
├── figures/
│   ├── analyse_rentabilite.png
│   └── comparaison_scenarios.png
└── docs/
    └── methodologie_van_tri.md
```

---

## 16. README GITHUB

```markdown
# District Heating Economic Analysis
## Analyse économique de raccordements à un réseau de chaleur urbain

> **Auteur :** Emmanuel TSAGUE | **Données :** simulées

## Objectif
Calculer la rentabilité (VAN, TRI, Payback) de chaque bâtiment candidat,
optimiser le portefeuille sous contrainte budgétaire et comparer des scénarios.

## Méthodes
- VAN / TRI / Payback par bâtiment
- Optimisation greedy sous contrainte budget
- Analyse de 4 scénarios de développement
- Cartographie des candidats

## Résultats (simulés)
- 23/50 bâtiments rentables | VAN portefeuille : 4,2 M€ | Payback moyen : 7,3 ans

## Avertissement
Données et résultats entièrement simulés — aucune organisation réelle.
```

---

## 17. VERSION CV

> Analyse économique de raccordements à un réseau de chaleur urbain : calcul VAN/TRI/Payback par bâtiment candidat, optimisation de portefeuille sous contrainte budgétaire (algorithme greedy), comparaison de 4 scénarios de développement, cartographie Python et dashboard décisionnel — Python, pandas, numpy, matplotlib.

---

## 18. VERSION ENTRETIEN

"J'ai travaillé sur un cas d'analyse économique pour un réseau de chaleur urbain. Le problème : un exploitant avait 50 bâtiments candidats au raccordement mais seulement le budget pour en connecter 15. Il fallait décider lesquels maximisaient la valeur économique. J'ai construit un modèle en trois temps : calcul individuel de la VAN, du TRI et du payback pour chaque bâtiment ; optimisation du portefeuille sous contrainte budgétaire par un algorithme greedy qui maximise le ratio VAN sur coût d'investissement ; et comparaison de quatre scénarios stratégiques. Les résultats simulés montrent que 46 % des candidats sont rentables, avec une VAN cumulée de 4,2 M€ sur 20 ans pour le portefeuille optimal. La limite principale : le modèle ne capture pas les synergies entre raccordements — raccorder un bâtiment peut rendre le suivant rentable. L'amélioration naturelle serait d'intégrer la théorie des graphes avec NetworkX."

---

## 19. VERSION PORTFOLIO

Ce projet démontre la capacité à combiner finance, énergie et Data Science pour répondre à une question stratégique concrète. Il est directement transférable à des contextes de gestion de portefeuille d'investissements : quels projets financer en priorité avec un budget limité ? La méthodologie VAN/TRI/Payback s'applique à tout projet d'infrastructure énergétique : extension de réseau d'eau, déploiement de bornes de recharge, installation de panneaux solaires en toiture.

**Transférabilité EDF/Enedis :** analyse de rentabilité des projets de raccordement réseau électrique, priorisation des investissements de modernisation du réseau, analyse coût/bénéfice des effacements de consommation.

---

## 20. POST LINKEDIN

**Data Science + énergie + finance : trois domaines qui font sens ensemble.**

Comment décider quels bâtiments raccorder en priorité à un réseau de chaleur quand le budget est limité ?

J'ai construit un modèle d'analyse économique qui calcule automatiquement, pour chaque bâtiment candidat : la Valeur Actuelle Nette sur 20 ans, le Taux de Rendement Interne, et le délai de récupération de l'investissement.

Puis un algorithme d'optimisation qui sélectionne le portefeuille de raccordements qui maximise la VAN totale sous contrainte budgétaire.

Résultat simulé : sur 50 candidats, 23 sont rentables. Le portefeuille optimal de 15 raccordements génère 4,2 M€ de VAN cumulée pour 1,5 M€ investi.

Ce type de modèle permet de passer de l'intuition à la décision objectivée — ce qui est l'essence même du travail Data Analyst en environnement énergie.

`#Énergie` `#ReseauDeChaleur` `#DataScience` `#AnalyseEconomique` `#Python` `#Investissement`

---

## 21. QUESTIONS D'ENTRETIEN

**Q : Qu'est-ce que la VAN et comment l'interpréter ?**
> La VAN est la somme des flux financiers futurs actualisés, diminuée de l'investissement initial. VAN > 0 : le projet crée de la valeur — il faut l'accepter. VAN < 0 : le projet détruit de la valeur. L'actualisation tient compte du fait qu'un euro futur vaut moins qu'un euro aujourd'hui.

**Q : Quelle différence entre TRI et VAN ? Lequel utiliser ?**
> La VAN mesure la valeur créée en euros. Le TRI mesure le rendement en pourcentage. Pour comparer des projets de taille différente, la VAN est plus fiable. Pour communiquer avec des financiers, le TRI est plus intuitif. En pratique, on utilise les deux.

**Q : Qu'est-ce qu'un algorithme greedy ?**
> Un algorithme greedy (glouton) prend à chaque étape la meilleure décision locale sans revenir en arrière. Ici : trier les bâtiments par ratio VAN/coût décroissant, et les ajouter au portefeuille tant que le budget le permet. C'est simple et rapide, mais pas toujours optimal (il peut manquer des combinaisons meilleures). La programmation linéaire donne la solution exacte.

**Q : Comment modéliser les synergies entre raccordements ?**
> Avec la théorie des graphes : chaque bâtiment est un nœud, le réseau existant est le graphe initial. Raccorder un bâtiment ajoute un nœud et peut réduire la distance d'autres bâtiments. NetworkX permet de calculer les plus courts chemins et d'évaluer l'impact de chaque raccordement sur le réseau global.

---

## 22-23. COMPÉTENCES DÉMONTRÉES

| Compétence | Preuve | Valeur | Phrase CV |
|-----------|--------|--------|-----------|
| Analyse financière | VAN, TRI, Payback | Décision d'investissement | "Modélisation économique : VAN, TRI, Payback Python" |
| Optimisation | Algorithme greedy sous contrainte | Maximisation ROI | "Optimisation de portefeuille sous contrainte budgétaire" |
| Énergie | Réseau chaleur, ENR&R, densité thermique | Expertise sectorielle | "Analyse économique infrastructure énergétique" |
| Scénarios | 4 stratégies comparées | Aide à la décision | "Analyse comparative de scénarios d'investissement" |
| Python | numpy, pandas, matplotlib | Automatisation | "Modèle financier Python automatisé" |
| Visualisation | Carte, scatter, comparaison | Communication | "Cartographie et visualisation décisionnelle" |

---

## 24. CONSEILS GITHUB

- Inclure une figure du schéma de réseau simulé — visuellement très impactant pour les recruteurs énergie
- Documenter les hypothèses financières dans `docs/methodologie_van_tri.md`
- Ajouter un notebook de sensibilité : "que se passe-t-il si le taux d'actualisation passe de 5 % à 8 % ?"
- Montrer clairement la distinction entre modèle greedy et optimal

---

*Fin du document — Emmanuel TSAGUE — CAS 3 — Analyse Économique Réseau de Chaleur*
