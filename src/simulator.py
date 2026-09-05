"""Deterministic, GPU-free AI factory simulator.

The values in this module are illustrative. They are designed to create a stable,
repeatable executive demo and are not NVIDIA product performance claims.
"""

from __future__ import annotations

from copy import deepcopy

from models import ClusterMetrics, FactoryState, SLARisk


class FactorySimulator:
    """Returns deterministic factory states for each demonstration scenario."""

    BASELINE = "Baseline"
    GPU_FAILURE = "GPU Node Failure"
    TRAFFIC_SPIKE = "Traffic Spike"
    POWER_CONSTRAINT = "Power Constraint"

    scenarios = (BASELINE, GPU_FAILURE, TRAFFIC_SPIKE, POWER_CONSTRAINT)

    def state(self, scenario: str) -> FactoryState:
        if scenario not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario}")

        states = {
            self.BASELINE: self._baseline(),
            self.GPU_FAILURE: self._gpu_failure(),
            self.TRAFFIC_SPIKE: self._traffic_spike(),
            self.POWER_CONSTRAINT: self._power_constraint(),
        }
        return deepcopy(states[scenario])

    @staticmethod
    def _baseline() -> FactoryState:
        return FactoryState(
            scenario=FactorySimulator.BASELINE,
            clusters=[
                ClusterMetrics(
                    name="Cluster A - latency-sensitive",
                    gpu_equivalents=128,
                    gpu_utilization_pct=67.0,
                    queue_depth=180,
                    ttft_ms=515,
                    tokens_per_second=650_000,
                    power_utilization_pct=72.0,
                    error_rate_pct=0.2,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
                ClusterMetrics(
                    name="Cluster B - shared inference",
                    gpu_equivalents=128,
                    gpu_utilization_pct=59.0,
                    queue_depth=125,
                    ttft_ms=480,
                    tokens_per_second=590_000,
                    power_utilization_pct=66.0,
                    error_rate_pct=0.1,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
            ],
            cost_per_million_tokens_usd=0.31,
            sla_risk=SLARisk.LOW,
            incident_note="Healthy operating state. Capacity headroom exists for routine bursts.",
        )

    @staticmethod
    def _gpu_failure() -> FactoryState:
        return FactoryState(
            scenario=FactorySimulator.GPU_FAILURE,
            clusters=[
                ClusterMetrics(
                    name="Cluster A - latency-sensitive",
                    gpu_equivalents=128,
                    gpu_utilization_pct=92.0,
                    queue_depth=1_620,
                    ttft_ms=1_840,
                    tokens_per_second=475_000,
                    power_utilization_pct=87.0,
                    error_rate_pct=3.9,
                    healthy_nodes=15,
                    total_nodes=16,
                ),
                ClusterMetrics(
                    name="Cluster B - shared inference",
                    gpu_equivalents=128,
                    gpu_utilization_pct=31.0,
                    queue_depth=95,
                    ttft_ms=455,
                    tokens_per_second=310_000,
                    power_utilization_pct=48.0,
                    error_rate_pct=0.1,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
            ],
            cost_per_million_tokens_usd=0.48,
            sla_risk=SLARisk.HIGH,
            incident_note=(
                "One simulated node in Cluster A is degraded. Cluster A is saturated while "
                "Cluster B retains substantial usable capacity."
            ),
        )

    @staticmethod
    def _traffic_spike() -> FactoryState:
        return FactoryState(
            scenario=FactorySimulator.TRAFFIC_SPIKE,
            clusters=[
                ClusterMetrics(
                    name="Cluster A - latency-sensitive",
                    gpu_equivalents=128,
                    gpu_utilization_pct=95.0,
                    queue_depth=2_350,
                    ttft_ms=2_120,
                    tokens_per_second=720_000,
                    power_utilization_pct=90.0,
                    error_rate_pct=0.8,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
                ClusterMetrics(
                    name="Cluster B - shared inference",
                    gpu_equivalents=128,
                    gpu_utilization_pct=74.0,
                    queue_depth=1_020,
                    ttft_ms=1_190,
                    tokens_per_second=610_000,
                    power_utilization_pct=78.0,
                    error_rate_pct=0.4,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
            ],
            cost_per_million_tokens_usd=0.43,
            sla_risk=SLARisk.HIGH,
            incident_note=(
                "Synthetic request volume increased approximately 3x. Both clusters are "
                "approaching saturation and latency is deteriorating."
            ),
        )

    @staticmethod
    def _power_constraint() -> FactoryState:
        return FactoryState(
            scenario=FactorySimulator.POWER_CONSTRAINT,
            clusters=[
                ClusterMetrics(
                    name="Cluster A - latency-sensitive",
                    gpu_equivalents=128,
                    gpu_utilization_pct=82.0,
                    queue_depth=560,
                    ttft_ms=790,
                    tokens_per_second=690_000,
                    power_utilization_pct=96.0,
                    error_rate_pct=0.2,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
                ClusterMetrics(
                    name="Cluster B - shared inference",
                    gpu_equivalents=128,
                    gpu_utilization_pct=70.0,
                    queue_depth=420,
                    ttft_ms=680,
                    tokens_per_second=590_000,
                    power_utilization_pct=94.0,
                    error_rate_pct=0.2,
                    healthy_nodes=16,
                    total_nodes=16,
                ),
            ],
            cost_per_million_tokens_usd=0.36,
            sla_risk=SLARisk.MEDIUM,
            incident_note=(
                "Facility power headroom is below the demonstration threshold. New local "
                "capacity should not be added until load is shifted or reduced."
            ),
        )
