import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def npv(cash_flows, discount_rate=0.05, capex=0):
    """Net present value of a series of annual cash flows."""
    return sum(cf / (1 + discount_rate) ** (t + 1)
               for t, cf in enumerate(cash_flows)) - capex


def irr(cash_flows, capex, tol=1e-6, max_iter=200):
    """Approximate IRR with Newton-Raphson."""
    r = 0.10
    for _ in range(max_iter):
        f  = sum(cf / (1 + r) ** (t + 1) for t, cf in enumerate(cash_flows)) - capex
        fp = sum(-(t + 1) * cf / (1 + r) ** (t + 2) for t, cf in enumerate(cash_flows))
        if abs(fp) < 1e-12:
            break
        r_new = r - f / fp
        if abs(r_new - r) < tol:
            return r_new
        r = r_new
    return r


def payback_period(annual_ebitda, capex):
    """Simple payback in years."""
    if annual_ebitda <= 0:
        return np.inf
    return capex / annual_ebitda


def project_cash_flows(revenue, opex, capex, years=25, residual_value=0.10):
    """Return list of annual free cash flows."""
    flows = [revenue - opex] * years
    flows[-1] += capex * residual_value
    return flows


def rank_projects(df):
    scored = df.copy()
    # Score: NPV > 0, IRR > 6%, payback < 20 years, ENR > 50%
    scored['viable'] = (
        (scored['npv_meur_25ans'] > 0) &
        (scored['irr_pct'] > 6) &
        (scored['payback_ans'] < 20) &
        (scored['taux_enr_pct'] > 50)
    )
    scored['score'] = (
        scored['npv_meur_25ans'].rank(pct=True) * 0.30
        + scored['irr_pct'].rank(pct=True) * 0.25
        + (-scored['payback_ans']).rank(pct=True) * 0.20
        + scored['taux_enr_pct'].rank(pct=True) * 0.15
        + scored['co2_evite_t'].rank(pct=True) * 0.10
    ).round(3)
    return scored.sort_values('score', ascending=False)


def plot_portfolio_analysis(df):
    ranked = rank_projects(df)

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))

    # 1. NPV vs IRR bubble
    colors = ['#4CAF50' if v else '#F44336' for v in ranked['viable']]
    size = (ranked['capex_total_keur'] / ranked['capex_total_keur'].max() * 400).clip(30)
    axes[0, 0].scatter(ranked['irr_pct'], ranked['npv_meur_25ans'],
                       c=colors, s=size, alpha=0.7, edgecolors='white')
    axes[0, 0].axhline(0, color='red', ls='--', lw=1)
    axes[0, 0].axvline(6, color='orange', ls='--', lw=1)
    axes[0, 0].set_xlabel('TRI (%)'); axes[0, 0].set_ylabel('VAN 25 ans (M€)')
    axes[0, 0].set_title('Matrice VAN / TRI (taille = CAPEX)')

    # 2. Payback distribution
    axes[0, 1].hist(ranked['payback_ans'].replace(np.inf, 50), bins=15,
                    color='#2196F3', edgecolor='white')
    axes[0, 1].axvline(20, color='red', ls='--', lw=1.5, label='Seuil 20 ans')
    axes[0, 1].set_title('Distribution temps de retour (ans)'); axes[0, 1].legend()

    # 3. ENR rate by source
    enr_src = ranked.groupby('source_energie')['taux_enr_pct'].mean().sort_values(ascending=False)
    axes[0, 2].barh(enr_src.index, enr_src.values, color='#4CAF50', edgecolor='white')
    axes[0, 2].set_title('Taux ENR moyen par source (%)'); axes[0, 2].axvline(50, color='red', ls='--')

    # 4. CO2 savings by source
    co2_src = ranked.groupby('source_energie')['co2_evite_t'].sum() / 1000
    axes[1, 0].bar(co2_src.index, co2_src.values, color='#00BCD4', edgecolor='white')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].set_title('CO₂ évité par source (kt)')

    # 5. Portfolio cumulative NPV by score rank
    top_n = ranked.head(10)
    axes[1, 1].barh(top_n['ville'] + ' ' + top_n['source_energie'],
                    top_n['npv_meur_25ans'], color=['#4CAF50' if v else '#FF9800'
                                                    for v in top_n['viable']])
    axes[1, 1].set_title('Top 10 projets — VAN (M€)')

    # 6. CAPEX vs Revenue scatter
    axes[1, 2].scatter(ranked['capex_total_keur'] / 1000,
                       ranked['revenue_annuel_meur'],
                       c=['#4CAF50' if v else '#F44336' for v in ranked['viable']],
                       alpha=0.7, edgecolors='white')
    axes[1, 2].set_xlabel('CAPEX (M€)'); axes[1, 2].set_ylabel('Revenue annuel (M€)')
    axes[1, 2].set_title('CAPEX vs Revenue')

    plt.suptitle('Analyse économique — Réseaux de Chaleur', fontweight='bold', fontsize=13)
    plt.tight_layout(); plt.show()
    return ranked
