"""Deterministic action-risk and approval policy.

This module is deliberately separate from the LLM client. The model can explain a
recommendation, but it cannot authorize an infrastructure action.
"""

from __future__ import annotations

from models import ActionRisk, Recommendation


AUTO_ELIGIBLE_ACTIONS = {
    "reroute_traffic_15pct",
    "reduce_batch_priority",
}

APPROVAL_REQUIRED_ACTIONS = {
    "drain_gpu_node",
    "scale_nim_replicas",
    "cloud_burst",
    "change_power_profile",
}


def evaluate_action(action_id: str) -> tuple[ActionRisk, bool]:
    """Return (risk, requires_approval) for a known simulated action."""
    if action_id in AUTO_ELIGIBLE_ACTIONS:
        return ActionRisk.LOW, False
    if action_id in APPROVAL_REQUIRED_ACTIONS:
        if action_id in {"drain_gpu_node", "change_power_profile"}:
            return ActionRisk.HIGH, True
        return ActionRisk.MEDIUM, True
    raise ValueError(f"Unknown action_id: {action_id}")


def recommendation(
    action_id: str,
    title: str,
    rationale: str,
    expected_outcome: str,
    simulated_command: str,
) -> Recommendation:
    risk, requires_approval = evaluate_action(action_id)
    return Recommendation(
        action_id=action_id,
        title=title,
        rationale=rationale,
        expected_outcome=expected_outcome,
        risk=risk,
        requires_approval=requires_approval,
        simulated_command=simulated_command,
    )
