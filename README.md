# When Diversification Fails

**Average correlation rose only modestly in stress, but that average hid opposite moves inside fixed income.** Investment-grade and high-yield credit moved closer together while Treasury–credit correlations fell. For the equal-weight portfolio, both the diversification ratio and the effective number of bets dropped.

## Results from daily ETF returns

November 15, 2016–October 30, 2026. The analysis uses Yahoo Finance adjusted prices for SPY, IEF, TLT, GLD, DBC, LQD, HYG and VNQ as proxies for equities, Treasuries, gold, commodities, credit and real estate.

| Metric | Normal | Stress |
| --- | ---: | ---: |
| Trading days | 1,655 | 848 |
| Average pairwise correlation | 0.264 | 0.307 |
| Diversification ratio | 1.779 | 1.580 |
| Effective number of bets | 6.78 | 6.20 |

| ETF pair | Stress minus normal correlation |
| --- | ---: |
| LQD–HYG | +0.127 |
| IEF–LQD | -0.252 |
| TLT–LQD | -0.277 |
| IEF–HYG | -0.081 |
| TLT–HYG | -0.116 |

All eight ETFs were simultaneously at least 10% below their own running peaks on at least one date. The 2022 inflation and rate shock had an average pairwise correlation of 0.387, versus 0.214 in the COVID shock window. The composition of stress mattered more than any single average.

### What counts as stress

A day is tagged as stress when 63-day trailing equal-weight portfolio volatility is at or above its expanding 80th percentile, or when that portfolio is at least 10% below its running peak. Conditioning on high volatility can bias unadjusted correlations upward, so these are descriptive comparisons, not evidence of structural contagion. See [Forbes and Rigobon](https://www.nber.org/papers/w7267).

The [analysis](src/diversification/analysis.py) also reports lower-tail co-exceedance and drawdown synchronization. It does not estimate GARCH models or copulas.

```bash
pip install -r requirements.txt
PYTHONPATH=src python scripts/run_analysis.py --mode live
```

The command uses the full available sample. For comparison with the dated table, restrict input prices to the same window (including the preceding close for the first return).
