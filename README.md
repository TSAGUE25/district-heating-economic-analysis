# District Heating Economic Analysis

> Analyse économique et énergétique de 15 réseaux de chaleur urbains (RCU) : rentabilité, efficacité, impact des ENR, score composite et projection des recettes.  
> **Stack :** Python · pandas · scikit-learn · matplotlib · seaborn

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-Data%20Science-orange)](https://github.com/TSAGUE25)

---

## Table des matières

1. [Titre et accroche](#1-titre-et-accroche)
2. [Contexte métier](#2-contexte-métier)
3. [Pourquoi ce projet existe](#3-pourquoi-ce-projet-existe)
4. [Problème métier](#4-problème-métier)
5. [Objectifs](#5-objectifs)
6. [Données utilisées](#6-données-utilisées)
7. [Préparation des données](#7-préparation-des-données)
8. [Méthodes et algorithmes](#8-méthodes-et-algorithmes)
9. [Démarche analytique](#9-démarche-analytique)
10. [Métriques clés](#10-métriques-clés)
11. [Explication des métriques](#11-explication-des-métriques)
12. [Résultats obtenus](#12-résultats-obtenus)
13. [Valeur métier](#13-valeur-métier)
14. [Limites du projet](#14-limites-du-projet)
15. [Améliorations possibles](#15-améliorations-possibles)
16. [Architecture du dépôt](#16-architecture-du-dépôt)
17. [README technique](#17-readme-technique)
18. [Version CV](#18-version-cv)
19. [Version entretien](#19-version-entretien)
20. [Version portfolio](#20-version-portfolio)
21. [Post LinkedIn](#21-post-linkedin)
22. [Questions d'entretien](#22-questions-dentretien)
23. [Compétences démontrées](#23-compétences-démontrées)
24. [Tableau compétences / preuves](#24-tableau-compétences--preuves)
25. [Conseils GitHub](#25-conseils-github)

---

## 1. Titre et accroche

**District Heating Economic Analysis** — Tableau de bord analytique complet sur 15 réseaux de chaleur urbains : analyse de rentabilité, efficacité énergétique, impact des ENR sur les coûts, score composite de performance et projection des recettes sur 3 ans par régression linéaire.

> *Ce projet illustre la capacité à analyser des actifs d'infrastructure énergétique avec des métriques financières et techniques combinées — compétence clé dans le secteur de l'énergie (EDF, Dalkia, ENGIE, collectivités).*

---

## 2. Contexte métier

Les réseaux de chaleur urbains (RCU) distribuent de la chaleur à partir d'une production centralisée vers des bâtiments résidentiels, tertiaires et industriels. En France, ils représentent plus de **30 000 km de canalisations**, 750 000 logements équivalents, et une production de **35 TWh/an**.

Avec la transition énergétique, les gestionnaires de RCU doivent simultanément :
- **Optimiser la rentabilité** face à la hausse des coûts de maintenance
- **Augmenter la part d'ENR** pour atteindre les objectifs climatiques (loi Énergie-Climat 2019)
- **Réduire les pertes réseau** qui représentent 10 à 20% de l'énergie produite

---

## 3. Pourquoi ce projet existe

**Problème concret :** Un gestionnaire de parc RCU ne dispose pas d'un tableau de bord unifié pour comparer ses installations sur des critères homogènes (financiers, énergétiques, environnementaux). Il ne sait pas quels réseaux prioriser pour les investissements de rénovation.

**Ce que ce projet apporte :**
- Classement objectif des réseaux par score composite
- Corrélation quantifiée entre taux ENR et réduction des coûts
- Projection des recettes pour le plan pluriannuel d'investissement
- Identification des réseaux déficitaires nécessitant une intervention

---

## 4. Problème métier

> *"Sur nos 15 réseaux, certains sont rentables et d'autres non. Comment identifier lesquels prioriser en investissement ? Est-ce que passer à plus d'ENR améliore réellement la rentabilité ? Où sont les plus grosses pertes ?"*

**Traduction analytique :**
- Calculer la marge nette (€ et %) par réseau sur 4 ans
- Quantifier la corrélation ENR / coût de production / marge
- Créer un score composite multicritère pour classer les actifs
- Projeter les recettes à 3 ans par régression linéaire

---

## 5. Objectifs

| # | Objectif | Méthode |
|---|----------|---------|
| 1 | Calculer la rentabilité par réseau | Marge = recettes − charges |
| 2 | Comparer prix vente vs coût production | Analyse prix unitaire (€/kWh) |
| 3 | Mesurer l'efficacité énergétique | Rendement réseau, taux de pertes |
| 4 | Quantifier l'impact des ENR | Corrélation + régression |
| 5 | Créer un score composite | StandardScaler + pondération |
| 6 | Projeter les recettes | Régression linéaire sklearn |
| 7 | Produire un classement actionnable | Rapport avec recommandations |

---

## 6. Données utilisées

> **Données entièrement simulées — aucune donnée réelle ou confidentielle.**

### `heating_network.csv` — 15 réseaux fictifs

| Colonne | Description |
|---------|-------------|
| `id_reseau` | Identifiant unique (RCU001–RCU015) |
| `type_energie_principale` | Biomasse, Géothermie, Gaz naturel, Cogénération... |
| `energie_renouvelable_pct` | Part d'ENR dans la production (%) |
| `rendement_reseau_pct` | Efficacité thermique (%) |
| `longueur_reseau_km` | Longueur du réseau de distribution |

### `annual_economics.csv` — 60 lignes (15 réseaux × 4 ans)

| Colonne | Description |
|---------|-------------|
| `recettes_eur` | Revenus de vente de chaleur (€) |
| `charges_eur` | Charges opérationnelles totales (€) |
| `cout_production_kwh` | Coût de production unitaire (€/kWh) |
| `prix_vente_kwh` | Prix de vente moyen (€/kWh) |
| `pertes_reseau_gwh` | Pertes thermiques (GWh) |

---

## 7. Préparation des données

```python
# Jointure réseaux + économique
merged = economics.merge(networks, on='id_reseau', how='left')

# Calcul des métriques dérivées
merged['marge_eur'] = merged['recettes_eur'] - merged['charges_eur']
merged['marge_pct'] = merged['marge_eur'] / merged['recettes_eur'] * 100
merged['pertes_pct'] = merged['pertes_reseau_gwh'] / merged['energie_produite_gwh'] * 100
```

---

## 8. Méthodes et algorithmes

| Méthode | Usage | Module |
|---------|-------|--------|
| Agrégation pandas (groupby) | Rentabilité par réseau/année | `pandas` |
| Corrélation de Pearson | ENR vs coût, ENR vs marge | `pandas.corr()` |
| Régression linéaire | Projection recettes 2024–2026 | `sklearn.LinearRegression` |
| StandardScaler + pondération | Score composite normalisé | `sklearn.StandardScaler` |
| Min-max normalization | Score sur 0–100 | `numpy` |

---

## 9. Démarche analytique

```
15 réseaux × 4 ans (60 obs.)
        │
        ▼
    EDA — types énergie, régions, ancienneté
        │
        ├──→ Rentabilité (marge €/%) par réseau et année
        ├──→ Analyse prix vente vs coût production (€/kWh)
        ├──→ Efficacité énergétique (rendement + pertes %)
        ├──→ Impact ENR (corrélation + régression)
        ├──→ Score composite (rentabilité + ENR + rendement + occupation)
        └──→ Projection recettes 2024–2026 (régression linéaire)
                        │
                        ▼
            8 figures + rapport Markdown
```

---

## 10. Métriques clés

| Métrique | Formule | Interprétation |
|----------|---------|----------------|
| Marge nette (%) | (Recettes − Charges) / Recettes | Rentabilité opérationnelle |
| Pertes réseau (%) | Pertes GWh / Production GWh | Efficacité de distribution |
| Coût production (€/kWh) | Charges / Énergie vendue | Compétitivité tarifaire |
| Score composite | Pondération normalisée 4 critères | Classement global |
| CV-AUC projection | R² de la régression linéaire | Fiabilité des projections |

---

## 11. Explication des métriques

### Marge nette vs EBITDA
La marge nette ici est opérationnelle (recettes − charges d'exploitation). Elle ne tient pas compte de l'amortissement des investissements ni des subventions, pour comparer les performances d'exploitation intrinsèques.

### Score composite — pourquoi pondérer ?
Les 4 critères n'ont pas la même échelle ni la même importance métier. La normalisation (StandardScaler) les rend comparables, puis la pondération (35% rentabilité, 25% ENR, 25% rendement, 15% occupation) reflète les priorités stratégiques d'un exploitant.

### Projection par régression linéaire
Adaptée pour une période courte (4 points historiques) et une tendance stable. Pour des projections plus longues, un modèle ARIMA ou une décomposition saisonnière serait préférable.

---

## 12. Résultats obtenus

### Rentabilité (2020–2023)

| Réseau | Marge cumulée | Marge % moy. | Type énergie |
|--------|--------------|-------------|-------------|
| Réseau Ouest (Grenoble) | **+34.2 M€** | **22.4%** | Géothermie 98% |
| Réseau Nord (Paris) | +28.6 M€ | 19.8% | Biomasse 72% |
| Réseau Est (Paris) | +18.4 M€ | 21.1% | Géothermie 95% |
| Réseau Historique (Metz) | **−4.2 M€** | **−5.1%** | Gaz naturel 8% |
| Réseau Ancien (Bordeaux) | **−6.8 M€** | **−7.3%** | Gaz naturel 5% |

### Impact ENR sur les coûts

- **Corrélation ENR / coût production : −0.81** (forte corrélation inverse)
- Les réseaux > 85% ENR ont un coût de production **moyen de 4.3 c€/kWh**
- Les réseaux < 20% ENR ont un coût **moyen de 7.4 c€/kWh** (+72%)

### Pertes réseau

- Moyenne parc : **10.8%** des pertes
- Meilleur : Réseau ENR Montpellier (5.8%)
- Plus élevé : Réseau Ancien Bordeaux (19.8%) — réseau vétuste

---

## 13. Valeur métier

| Décision | Donnée fournie |
|----------|---------------|
| Quels réseaux rénover en priorité ? | Score composite + pertes réseau |
| Faut-il convertir les réseaux gaz ? | Corrélation ENR/coût (-0.81) |
| Plan pluriannuel d'investissement | Projection recettes 2024–2026 |
| Revalorisation tarifaire | Évolution coût production vs prix vente |

---

## 14. Limites du projet

| Limite | Impact |
|--------|--------|
| 15 réseaux seulement | Insuffisant pour un modèle statistique robuste |
| Régression linéaire | Ne capture pas les ruptures (hausse gaz 2022) |
| Pas d'amortissement | Marge opérationnelle ≠ rentabilité comptable |
| Données simulées | Paramètres non calés sur des réseaux réels |
| Pas de dimension géographique | Pas de carte des pertes par tronçon |

---

## 15. Améliorations possibles

- **SIG / GeoPandas** : cartographier les réseaux et les pertes par tronçon
- **Modèle ARIMA** : projection avec saisonnalité (DJU) pour les recettes
- **Optimisation tarifaire** : modèle d'élasticité prix / volume
- **Simulation scénarios ENR** : impact d'une conversion progressive sur 10 ans
- **Dashboard Streamlit** : interface interactive pour les exploitants

---

## 16. Architecture du dépôt

```
district-heating-economic-analysis/
│
├── data_sample/
│   ├── heating_network.csv     # 15 réseaux fictifs
│   └── annual_economics.csv   # 60 lignes économiques (2020–2023)
│
├── src/
│   ├── __init__.py
│   ├── heating_analyzer.py    # Classe HeatingAnalyzer (7 méthodes)
│   └── visualization.py       # Classe HeatingVisualizer (8 figures)
│
├── notebooks/
│   └── 01_heating_analysis.py  # Script complet 10 sections
│
├── figures/                    # 8 visualisations générées
├── reports/
│   └── heating_report_sample.md
│
├── docs/
│   └── methodologie.md
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 17. README technique

### Installation

```bash
git clone https://github.com/TSAGUE25/district-heating-economic-analysis
cd district-heating-economic-analysis
pip install -r requirements.txt
```

### Exécution

```bash
python notebooks/01_heating_analysis.py
```

### Utilisation directe

```python
import pandas as pd
from src.heating_analyzer import HeatingAnalyzer

networks  = pd.read_csv('data_sample/heating_network.csv')
economics = pd.read_csv('data_sample/annual_economics.csv')

analyzer = HeatingAnalyzer(networks, economics)
print(analyzer.summary())
print(analyzer.classement_rentabilite())
print(analyzer.score_performance())
print(analyzer.projection_recettes(annees_futures=3))
```

---

## 18. Version CV

> *À copier dans la section "Projets" du CV*

**District Heating Economic Analysis** | Python, pandas, scikit-learn, matplotlib  
Analyse économique de 15 réseaux de chaleur urbains sur 4 ans (2020–2023) : calcul de rentabilité, corrélation ENR/coût de production (r = −0.81), score composite multicritère (StandardScaler + pondération), projection des recettes par régression linéaire, 8 visualisations. Architecture OOP avec classes `HeatingAnalyzer` et `HeatingVisualizer`.

---

## 19. Version entretien

*Question : "Avez-vous de l'expérience sur l'analyse de données dans le secteur de l'énergie ?"*

> "Oui, j'ai réalisé un projet d'analyse économique sur des réseaux de chaleur urbains — un sujet directement lié aux enjeux de la transition énergétique.
>
> J'ai analysé 15 réseaux sur 4 ans : calcul de marge opérationnelle, analyse du coût de production par type d'énergie, et j'ai quantifié la corrélation entre le taux d'ENR et le coût de production — elle est de −0.81 : chaque point de progression en ENR réduit le coût de production de manière significative.
>
> J'ai aussi construit un score composite pour classer les réseaux selon 4 critères pondérés, et projeté les recettes à 3 ans par régression linéaire pour alimenter un plan pluriannuel d'investissement.
>
> Ce type d'analyse m'intéresse particulièrement dans un contexte comme EDF ou une collectivité gérant un parc d'actifs énergétiques."

---

## 20. Version portfolio

Ce projet démontre la capacité à croiser des données financières et techniques sur des actifs d'infrastructure pour produire un classement objectif et des recommandations d'investissement. Il mobilise des techniques d'agrégation pandas, de corrélation statistique, de normalisation sklearn et de régression linéaire dans un contexte métier réaliste.

**Adapté pour :** EDF, Dalkia, ENGIE, Coriance, collectivités territoriales, bureaux d'études énergie.

---

## 21. Post LinkedIn

> **Les réseaux de chaleur au gaz coûtent 72% de plus à produire que les réseaux ENR**
>
> C'est ce que révèle mon analyse sur 15 réseaux de chaleur urbains fictifs.
>
> Ce que j'ai fait :
>
> Analysé 4 ans de données économiques (2020–2023)  
> Calculé la marge nette par réseau  
> Quantifié la corrélation ENR / coût de production : **r = −0.81**  
> Construit un score composite pour classer les actifs  
> Projeté les recettes à 3 ans  
>
> Résultat : les réseaux géothermie et biomasse à 90%+ ENR sont à la fois les plus rentables ET les plus efficaces énergétiquement.
>
> Code complet sur GitHub  
> #DataScience #Energie #RéseauxDeChaleur #Python #Portfolio #EDF

---

## 22. Questions d'entretien

**Q1 : Qu'est-ce qu'un réseau de chaleur urbain ?**  
Un RCU produit de la chaleur (eau chaude sous pression) dans une centrale et la distribue via un réseau de canalisations isolées à des abonnés résidentiels, tertiaires ou industriels. En France, on compte ~800 RCU couvrant environ 5% de la consommation de chaleur.

**Q2 : Pourquoi normaliser avec StandardScaler avant de créer un score composite ?**  
Les variables ont des échelles très différentes : la marge est en %, l'ENR en %, le rendement en %, mais les plages de valeurs diffèrent. Sans normalisation, une variable avec une grande variance domine le score. StandardScaler centre et réduit chaque variable (μ=0, σ=1) avant pondération.

**Q3 : Quelle est la limite de la régression linéaire pour projeter les recettes d'un réseau de chaleur ?**  
Les recettes d'un RCU dépendent fortement des DJU (degrés-jours unifiés) qui varient d'une année à l'autre selon la météo. Une régression linéaire sur le temps ne capte pas cette saisonnalité. Un modèle plus robuste inclurait les DJU comme variable prédictive ou utiliserait une décomposition temporelle.

**Q4 : Comment calculer le taux de pertes réseau et qu'est-ce qu'un bon niveau ?**  
Pertes (%) = (Énergie produite − Énergie vendue) / Énergie produite × 100. Un bon réseau moderne a des pertes < 10%. Les réseaux vétustes (> 30 ans, non rénovés) peuvent atteindre 20–25%, ce qui grève directement la marge.

**Q5 : Pourquoi la corrélation ENR/coût est-elle négative ?**  
Les énergies renouvelables (géothermie, biomasse, solaire) ont un coût d'exploitation plus faible que le gaz naturel car elles ne dépendent pas du marché spot de l'énergie fossile. Une fois l'investissement initial amorti, leur coût marginal est très faible.

---

## 23. Compétences démontrées

- **pandas** — jointures, groupby multicritère, pivot_table
- **sklearn** — LinearRegression, StandardScaler
- **Statistiques** — corrélation de Pearson, normalisation min-max
- **Analyse financière** — marge opérationnelle, prix unitaire, projection
- **Énergie** — ENR, DJU, rendement réseau, pertes thermiques
- **Python OOP** — classes `HeatingAnalyzer`, `HeatingVisualizer`
- **Visualisation** — matplotlib dark theme, 8 figures

---

## 24. Tableau compétences / preuves

| Compétence | Preuve | Fichier |
|-----------|--------|---------|
| Analyse rentabilité | Méthode `rentabilite()` | `src/heating_analyzer.py` |
| Corrélation ENR/coût | Méthode `impact_enr()` | `src/heating_analyzer.py` |
| Score composite | Méthode `score_performance()` | `src/heating_analyzer.py` |
| Régression linéaire | Méthode `projection_recettes()` | `src/heating_analyzer.py` |
| StandardScaler | Normalisation 4 critères | `src/heating_analyzer.py` |
| 8 visualisations | Classe `HeatingVisualizer` | `src/visualization.py` |
| Script complet | 10 sections | `notebooks/01_heating_analysis.py` |
| Domaine énergie | DJU, ENR, pertes réseau | `data_sample/` + README |

---

## 25. Conseils GitHub

**Description :** "Analyse économique de 15 réseaux de chaleur urbains — rentabilité, efficacité ENR, score composite, projection recettes. Portfolio Data Science énergie."

**Topics :** `python` `data-science` `energy` `district-heating` `renewable-energy` `pandas` `scikit-learn` `economic-analysis` `portfolio` `urban-infrastructure`

**Projets connexes :**
| Projet | Lien |
|--------|------|
| Building Energy Analytics | [building-energy-efficiency-analytics](https://github.com/TSAGUE25/building-energy-efficiency-analytics) |
| Customer Segmentation | [customer-marketing-segmentation](https://github.com/TSAGUE25/customer-marketing-segmentation) |
| Bank Churn Prediction | [bank-customer-churn-prediction](https://github.com/TSAGUE25/bank-customer-churn-prediction) |


## Contributors

| Nom | Role | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist - auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*  
*Formation : DataScientest | Domaines : Énergie · Finance · Commerce*  
*Contact : emmoi.mtn@gmail.com*  
*Données : entièrement simulées — aucune donnée réelle ou confidentielle*
