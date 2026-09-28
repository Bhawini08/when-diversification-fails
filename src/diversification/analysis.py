from __future__ import annotations
import pandas as pd
from .metrics import (
    portfolio_returns, stress_mask, conditional_correlation,
    downside_correlation, average_pairwise_correlation,
    rolling_average_correlation, diversification_ratio,
    effective_number_of_bets, lower_tail_coexceedance,
    drawdown_synchronization, crisis_window_summary,
)

CRISIS_WINDOWS = {
    "Global Financial Crisis": ("2008-09-01", "2009-03-31"),
    "COVID Shock": ("2020-02-19", "2020-04-30"),
    "2022 Inflation / Rate Shock": ("2022-01-03", "2022-10-31"),
}

def run_dependence_analysis(returns: pd.DataFrame):
    stress = stress_mask(returns)
    normal = ~stress

    full_corr = returns.corr()
    stress_corr = conditional_correlation(returns, stress)
    normal_corr = conditional_correlation(returns, normal)
    downside_corr = downside_correlation(returns, 0.0)

    summary = pd.DataFrame([
        {
            "regime": "full_sample",
            "observations": len(returns),
            "avg_pairwise_corr": average_pairwise_correlation(full_corr),
            "diversification_ratio": diversification_ratio(returns),
            "effective_bets": effective_number_of_bets(returns),
        },
        {
            "regime": "normal",
            "observations": int(normal.sum()),
            "avg_pairwise_corr": average_pairwise_correlation(normal_corr),
            "diversification_ratio": diversification_ratio(returns.loc[normal]),
            "effective_bets": effective_number_of_bets(returns.loc[normal]),
        },
        {
            "regime": "stress",
            "observations": int(stress.sum()),
            "avg_pairwise_corr": average_pairwise_correlation(stress_corr),
            "diversification_ratio": diversification_ratio(returns.loc[stress]),
            "effective_bets": effective_number_of_bets(returns.loc[stress]),
        },
    ])

    sync = drawdown_synchronization(returns)
    portfolio = portfolio_returns(returns)
    rolling_corr = rolling_average_correlation(returns)

    return {
        "summary": summary,
        "full_corr": full_corr,
        "normal_corr": normal_corr,
        "stress_corr": stress_corr,
        "downside_corr": downside_corr,
        "tail_coexceedance": lower_tail_coexceedance(returns),
        "stress_mask": stress,
        "drawdown_sync": sync,
        "portfolio_returns": portfolio,
        "rolling_avg_corr": rolling_corr,
        "crisis_windows": crisis_window_summary(returns, CRISIS_WINDOWS),
    }
