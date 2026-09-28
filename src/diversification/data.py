from __future__ import annotations
import numpy as np
import pandas as pd

ASSETS = ["SPY", "IEF", "TLT", "GLD", "DBC", "LQD", "HYG", "VNQ"]

def synthetic_returns(n: int = 1800, seed: int = 42) -> pd.DataFrame:
    """Generate deterministic multi-asset returns with explicit stress regimes."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2018-01-02", periods=n)
    stress = np.zeros(n, dtype=bool)
    for start, length in [(330, 70), (760, 55), (1180, 90), (1510, 65)]:
        stress[start:start+length] = True

    names = ASSETS
    k = len(names)
    r = np.zeros((n, k))

    normal_corr = np.array([
        [1,.05,-.05,.00,.15,.35,.55,.55],
        [.05,1,.78,.10,-.05,.45,.05,-.05],
        [-.05,.78,1,.15,-.10,.30,-.05,-.10],
        [.00,.10,.15,1,.20,.10,.00,.05],
        [.15,-.05,-.10,.20,1,.05,.10,.20],
        [.35,.45,.30,.10,.05,1,.55,.25],
        [.55,.05,-.05,.00,.10,.55,1,.45],
        [.55,-.05,-.10,.05,.20,.25,.45,1],
    ])
    stress_corr = np.array([
        [1,-.20,-.35,.05,.45,.70,.85,.82],
        [-.20,1,.88,.20,-.20,.10,-.25,-.30],
        [-.35,.88,1,.25,-.25,.00,-.35,-.38],
        [.05,.20,.25,1,.25,.15,.05,.05],
        [.45,-.20,-.25,.25,1,.40,.50,.55],
        [.70,.10,.00,.15,.40,1,.78,.65],
        [.85,-.25,-.35,.05,.50,.78,1,.80],
        [.82,-.30,-.38,.05,.55,.65,.80,1],
    ])

    normal_vol = np.array([.010,.0045,.007,.008,.010,.005,.007,.011])
    stress_vol = normal_vol * np.array([2.5,1.6,1.8,1.8,2.0,2.2,2.8,2.4])
    normal_mu = np.array([.00035,.00012,.00012,.00012,.00015,.00018,.00022,.00028])
    stress_mu = np.array([-.0018,.00045,.00055,.00015,-.0010,-.0007,-.0016,-.0017])

    for t in range(n):
        corr = stress_corr if stress[t] else normal_corr
        vol = stress_vol if stress[t] else normal_vol
        mu = stress_mu if stress[t] else normal_mu
        cov = np.outer(vol, vol) * corr
        r[t] = rng.multivariate_normal(mu, cov)

    return pd.DataFrame(r, index=idx, columns=names)

def live_returns(tickers=None, start="2007-01-01", end=None) -> pd.DataFrame:
    import yfinance as yf
    tickers = tickers or ASSETS
    raw = yf.download(
        tickers, start=start, end=end, auto_adjust=True,
        progress=False, threads=False
    )
    if raw.empty:
        raise RuntimeError("Yahoo Finance returned no data")
    if isinstance(raw.columns, pd.MultiIndex):
        px = raw["Close"] if "Close" in raw.columns.get_level_values(0) else raw.xs("Close", axis=1, level=1)
    else:
        px = raw[["Close"]].copy()
        px.columns = [tickers[0]]
    px.columns = [str(c).upper() for c in px.columns]
    return px.pct_change(fill_method=None).dropna(how="any")
