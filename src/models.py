"""Domain models for the AI Factory Guardian demo."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class SLARisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ActionRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(slots=True)
class ClusterMetrics:
    name: str
    gpu_equivalents: int
    gpu_utilization_pct: float
    queue_depth: int
    ttft_ms: float
    tokens_per_second: int
    power_utilization_pct: float
    error_rate_pct: float
    healthy_nodes: int
    total_nodes: int


@dataclass(slots=True)
class FactoryState:
    scenario: str
    clusters: list[ClusterMetrics]
    cost_per_million_tokens_usd: float
    sla_risk: SLARisk
    incident_note: str

    @property
    def total_gpu_equivalents(self) -> int:
        return sum(cluster.gpu_equivalents for cluster in self.clusters)

    @property
    def average_gpu_utilization_pct(self) -> float:
        total = sum(c.gpu_utilization_pct * c.gpu_equivalents for c in self.clusters)
        return total / max(self.total_gpu_equivalents, 1)

    @property
    def total_queue_depth(self) -> int:
        return sum(c.queue_depth for c in self.clusters)

    @property
    def weighted_ttft_ms(self) -> float:
        total = sum(c.ttft_ms * c.gpu_equivalents for c in self.clusters)
        return total / max(self.total_gpu_equivalents, 1)

    @property
    def total_tokens_per_second(self) -> int:
        return sum(c.tokens_per_second for c in self.clusters)

    @property
    def average_power_utilization_pct(self) -> float:
        total = sum(c.power_utilization_pct * c.gpu_equivalents for c in self.clusters)
        return total / max(self.total_gpu_equivalents, 1)


@dataclass(slots=True)
class Recommendation:
    action_id: str
    title: str
    rationale: str
    expected_outcome: str
    risk: ActionRisk
    requires_approval: bool
    simulated_command: str


@dataclass(slots=True)
class AnalysisResult:
    probable_cause: str
    confidence_pct: int
    recommendations: list[Recommendation]
    predicted_ttft_ms: float
    predicted_gpu_utilization_pct: float
    predicted_tokens_per_second: int
    predicted_cost_per_million_tokens_usd: float
    deterministic_summary: str
    model_summary: str | None = None


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    message: str
    actor: str = "guardian"
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
