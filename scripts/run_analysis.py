import argparse
import json
from pathlib import Path

from diversification.data import synthetic_returns, live_returns
from diversification.analysis import run_dependence_analysis

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["synthetic", "live"], default="synthetic")
args = parser.parse_args()

returns = synthetic_returns() if args.mode == "synthetic" else live_returns()
res = run_dependence_analysis(returns)

out = Path("results")
out.mkdir(exist_ok=True)

res["summary"].to_csv(out / f"{args.mode}_regime_summary.csv", index=False)
res["full_corr"].to_csv(out / f"{args.mode}_full_correlation.csv")
res["normal_corr"].to_csv(out / f"{args.mode}_normal_correlation.csv")
res["stress_corr"].to_csv(out / f"{args.mode}_stress_correlation.csv")
res["downside_corr"].to_csv(out / f"{args.mode}_downside_correlation.csv")
res["tail_coexceedance"].to_csv(out / f"{args.mode}_tail_coexceedance.csv")
res["drawdown_sync"].to_csv(out / f"{args.mode}_drawdown_synchronization.csv")
res["rolling_avg_corr"].to_csv(out / f"{args.mode}_rolling_average_correlation.csv")
res["crisis_windows"].to_csv(out / f"{args.mode}_crisis_windows.csv", index=False)

stress_share = float(res["stress_mask"].mean())
normal_corr = float(res["summary"].loc[res["summary"].regime=="normal","avg_pairwise_corr"].iloc[0])
stress_corr = float(res["summary"].loc[res["summary"].regime=="stress","avg_pairwise_corr"].iloc[0])
normal_dr = float(res["summary"].loc[res["summary"].regime=="normal","diversification_ratio"].iloc[0])
stress_dr = float(res["summary"].loc[res["summary"].regime=="stress","diversification_ratio"].iloc[0])

metrics = {
    "mode": args.mode,
    "observations": int(len(returns)),
    "stress_share": stress_share,
    "normal_avg_pairwise_corr": normal_corr,
    "stress_avg_pairwise_corr": stress_corr,
    "correlation_jump": stress_corr - normal_corr,
    "normal_diversification_ratio": normal_dr,
    "stress_diversification_ratio": stress_dr,
    "diversification_ratio_change": stress_dr - normal_dr,
    "max_share_assets_in_drawdown": float(res["drawdown_sync"]["share_assets_in_drawdown"].max()),
}
(out / f"{args.mode}_metrics.json").write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
