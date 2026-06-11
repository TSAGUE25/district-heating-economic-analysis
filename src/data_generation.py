import numpy as np
import pandas as pd
from pathlib import Path


def generate_district_heating_data(n_networks=30, seed=42):
    rng = np.random.default_rng(seed)

    types = ['residentiel', 'mixte', 'tertiaire', 'industriel']
    sources = ['biomasse', 'geothermie', 'recuperation_chaleur', 'gaz_naturel', 'electricite']
    villes = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Nantes', 'Lille',
              'Strasbourg', 'Grenoble', 'Montpellier', 'Rennes']

    # Network parameters
    longueur_km = np.clip(rng.lognormal(2.5, 0.7, n_networks), 2, 80).round(1)
    nb_abonnes  = (longueur_km * rng.uniform(20, 80, n_networks)).astype(int)
    puissance_mw = np.clip(longueur_km * rng.uniform(1.5, 4, n_networks), 5, 200).round(1)

    source = rng.choice(sources, n_networks, p=[0.30, 0.20, 0.25, 0.15, 0.10])

    # Investment & costs
    capex_km = rng.uniform(800, 2000, n_networks)  # k€/km
    capex_total = (longueur_km * capex_km).round(0)
    opex_annuel_pct = rng.uniform(1.5, 3.5, n_networks) / 100

    # Revenue
    chaleur_prod_gwh = (puissance_mw * rng.uniform(3000, 5500, n_networks) / 1000).round(2)
    prix_chaleur = rng.uniform(55, 110, n_networks)  # €/MWh
    revenue_annuel = (chaleur_prod_gwh * 1000 * prix_chaleur / 1e6).round(3)  # M€

    # Economic metrics
    opex_annuel = (capex_total * opex_annuel_pct / 1000).round(3)  # M€
    ebitda = (revenue_annuel - opex_annuel).round(3)

    # NPV over 25 years at 5% discount rate
    discount_rate = 0.05
    npv = np.array([
        sum(ebitda[i] / (1 + discount_rate) ** t for t in range(1, 26)) - capex_total[i] / 1000
        for i in range(n_networks)
    ]).round(2)

    # Simple payback
    payback = np.where(ebitda > 0,
                       np.clip(capex_total / 1000 / ebitda, 1, 50),
                       np.inf).round(1)

    # IRR approximation
    irr = np.where(npv > 0,
                   (ebitda / (capex_total / 1000) - discount_rate) * 100 + rng.normal(0, 0.5, n_networks),
                   rng.uniform(0, 3, n_networks))
    irr = np.clip(irr, 0, 25).round(2)

    # ENR rate
    enr_map = {'biomasse': 95, 'geothermie': 100, 'recuperation_chaleur': 80,
               'gaz_naturel': 5, 'electricite': 30}
    taux_enr = np.array([enr_map[s] + rng.uniform(-5, 5) for s in source]).clip(0, 100).round(1)

    # CO2 savings
    co2_ref   = chaleur_prod_gwh * 1000 * 0.230  # tCO2 (gas reference)
    co2_reel  = np.where(
        source == 'gaz_naturel', chaleur_prod_gwh * 1000 * 0.200,
        chaleur_prod_gwh * 1000 * rng.uniform(0.01, 0.06, n_networks)
    ).round(0)
    co2_evite = (co2_ref - co2_reel).round(0)

    return pd.DataFrame({
        'reseau_id':          range(1, n_networks + 1),
        'ville':              rng.choice(villes, n_networks),
        'type_reseau':        rng.choice(types, n_networks, p=[0.45, 0.30, 0.15, 0.10]),
        'source_energie':     source,
        'longueur_km':        longueur_km,
        'nb_abonnes':         nb_abonnes,
        'puissance_mw':       puissance_mw,
        'chaleur_prod_gwh':   chaleur_prod_gwh,
        'capex_total_keur':   capex_total.astype(int),
        'opex_annuel_meur':   opex_annuel,
        'revenue_annuel_meur':revenue_annuel,
        'ebitda_meur':        ebitda,
        'prix_chaleur_mwh':   prix_chaleur.round(2),
        'npv_meur_25ans':     npv,
        'irr_pct':            irr,
        'payback_ans':        payback,
        'taux_enr_pct':       taux_enr,
        'co2_evite_t':        co2_evite.astype(int),
    })


def load_or_generate(csv_path, **kwargs):
    path = Path(csv_path)
    if path.exists():
        return pd.read_csv(path)
    df = generate_district_heating_data(**kwargs)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df
