# District Heating Economic Analysis

> Analyse économique et énergétique de 15 réseaux de chaleur urbains (RCU) : rentabilité, efficacité, impact des ENR, score composite et projection des recettes.
> **Stack :** Python · pandas · scikit-learn · matplotlib · seaborn

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Portfolio](https://img.shields.io/badge/Portfolio-TSAGUE%20Emmanuel-purple)](https://github.com/TSAGUE25)

---

## Table des matières

1. [Contexte métier](#1-contexte-métier)
2. [Problème résolu](#2-problème-résolu)
3. [Données utilisées](#3-données-utilisées)
4. [Méthodes et algorithmes](#4-méthodes-et-algorithmes)
5. [Démarche analytique](#5-démarche-analytique)
6. [Métriques clés](#6-métriques-clés)
7. [Résultats obtenus](#7-résultats-obtenus)
8. [Valeur métier](#8-valeur-métier)
9. [Architecture du projet](#9-architecture-du-projet)
10. [Installation et usage](#10-installation-et-usage)
11. [Compétences démontrées](#11-compétences-démontrées)
12. [Limites et améliorations](#12-limites-et-améliorations)
13. [Contributors](#13-contributors)

---

## 1. Contexte métier

Les réseaux de chaleur urbains (RCU) distribuent de la chaleur à partir d'une production centralisée vers des bâtiments résidentiels, tertiaires et industriels. En France, ils représentent plus de **30 000 km de canalisations**, 750 000 logements équivalents, et une production de **35 TWh/an**.

Avec la transition énergétique, les gestionnaires de RCU doivent simultanément :
- **Optimiser la rentabilité** face à la hausse des coûts de maintenance
- **Augmenter la part d'ENR** pour atteindre les objectifs climatiques (loi Énergie-Climat 2019)
- **Réduire les pertes réseau** qui représentent 10 à 20% de l'énergie produite

---

## 2. Problème résolu

> *"Sur nos 15 réseaux, certains sont rentables et d'autres non. Comment identifier lesquels prioriser en investissement ? Est-ce que passer à plus d'ENR améliore réellement la rentabilité ? Où sont les plus grosses pertes ?"*

Ce projet apporte :
- Un **classement objectif** des réseaux par score composite multicritère
- La **corrélation quantifiée** entre taux d'ENR et réduction des coûts (r = −0.81)
- Une **projection des recettes** à 3 ans par régression linéaire pour alimenter le plan pluriannuel d'investissement
- L'**identification des réseaux déficitaires** nécessitant une intervention prioritaire

| Objectif | Méthode |
|----------|---------|
| Calculer la rentabilité par réseau | Marge = recettes − charges |
| Comparer prix vente vs coût production | Analyse prix unitaire (€/kWh) |
| Mesurer l'efficacité énergétique | Rendement réseau, taux de pertes |
| Quantifier l'impact des ENR | Corrélation + régression |
| Créer un score composite | StandardScaler + pondération |
| Projeter les recettes | Régression linéaire sklearn |

---

## 3. Données utilisées

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

## 4. Méthodes et algorithmes

| Méthode | Usage | Module |
|---------|-------|--------|
| Agrégation pandas (groupby) | Rentabilité par réseau/année | `pandas` |
| Corrélation de Pearson | ENR vs coût, ENR vs marge | `pandas.corr()` |
| Régression linéaire | Projection recettes 2024–2026 | `sklearn.LinearRegression` |
| StandardScaler + pondération | Score composite normalisé | `sklearn.StandardScaler` |
| Min-max normalization | Score sur 0–100 | `numpy` |

---

## 5. Démarche analytique

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

## 6. Métriques clés

| Métrique | Formule | Interprétation |
|----------|---------|----------------|
| Marge nette (%) | (Recettes − Charges) / Recettes | Rentabilité opérationnelle |
| Pertes réseau (%) | Pertes GWh / Production GWh | Efficacité de distribution |
| Coût production (€/kWh) | Charges / Énergie vendue | Compétitivité tarifaire |
| Score composite | Pondération normalisée 4 critères | Classement global |
| R² projection | Coefficient de détermination | Fiabilité des projections |

**Score composite — pondération :** 35% rentabilité · 25% ENR · 25% rendement · 15% taux d'occupation

**Régression linéaire :** adaptée pour 4 points historiques et tendance stable. Pour des projections longues, un modèle ARIMA ou avec DJU comme prédicteur serait préférable.

---

## 7. Résultats obtenus

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
- Réseaux > 85% ENR : coût moyen de **4.3 c€/kWh**
- Réseaux < 20% ENR : coût moyen de **7.4 c€/kWh** (+72%)

### Pertes réseau

| Indicateur | Valeur |
|-----------|--------|
| Moyenne parc | **10.8%** de pertes |
| Meilleur réseau | Réseau ENR Montpellier — **5.8%** |
| Réseau le plus dégradé | Réseau Ancien Bordeaux — **19.8%** (infrastructure vétuste) |

---

## 8. Valeur métier

| Question métier | Donnée fournie par l'analyse |
|----------------|------------------------------|
| Quels réseaux rénover en priorité ? | Score composite + pertes réseau |
| Faut-il convertir les réseaux gaz ? | Corrélation ENR/coût (−0.81) |
| Plan pluriannuel d'investissement | Projection recettes 2024–2026 |
| Revalorisation tarifaire | Évolution coût production vs prix vente |

**Adapté pour :** EDF, Dalkia, ENGIE, Coriance, collectivités territoriales, bureaux d'études énergie.

---

## 9. Architecture du projet

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
│   └── 01_heating_analysis.py  # Pipeline complet 10 sections
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

## 10. Installation et usage

```bash
git clone https://github.com/TSAGUE25/district-heating-economic-analysis
cd district-heating-economic-analysis
pip install -r requirements.txt
python notebooks/01_heating_analysis.py
```

**Utilisation directe des classes :**

```python
import pandas as pd
from src.heating_analyzer import HeatingAnalyzer

networks  = pd.read_csv('data_sample/heating_network.csv')
economics = pd.read_csv('data_sample/annual_economics.csv')

analyzer = HeatingAnalyzer(networks, economics)
print(analyzer.classement_rentabilite())
print(analyzer.score_performance())
print(analyzer.projection_recettes(annees_futures=3))
```

**Sorties produites :**
- `figures/` — 8 visualisations PNG (score composite, corrélation ENR/coût, projection, pertes...)
- `reports/heating_report_sample.md` — rapport Markdown auto-généré

---

## 11. Compétences démontrées

| Compétence | Mise en œuvre | Fichier |
|-----------|--------------|---------|
| **Analyse financière** | Marge opérationnelle, coût unitaire, projection | `src/heating_analyzer.py` |
| **Corrélation de Pearson** | ENR vs coût de production (r = −0.81) | `src/heating_analyzer.py` |
| **Score composite multicritère** | StandardScaler + pondération 4 critères | `src/heating_analyzer.py` |
| **Régression linéaire** | Projection recettes 2024–2026 | `src/heating_analyzer.py` |
| **Python OOP** | Classes `HeatingAnalyzer`, `HeatingVisualizer` | `src/` |
| **Visualisation** | 8 figures matplotlib dark theme | `src/visualization.py` |
| **Domaine énergie** | ENR, DJU, pertes réseau, rendement thermique | `data_sample/` + README |
| **Pipeline complet** | 10 sections EDA → rapport | `notebooks/` |

**Stack technique :** `pandas` · `numpy` · `scikit-learn` (LinearRegression, StandardScaler) · `matplotlib` · `seaborn`

---

## 12. Limites et améliorations

**Limites actuelles :**

| Limite | Impact |
|--------|--------|
| 15 réseaux seulement | Insuffisant pour un modèle statistique robuste |
| Régression linéaire | Ne capture pas les ruptures (hausse gaz 2022) |
| Pas d'amortissement | Marge opérationnelle ≠ rentabilité comptable |
| Données simulées | Paramètres non calés sur des réseaux réels |

**Pistes d'amélioration :**
- **SIG / GeoPandas** : cartographier les réseaux et les pertes par tronçon
- **Modèle ARIMA avec DJU** : projection avec saisonnalité météorologique
- **Simulation scénarios ENR** : impact d'une conversion progressive sur 10 ans
- **Dashboard Streamlit** : interface interactive pour les exploitants

---

## Ce projet démontre

- La capacité à mener une **analyse économique et financière** sur un parc d'actifs énergétiques : marge opérationnelle, coût unitaire, analyse prix/coût
- La **quantification de l'impact des ENR** par corrélation de Pearson (r = −0.81) — argument chiffré pour des décisions d'investissement
- La construction d'un **score composite multicritère** (StandardScaler + pondération 4 dimensions) : outil de classement objectif et actionnable
- La **projection des recettes à 3 ans** par régression linéaire sklearn — directement utilisable pour un plan pluriannuel d'investissement (PPI)
- Un pipeline **adaptable au secteur énergie** (EDF, Dalkia, Engie, collectivités) : changer les CSV suffit pour analyser tout portefeuille de réseaux
- La **maîtrise du vocabulaire domaine** : ENR, DJU, rendement réseau, pertes thermiques, tarif chaleur — crédibilité vis-à-vis des experts métier

---

## 13. Contributors

| Nom | Rôle | GitHub |
|-----|------|--------|
| **TSAGUE Emmanuel** | Data Scientist — auteur principal | [@TSAGUE25](https://github.com/TSAGUE25) |

---

*Auteur : Emmanuel TSAGUE — Data Scientist / Data Analyst*
*Formation : DataScientest | Domaines : Énergie · Finance · Performance opérationnelle*
*Contact : emmatsague@yahoo.fr | [LinkedIn](https://www.linkedin.com/in/emmanuel-tsague-114295414)*
*Données : entièrement simulées — aucune donnée réelle ou confidentielle*
