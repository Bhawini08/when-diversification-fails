from __future__ import annotations
import numpy as np
import pandas as pd

def portfolio_returns(returns: pd.DataFrame, weights=None) -> pd.Series:
    if weights is None:
        w = np.repeat(1 / returns.shape[1], returns.shape[1])
    elif isinstance(weights, pd.Series):
        w = weights.reindex(returns.columns).to_numpy(float)
    else:
        w = np.asarray(weights, float)
    w = w / w.sum()
    return pd.Series(returns.to_numpy() @ w, index=returns.index, name="portfolio")

def drawdown(returns: pd.Series) -> pd.Series:
    wealth = (1 + returns.fillna(0)).cumprod()
    return wealth / wealth.cummax() - 1

def rolling_volatility(returns: pd.Series, window=63, annualization=252) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(annualization)

def stress_mask(
    returns: pd.DataFrame,
    vol_window: int = 63,
    vol_quantile: float = 0.80,
    drawdown_threshold: float = -0.10,
) -> pd.Series:
    p = portfolio_returns(returns)
    vol = rolling_volatility(p, vol_window)
    # expanding quantile uses information available through each date
    threshold = vol.expanding(min_periods=max(vol_window, 126)).quantile(vol_quantile)
    dd = drawdown(p)
    mask = (vol >= threshold) | (dd <= drawdown_threshold)
    return mask.fillna(False).rename("stress")

def average_pairwise_correlation(corr: pd.DataFrame) -> float:
    a = corr.to_numpy(float)
    n = len(a)
    return float((a.sum() - np.trace(a)) / (n * (n - 1)))

def conditional_correlation(returns: pd.DataFrame, mask: pd.Series) -> pd.DataFrame:
    x = returns.loc[mask.reindex(returns.index).fillna(False)]
    return x.corr()

def downside_correlation(returns: pd.DataFrame, threshold=0.0) -> pd.DataFrame:
    market = returns.mean(axis=1)
    return returns.loc[market < threshold].corr()

def rolling_average_correlation(returns: pd.DataFrame, window=63) -> pd.Series:
    vals = []
    idx = []
    for i in range(window - 1, len(returns)):
        c = returns.iloc[i-window+1:i+1].corr()
        vals.append(average_pairwise_correlation(c))
        idx.append(returns.index[i])
    return pd.Series(vals, index=idx, name="avg_pairwise_corr")

def diversification_ratio(returns: pd.DataFrame, weights=None, annualization=252) -> float:
    if weights is None:
        w = np.repeat(1 / returns.shape[1], returns.shape[1])
    else:
        w = np.asarray(weights, float)
        w = w / w.sum()
    cov = returns.cov().to_numpy(float) * annualization
    asset_vol = np.sqrt(np.diag(cov))
    port_vol = np.sqrt(w @ cov @ w)
    return float((w @ asset_vol) / port_vol)

def effective_number_of_bets(returns: pd.DataFrame, weights=None) -> float:
    if weights is None:
        w = np.repeat(1 / returns.shape[1], returns.shape[1])
    else:
        w = np.asarray(weights, float)
        w = w / w.sum()
    cov = returns.cov().to_numpy(float)
    marginal = cov @ w
    contrib = w * marginal
    total = contrib.sum()
    if total <= 0:
        return float("nan")
    shares = contrib / total
    return float(1.0 / np.sum(shares ** 2))

def lower_tail_coexceedance(returns: pd.DataFrame, q=0.05) -> pd.DataFrame:
    """Pairwise probability both assets are below their own q-quantile, conditional on one being below."""
    thresholds = returns.quantile(q)
    flags = returns.lt(thresholds, axis=1)
    cols = returns.columns
    out = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols, dtype=float)
    for i, a in enumerate(cols):
        for j, b in enumerate(cols):
            if i == j:
                continue
            denom = flags[a].sum()
            out.loc[a, b] = float((flags[a] & flags[b]).sum() / denom) if denom else np.nan
    return out

def drawdown_synchronization(returns: pd.DataFrame, threshold=-0.10) -> pd.DataFrame:
    dd = pd.DataFrame({c: drawdown(returns[c]) for c in returns.columns})
    in_dd = dd <= threshold
    simultaneous = in_dd.sum(axis=1)
    return pd.DataFrame({
        "assets_in_drawdown": simultaneous,
        "share_assets_in_drawdown": simultaneous / returns.shape[1]
    }, index=returns.index)

def crisis_window_summary(returns: pd.DataFrame, windows: dict[str, tuple[str,str]]) -> pd.DataFrame:
    rows = []
    for name, (start, end) in windows.items():
        x = returns.loc[start:end]
        if len(x) < 5:
            continue
        p = portfolio_returns(x)
        rows.append({
            "window": name,
            "start": str(x.index.min().date()),
            "end": str(x.index.max().date()),
            "observations": len(x),
            "portfolio_return": float((1+p).prod()-1),
            "portfolio_max_drawdown": float(drawdown(p).min()),
            "avg_pairwise_corr": average_pairwise_correlation(x.corr()),
            "diversification_ratio": diversification_ratio(x),
        })
    return pd.DataFrame(rows)
