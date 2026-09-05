"""Streamlit user interface for NVIDIA AI Factory Guardian."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow `streamlit run src/app.py` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import analyze
from audit import append_event
from models import AuditEvent
from nvidia_client import is_configured
from simulator import FactorySimulator


st.set_page_config(
    page_title="AI Factory Guardian",
    page_icon="🟢",
    layout="wide",
)


CUSTOM_CSS = """
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stMetricValue"] {font-size: 1.9rem;}
.guardian-kicker {font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; color: #76B900; font-weight: 700;}
.guardian-title {font-size: 2.55rem; font-weight: 750; margin-top: 0.15rem; margin-bottom: 0.2rem;}
.guardian-subtitle {font-size: 1.05rem; color: #8c8c8c; margin-bottom: 1.2rem;}
.status-low {padding: 0.35rem 0.7rem; border-radius: 999px; background: rgba(118,185,0,0.16); display: inline-block; font-weight: 700;}
.status-medium {padding: 0.35rem 0.7rem; border-radius: 999px; background: rgba(255,170,0,0.16); display: inline-block; font-weight: 700;}
.status-high {padding: 0.35rem 0.7rem; border-radius: 999px; background: rgba(255,70,70,0.16); display: inline-block; font-weight: 700;}
.small-note {font-size: 0.82rem; color: #8c8c8c;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def ensure_state() -> None:
    if "scenario" not in st.session_state:
        st.session_state.scenario = FactorySimulator.BASELINE
    if "audit" not in st.session_state:
        st.session_state.audit = []
    if "approved" not in st.session_state:
        st.session_state.approved = set()


def inject(scenario: str) -> None:
    st.session_state.scenario = scenario
    st.session_state.approved = set()
    st.session_state.audit = append_event(
        st.session_state.audit,
        "SCENARIO",
        f"Scenario selected: {scenario}",
        actor="demo-operator",
    )


def risk_badge(risk: str) -> str:
    cls = {"LOW": "status-low", "MEDIUM": "status-medium", "HIGH": "status-high"}[risk]
    return f'<span class="{cls}">{risk} SLO RISK</span>'


ensure_state()
simulator = FactorySimulator()

st.markdown('<div class="guardian-kicker">Portfolio Proof of Concept</div>', unsafe_allow_html=True)
st.markdown('<div class="guardian-title">NVIDIA AI Factory Guardian</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="guardian-subtitle">Agentic SRE + Token Economics for AI Factories · GPU-free simulation · deterministic guardrails</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Demo controls")
    st.caption("Inject a synthetic production condition.")
    if st.button("✅ Reset to baseline", use_container_width=True):
        inject(FactorySimulator.BASELINE)
    if st.button("🔥 Inject GPU node failure", use_container_width=True):
        inject(FactorySimulator.GPU_FAILURE)
    if st.button("📈 Inject 3× traffic spike", use_container_width=True):
        inject(FactorySimulator.TRAFFIC_SPIKE)
    if st.button("⚡ Inject power constraint", use_container_width=True):
        inject(FactorySimulator.POWER_CONSTRAINT)

    st.divider()
    model_available = is_configured()
    use_model = st.toggle(
        "Use NVIDIA-hosted model summary",
        value=False,
        disabled=not model_available,
        help="Optional. The deterministic analysis works without an API key.",
    )
    if model_available:
        st.success("NVIDIA API key detected")
    else:
        st.info("No NVIDIA API key detected — deterministic mode active")

state = simulator.state(st.session_state.scenario)
result = analyze(state, use_model=use_model)

# Header status
status_left, status_right = st.columns([4, 1])
with status_left:
    st.subheader(state.scenario)
    st.write(state.incident_note)
with status_right:
    st.markdown(risk_badge(state.sla_risk.value), unsafe_allow_html=True)

# Factory metrics
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("GPU utilization", f"{state.average_gpu_utilization_pct:.0f}%")
m2.metric("TTFT", f"{state.weighted_ttft_ms:.0f} ms")
m3.metric("Queue depth", f"{state.total_queue_depth:,}")
m4.metric("Tokens / sec", f"{state.total_tokens_per_second/1_000_000:.2f}M")
m5.metric("Cost / 1M tokens", f"${state.cost_per_million_tokens_usd:.2f}")
m6.metric("Power", f"{state.average_power_utilization_pct:.0f}%")

st.divider()

# Cluster evidence
st.subheader("1 · Observe")
cluster_df = pd.DataFrame(
    [
        {
            "Cluster": c.name,
            "GPU eq.": c.gpu_equivalents,
            "GPU util %": c.gpu_utilization_pct,
            "Queue": c.queue_depth,
            "TTFT ms": c.ttft_ms,
            "Tokens/s": c.tokens_per_second,
            "Power %": c.power_utilization_pct,
            "Errors %": c.error_rate_pct,
            "Healthy nodes": f"{c.healthy_nodes}/{c.total_nodes}",
        }
        for c in state.clusters
    ]
)
st.dataframe(cluster_df, use_container_width=True, hide_index=True)

st.subheader("2 · Reason")
left, right = st.columns([2, 1])
with left:
    st.markdown(f"**Probable cause ({result.confidence_pct}% confidence)**")
    st.write(result.probable_cause)
    st.markdown("**Deterministic operations summary**")
    st.info(result.deterministic_summary)
    if result.model_summary:
        st.markdown("**Optional NVIDIA model explanation**")
        st.success(result.model_summary)
with right:
    predicted = pd.DataFrame(
        {
            "Metric": ["TTFT", "GPU utilization", "Tokens/s", "Cost / 1M tokens"],
            "Current": [
                f"{state.weighted_ttft_ms:.0f} ms",
                f"{state.average_gpu_utilization_pct:.0f}%",
                f"{state.total_tokens_per_second:,}",
                f"${state.cost_per_million_tokens_usd:.2f}",
            ],
            "After plan": [
                f"{result.predicted_ttft_ms:.0f} ms",
                f"{result.predicted_gpu_utilization_pct:.0f}%",
                f"{result.predicted_tokens_per_second:,}",
                f"${result.predicted_cost_per_million_tokens_usd:.2f}",
            ],
        }
    )
    st.dataframe(predicted, use_container_width=True, hide_index=True)
    st.caption("Illustrative PoC projections — not product benchmarks.")

st.subheader("3 · Decide")
for rec in result.recommendations:
    with st.container(border=True):
        c1, c2, c3 = st.columns([5, 1, 2])
        with c1:
            st.markdown(f"**{rec.title}**")
            st.write(rec.rationale)
            st.caption(f"Expected: {rec.expected_outcome}")
        with c2:
            st.markdown(f"**{rec.risk.value}** risk")
            st.caption("Human approval" if rec.requires_approval else "Auto-eligible")
        with c3:
            if rec.requires_approval:
                key = f"approve_{state.scenario}_{rec.action_id}"
                if rec.action_id in st.session_state.approved:
                    st.success("APPROVED")
                elif st.button("Approve simulated action", key=key, use_container_width=True):
                    st.session_state.approved.add(rec.action_id)
                    st.session_state.audit = append_event(
                        st.session_state.audit,
                        "APPROVAL",
                        f"Approved: {rec.title}",
                        actor="human-operator",
                        details={"action_id": rec.action_id, "risk": rec.risk.value},
                    )
                    st.rerun()
            else:
                st.success("AUTO-ELIGIBLE")

        with st.expander("Show simulated action"):
            st.code(rec.simulated_command, language="text")

st.subheader("4 · Audit")
if not st.session_state.audit:
    st.caption("Audit events will appear as scenarios and approvals are exercised.")
else:
    audit_rows = [
        {
            "UTC": event.timestamp,
            "Type": event.event_type,
            "Actor": event.actor,
            "Event": event.message,
        }
        for event in reversed(st.session_state.audit[-12:])
    ]
    st.dataframe(pd.DataFrame(audit_rows), use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Synthetic portfolio PoC. No real infrastructure actions are executed. "
    "The model is never the authorization layer."
)
