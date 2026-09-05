"""Optional NVIDIA-hosted OpenAI-compatible model client."""

from __future__ import annotations

import os
from typing import Iterable

from models import FactoryState, Recommendation


def _load_dotenv_if_available() -> None:
    """Load a local .env file when python-dotenv is installed.

    The base simulation should remain importable even before optional client
    dependencies are installed, which makes the GPU-free deterministic path
    easy to test.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


_load_dotenv_if_available()


def is_configured() -> bool:
    return bool(os.getenv("NVIDIA_API_KEY", "").strip())


def explain(
    state: FactoryState,
    probable_cause: str,
    recommendations: Iterable[Recommendation],
) -> str | None:
    """Ask a hosted model to explain deterministic findings in executive language.

    This function is not part of the authorization path. It receives synthetic
    telemetry and recommendations that have already been computed by code.
    """
    api_key = os.getenv("NVIDIA_API_KEY", "").strip()
    if not api_key:
        return None

    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    model = os.getenv("NVIDIA_MODEL", "mistralai/mistral-nemotron")

    rec_text = "\n".join(
        f"- {r.title}: {r.rationale} (approval_required={r.requires_approval})"
        for r in recommendations
    )

    prompt = f"""
You are the executive operations narrator for a synthetic AI-factory demonstration.
Do not invent metrics, actions, NVIDIA product claims, or root causes.
Do not authorize actions. The deterministic policy engine is authoritative.

Scenario: {state.scenario}
SLO risk: {state.sla_risk.value}
Average GPU utilization: {state.average_gpu_utilization_pct:.1f}%
Weighted TTFT: {state.weighted_ttft_ms:.0f} ms
Queue depth: {state.total_queue_depth}
Tokens/second: {state.total_tokens_per_second:,}
Power utilization: {state.average_power_utilization_pct:.1f}%
Estimated cost / 1M tokens: ${state.cost_per_million_tokens_usd:.2f}
Probable cause: {probable_cause}

Deterministic recommendations:
{rec_text}

Write a concise 4-6 sentence executive incident summary. Clearly distinguish
observed evidence, inferred cause, proposed remediation, and any actions that
require human approval.
""".strip()

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Optional NVIDIA model support requires the 'openai' package. "
            "Install requirements.txt before enabling model narration."
        ) from exc

    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You explain synthetic infrastructure findings accurately and concisely. "
                    "Never claim authority to execute an action."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=450,
        stream=False,
    )
    return response.choices[0].message.content
