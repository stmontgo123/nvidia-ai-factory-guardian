"""Deterministic diagnostic agent for the portfolio demonstration."""

from __future__ import annotations

from models import AnalysisResult, FactoryState
from nvidia_client import explain as nvidia_explain
from policy import recommendation
from simulator import FactorySimulator


def analyze(state: FactoryState, use_model: bool = False) -> AnalysisResult:
    """Analyze a synthetic factory state and return explainable recommendations."""

    if state.scenario == FactorySimulator.BASELINE:
        cause = "No active incident; the factory has normal capacity headroom."
        recs = [
            recommendation(
                "reroute_traffic_15pct",
                "Maintain balanced routing",
                "Both clusters are healthy and no emergency action is required.",
                "Preserve latency headroom while avoiding concentrated load.",
                "SIMULATE router.weight cluster_a=50 cluster_b=50",
            )
        ]
        result = AnalysisResult(
            probable_cause=cause,
            confidence_pct=98,
            recommendations=recs,
            predicted_ttft_ms=495,
            predicted_gpu_utilization_pct=63,
            predicted_tokens_per_second=1_240_000,
            predicted_cost_per_million_tokens_usd=0.31,
            deterministic_summary=(
                "Factory health is normal. No consequential remediation is required. "
                "Continue balanced routing and monitor capacity headroom."
            ),
        )

    elif state.scenario == FactorySimulator.GPU_FAILURE:
        cause = (
            "A degraded node in Cluster A has reduced usable capacity while routing remains "
            "concentrated on Cluster A; Cluster B retains significant headroom."
        )
        recs = [
            recommendation(
                "reroute_traffic_15pct",
                "Shift 15% of inference traffic to Cluster B",
                "Cluster B is lightly utilized while Cluster A is saturated.",
                "Reduce queue pressure immediately without a privileged node operation.",
                "SIMULATE router.shift destination=cluster_b percent=15",
            ),
            recommendation(
                "drain_gpu_node",
                "Drain the degraded GPU node",
                "The node has elevated errors and should be isolated from new work.",
                "Remove the unstable node from the serving path and prevent cascading errors.",
                "SIMULATE node.drain cluster=cluster_a node=gpu-node-47",
            ),
            recommendation(
                "scale_nim_replicas",
                "Add two inference replicas after the node is isolated",
                "Recovered capacity should be redistributed to restore latency headroom.",
                "Improve TTFT and absorb residual queue backlog.",
                "SIMULATE nim.scale replicas=+2 cluster=cluster_b",
            ),
        ]
        result = AnalysisResult(
            probable_cause=cause,
            confidence_pct=94,
            recommendations=recs,
            predicted_ttft_ms=710,
            predicted_gpu_utilization_pct=76,
            predicted_tokens_per_second=1_240_000,
            predicted_cost_per_million_tokens_usd=0.29,
            deterministic_summary=(
                "Cluster A saturation is correlated with one degraded node while Cluster B "
                "has spare capacity. Shift bounded traffic immediately, then request approval "
                "to drain the node and restore replica headroom."
            ),
        )

    elif state.scenario == FactorySimulator.TRAFFIC_SPIKE:
        cause = (
            "A synthetic 3x request surge has driven both clusters toward saturation; queue "
            "growth is now the dominant contributor to TTFT risk."
        )
        recs = [
            recommendation(
                "reduce_batch_priority",
                "Deprioritize noninteractive batch inference",
                "Latency-sensitive requests should retain first access to constrained capacity.",
                "Recover interactive SLO headroom without immediately adding infrastructure.",
                "SIMULATE queue.priority workload=batch priority=low",
            ),
            recommendation(
                "scale_nim_replicas",
                "Scale inference replicas",
                "Both clusters are near saturation and queue depth continues to rise.",
                "Increase serving concurrency while the burst persists.",
                "SIMULATE nim.scale replicas=+4",
            ),
            recommendation(
                "cloud_burst",
                "Evaluate temporary cloud-burst capacity",
                "If the demand burst persists, local headroom may be insufficient.",
                "Protect SLOs while exposing the incremental cost decision to a human operator.",
                "SIMULATE capacity.cloud_burst gpu_equivalents=32 duration=60m",
            ),
        ]
        result = AnalysisResult(
            probable_cause=cause,
            confidence_pct=96,
            recommendations=recs,
            predicted_ttft_ms=760,
            predicted_gpu_utilization_pct=81,
            predicted_tokens_per_second=1_680_000,
            predicted_cost_per_million_tokens_usd=0.35,
            deterministic_summary=(
                "Demand, not hardware failure, is driving the incident. Protect interactive "
                "traffic first, then request approval to add temporary serving capacity."
            ),
        )

    elif state.scenario == FactorySimulator.POWER_CONSTRAINT:
        cause = (
            "Facility power utilization is above the demonstration operating threshold even "
            "though GPU demand remains serviceable. Capacity expansion on-premises would "
            "increase risk."
        )
        recs = [
            recommendation(
                "reduce_batch_priority",
                "Throttle low-priority batch inference",
                "Batch work can yield capacity without directly impacting interactive demand.",
                "Create power headroom while preserving user-facing latency.",
                "SIMULATE queue.throttle workload=batch percent=25",
            ),
            recommendation(
                "change_power_profile",
                "Apply reduced-power profile to noncritical workers",
                "Power headroom is the binding constraint in this scenario.",
                "Lower facility demand while maintaining critical serving capacity.",
                "SIMULATE gpu.power_profile workers=noncritical profile=efficiency",
            ),
            recommendation(
                "cloud_burst",
                "Shift low-priority work to external burst capacity",
                "Moving noncritical workloads can free both power and local GPU capacity.",
                "Restore power headroom while making incremental cost explicit.",
                "SIMULATE placement.shift workload=batch destination=cloud-burst",
            ),
        ]
        result = AnalysisResult(
            probable_cause=cause,
            confidence_pct=92,
            recommendations=recs,
            predicted_ttft_ms=610,
            predicted_gpu_utilization_pct=72,
            predicted_tokens_per_second=1_210_000,
            predicted_cost_per_million_tokens_usd=0.34,
            deterministic_summary=(
                "Power, not GPU availability, is the binding constraint. Reduce noncritical "
                "local demand before adding capacity, and require human approval for power-profile "
                "or cloud-placement changes."
            ),
        )

    else:  # defensive programming if another state enters the function
        raise ValueError(f"Unsupported scenario: {state.scenario}")

    if use_model:
        try:
            result.model_summary = nvidia_explain(
                state=state,
                probable_cause=result.probable_cause,
                recommendations=result.recommendations,
            )
        except Exception as exc:  # the deterministic demo should remain available
            result.model_summary = f"Optional NVIDIA model unavailable: {exc}"

    return result
