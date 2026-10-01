# When Diversification Fails

A cross-asset risk research project examining how diversification changes during market stress.

The central question is not whether assets are diversified on average. It is whether the relationships that justify diversification remain intact when losses accelerate, volatility rises, and drawdowns become synchronized.

## Research questions

- Do cross-asset correlations rise during stressed markets?
- Which relationships deteriorate most in downside states?
- How often do major asset classes experience simultaneous drawdowns?
- Does a portfolio that looks diversified in normal markets become concentrated in stress?
- Which metrics detect diversification fragility earlier than a static correlation matrix?

## Asset universe

The default live universe uses liquid U.S.-listed ETFs as transparent proxies for broad asset classes:

- SPY: U.S. equities
- IEF: intermediate U.S. Treasuries
- TLT: long-duration U.S. Treasuries
- GLD: gold
- DBC: broad commodities
- LQD: investment-grade credit
- HYG: high-yield credit
- VNQ: U.S. REITs

## Analytics

- full-sample and rolling correlation
- downside correlation
- stress versus normal-state correlation
- lower-tail co-exceedance
- synchronized drawdown frequency
- average pairwise correlation
- diversification ratio
- effective number of bets
- volatility-regime classification
- portfolio fragility diagnostics
- crisis-window summaries

## Methodology

Stress is identified using only contemporaneous or trailing information. The default market-state classifier combines trailing portfolio volatility and portfolio drawdown. A date is classified as stressed when trailing volatility is above its historical threshold or the portfolio is in a sufficiently deep drawdown.

Downside dependence is measured separately from unconditional dependence so benign periods do not dilute the relationships that matter during losses.

The project deliberately distinguishes descriptive stress diagnostics from predictive claims. It asks whether diversification has historically weakened in stress, not whether a specific crisis can be forecast.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

pytest -q
python scripts/run_analysis.py --mode synthetic
python scripts/run_analysis.py --mode live

streamlit run dashboard/app.py
```

Outputs are written to `results/`.

## Research discipline

The live analysis uses market data only for empirical validation. Synthetic mode exists so tests and CI remain deterministic and reproducible.

## What the repository produces

The analysis writes regime summaries, full/normal/stress/downside correlation matrices, lower-tail co-exceedance, synchronized drawdowns, rolling average correlation, crisis-window diagnostics, and a compact metrics JSON to `results/`. The generated directory is intentionally excluded from version control so empirical outputs can be regenerated from the current data rather than presented as permanently current.

## Validation

The test suite checks the stress classifier, dependence metrics, diversification diagnostics, and deterministic synthetic research path. GitHub Actions installs the environment, runs `pytest`, and executes the synthetic analysis on every push and pull request.

## Limitations

ETF proxies are investable approximations rather than pure asset-class indexes. Inception dates differ, exposures evolve through time, and correlation alone does not describe joint downside risk. The framework therefore combines several diagnostics and treats crisis windows as descriptive evidence rather than forecasts.

