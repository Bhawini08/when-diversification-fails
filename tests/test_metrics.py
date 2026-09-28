import numpy as np
import pandas as pd

from diversification.data import synthetic_returns
from diversification.metrics import (
    stress_mask, average_pairwise_correlation, diversification_ratio,
    effective_number_of_bets, lower_tail_coexceedance, drawdown_synchronization,
)
from diversification.analysis import run_dependence_analysis

def test_synthetic_stress_has_higher_average_correlation():
    r = synthetic_returns(1800, seed=42)
    out = run_dependence_analysis(r)
    s = out["summary"].set_index("regime")
    assert s.loc["stress","avg_pairwise_corr"] > s.loc["normal","avg_pairwise_corr"]

def test_diversification_metrics_are_finite():
    r = synthetic_returns(800, seed=1)
    dr = diversification_ratio(r)
    eb = effective_number_of_bets(r)
    assert np.isfinite(dr) and dr > 0
    assert np.isfinite(eb) and eb > 0

def test_tail_matrix_and_drawdown_sync_shapes():
    r = synthetic_returns(600, seed=3)
    tail = lower_tail_coexceedance(r)
    sync = drawdown_synchronization(r)
    assert tail.shape == (r.shape[1], r.shape[1])
    assert ((tail.values >= 0) & (tail.values <= 1)).all()
    assert sync["share_assets_in_drawdown"].between(0,1).all()

def test_stress_mask_is_nontrivial():
    r = synthetic_returns(1000, seed=5)
    m = stress_mask(r)
    assert 0 < m.mean() < 1
