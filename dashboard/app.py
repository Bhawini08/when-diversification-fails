import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diversification.data import synthetic_returns, live_returns
from diversification.analysis import run_dependence_analysis

st.set_page_config(page_title="When Diversification Fails", layout="wide")
st.title("When Diversification Fails")
st.caption("Cross-asset dependence, stress correlation, tail co-movement, and diversification fragility.")

mode = st.sidebar.selectbox("Data", ["synthetic", "live"])
returns = synthetic_returns() if mode == "synthetic" else live_returns()
res = run_dependence_analysis(returns)
summary = res["summary"].set_index("regime")

c1, c2, c3 = st.columns(3)
c1.metric("Normal avg correlation", f"{summary.loc['normal','avg_pairwise_corr']:.2f}")
c2.metric("Stress avg correlation", f"{summary.loc['stress','avg_pairwise_corr']:.2f}")
c3.metric("Stress diversification ratio", f"{summary.loc['stress','diversification_ratio']:.2f}")

tabs = st.tabs(["Regimes", "Correlation", "Drawdown synchronization", "Tail dependence", "Crisis windows"])

with tabs[0]:
    st.dataframe(res["summary"], use_container_width=True)
    st.line_chart(res["rolling_avg_corr"])

with tabs[1]:
    left, right = st.columns(2)
    left.subheader("Normal correlation")
    left.dataframe(res["normal_corr"].round(2), use_container_width=True)
    right.subheader("Stress correlation")
    right.dataframe(res["stress_corr"].round(2), use_container_width=True)

with tabs[2]:
    st.line_chart(res["drawdown_sync"]["share_assets_in_drawdown"])
    st.caption("Share of assets simultaneously in drawdowns deeper than 10%.")

with tabs[3]:
    st.dataframe(res["tail_coexceedance"].round(2), use_container_width=True)

with tabs[4]:
    st.dataframe(res["crisis_windows"], use_container_width=True)
