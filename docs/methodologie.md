# Méthodologie — District Heating Economic Analysis

## 1. Calcul de la marge opérationnelle

Marge (€) = Recettes − Charges d'exploitation  
Marge (%) = Marge € / Recettes × 100

Les charges incluent : coût de production de chaleur, maintenance réseau, personnel, frais généraux.  
Les subventions sont comptabilisées séparément pour isoler la rentabilité intrinsèque.

## 2. Corrélation ENR / coût de production

Méthode : corrélation de Pearson entre `energie_renouvelable_pct` et `cout_production_kwh`.  
Interprétation :
- r > 0.7 : forte corrélation positive
- r < −0.7 : forte corrélation inverse (ENR élevé → coût faible)

## 3. Score composite multicritère

Étapes :
1. Calculer 4 indicateurs par réseau : marge_pct, enr_pct, rendement_pct, taux_occupation
2. Normaliser avec `StandardScaler` (μ=0, σ=1)
3. Appliquer les pondérations : 35% rentabilité, 25% ENR, 25% rendement, 15% occupation
4. Normaliser le résultat sur 0–100 (min-max)

Les pondérations reflètent les priorités d'un exploitant de réseau en contexte de transition énergétique.

## 4. Projection linéaire des recettes

Pour chaque réseau, ajustement d'une droite `recettes = a × année + b` avec `sklearn.LinearRegression`.  
Hypothèse : tendance stable, pas de rupture tarifaire majeure.  
Limite : ne capture pas la volatilité des prix de l'énergie ni les DJU annuels.

## 5. Pertes réseau

Pertes (%) = (Énergie produite − Énergie vendue) / Énergie produite × 100  
Seuil d'alerte : > 10%  
Cause principale : isolation insuffisante des canalisations (réseaux anciens pré-1985).
