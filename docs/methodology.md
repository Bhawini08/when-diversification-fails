# Methodology

## Research objective

Traditional diversification analysis often relies on one full-sample covariance matrix. This project tests whether that average relationship is representative of the states in which diversification matters most.

## Stress definition

The default state classifier uses an equal-weight cross-asset portfolio.

A date is classified as stressed if either:

- trailing 63-day annualized volatility exceeds the expanding 80th percentile of volatility observed up to that date, or
- the equal-weight portfolio is in a drawdown of at least 10%.

The volatility threshold is expanding rather than full-sample, which avoids using future information to label earlier observations.

## Dependence measures

### Average pairwise correlation

The mean of all off-diagonal elements of the cross-asset correlation matrix.

### Downside correlation

Correlation estimated only on days when the equal-weight cross-asset portfolio return is negative.

### Lower-tail co-exceedance

For each pair of assets, the framework estimates the conditional frequency with which asset B is below its own 5th-percentile return when asset A is below its own 5th-percentile return.

This is not a full copula-based tail-dependence estimator. It is a transparent empirical stress diagnostic.

### Drawdown synchronization

Each asset is classified as being in a deep drawdown when its cumulative drawdown is at least 10%. The framework then measures how many assets are in deep drawdown simultaneously.

## Diversification diagnostics

### Diversification ratio

Weighted average standalone volatility divided by portfolio volatility.

A decline in the diversification ratio during stress indicates that standalone risks are becoming less diversifying at the portfolio level.

### Effective number of bets

Risk contributions are converted into concentration shares and summarized using an inverse-Herfindahl measure. This makes it possible to compare nominal asset count with effective risk diversification.

## Crisis windows

The live analysis reports dedicated summaries for:

- Global Financial Crisis
- COVID shock
- 2022 inflation / rate shock

These windows are descriptive case studies and do not enter the stress classifier.

## Limitations

ETF proxies have inception-date differences, structural exposures change through time, and correlation is not a complete description of dependence. The project therefore reports multiple complementary diagnostics rather than treating any single statistic as definitive.
