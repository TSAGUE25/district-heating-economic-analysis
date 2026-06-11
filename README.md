# Analyse Économique d'un Réseau de Chaleur Urbain

> **Prioriser les raccordements rentables pour maximiser la valeur économique**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Domaine](https://img.shields.io/badge/Domaine-Énergie-green)
![Statut](https://img.shields.io/badge/Statut-Portfolio-orange)
![Données](https://img.shields.io/badge/Données-Simulées%2FAnonymisées-lightgrey)

---

## Contexte métier

Les réseaux de chaleur urbains doivent prioriser les raccordements de nouveaux clients en tenant compte des contraintes budgétaires. Chaque projet a un profil économique différent (investissement, revenus, durée d'amortissement).

---

## Problème traité

Calculer la rentabilité (VAN, TRI, Payback) de chaque projet de raccordement et optimiser le portefeuille sous contrainte budgétaire pour maximiser la valeur économique totale.

---

## Solution proposée

Calcul VAN par actualisation des flux sur 20 ans, TRI par bissection numérique, algorithme greedy d'optimisation du portefeuille sous contrainte budgétaire, comparaison de 4 scénarios d'investissement.

---

## Technologies utilisées

| Outil | Usage |
|-------|-------|
| Python 3.10+ | Langage principal |
| pandas / numpy | Manipulation des données |
| scikit-learn | Machine Learning & preprocessing |
| matplotlib / seaborn | Visualisation |
| Jupyter Notebook | Exploration interactive |

> Voir `requirements.txt` pour la liste complète.

---

## Structure du projet

```
district-heating-economic-analysis/
├── README.md              ← Ce fichier
├── PORTFOLIO.md           ← Documentation complète du cas d'usage
├── .gitignore
├── requirements.txt
├── notebooks/             ← Jupyter Notebooks d'exploration
├── src/                   ← Code Python modulaire
├── data_sample/           ← Données simulées (anonymisées)
├── figures/               ← Graphiques et visualisations
├── reports/               ← Rapports et synthèses
└── docs/                  ← Documentation complémentaire
```

---

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/TSAGUE25/district-heating-economic-analysis.git
cd district-heating-economic-analysis

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer Jupyter
jupyter notebook
```

---

## Métriques clés (données simulées)

```
VAN (€), TRI (%), Payback (ans), VAN totale du portefeuille
```

---

## Valeur métier

Optimisation du retour sur investissement. Aide à la décision pour les collectivités.

---

## Limites

Taux d'actualisation fixe. Pas de simulation Monte Carlo des incertitudes.

---

## Prochaines améliorations

Simulation Monte Carlo. Optimisation par programmation linéaire. Carte géographique.

---

## Avertissement — Confidentialité

> **Toutes les données utilisées dans ce projet sont simulées, synthétiques ou anonymisées.**
> Aucune donnée réelle, confidentielle ou propriétaire n'est présente dans ce dépôt.
> Ce projet est un cas d'usage pédagogique à destination du portfolio professionnel d'Emmanuel TSAGUE.

---

## Contributors

**TSAGUE EMMANUEL** - Data Scientist  
Specialise en Machine Learning, Data Analysis et systemes decisionnels.  
Formation Datascientest 2024 | EDF MAD EDVANCE  
Email : [emmatsague@yahoo.fr](mailto:emmatsague@yahoo.fr)  
GitHub : [github.com/TSAGUE25](https://github.com/TSAGUE25)

