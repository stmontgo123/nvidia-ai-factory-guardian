# NVIDIA AI Factory Guardian

**Agentic SRE + Token Economics for AI Factories**

> Keep an AI factory healthy while maximizing useful inference per GPU, per watt, and per dollar.

NVIDIA AI Factory Guardian is an independent portfolio proof of concept showing how enterprise operations teams can reason over AI-infrastructure telemetry, predict SLO risk, recommend bounded remediation, require human approval for consequential actions, and preserve a defensible audit trail.

The first release is intentionally **GPU-free**: it simulates an AI factory on a laptop and optionally uses a hosted NVIDIA NIM-compatible endpoint for the natural-language operations summary. A later phase can connect the same operating model to NVIDIA Dynamo simulation, DCGM telemetry, Prometheus/Grafana, Run:ai, and live NIM metrics.

> **Independent portfolio project. Not affiliated with or endorsed by NVIDIA.**

## Anchor scenario

A 256-GPU-equivalent inference estate begins missing latency objectives while expensive capacity sits underused elsewhere.

Guardian:

1. observes cluster utilization, queue depth, time-to-first-token (TTFT), throughput, power, and health signals;
2. correlates symptoms across two simulated AI-factory clusters;
3. predicts SLO risk before the incident becomes a user-visible outage;
4. generates an explainable remediation plan;
5. applies deterministic risk policy outside the Large Language Model;
6. automatically permits only bounded low-risk actions;
7. queues consequential actions for explicit human approval; and
8. records evidence, recommendations, approvals, and actions in an audit trail.

## Killer value proposition

- Increase effective GPU utilization
- Reduce latency and queueing risk
- Improve tokens-per-dollar and tokens-per-watt visibility
- Detect degraded nodes before they become broad service incidents
- Rebalance workloads across available capacity
- Model cloud-burst and capacity decisions
- Keep consequential infrastructure actions under human control
- Create an auditable record of operational decisions

## Core architecture principle

**The model is not the authorization layer.**

```text
GPU / Inference / Power Telemetry
              |
              v
     Normalized Factory State
              |
      +-------+-------+
      |               |
      v               v
Deterministic       Optional
Diagnostics         Nemotron Summary
      |               |
      +-------+-------+
              v
     Recommended Actions
              |
              v
      Policy / Risk Engine
        +-----+-----+
        |           |
  Bounded / low   Consequential
        |           |
        v           v
   AUTO-ELIGIBLE   PENDING HUMAN APPROVAL
        |           |
        +-----+-----+
              v
          Audit Trail
```

## Demo scenarios

### 1. GPU node degradation

One node begins erroring and the affected cluster loses usable capacity. Guardian identifies the degraded node, recommends draining it, redistributes traffic, and predicts recovery.

### 2. Inference traffic spike

Request volume triples. Queue depth and TTFT rise while another cluster has capacity. Guardian recommends workload redistribution and a controlled replica increase.

### 3. Power constraint

Facility power approaches its operating threshold. Guardian recommends reducing noncritical load, shifting low-priority work, and preserving latency-sensitive inference.

## Metrics shown in the PoC

- GPU utilization
- Time to first token (TTFT)
- Queue depth
- Tokens per second
- Estimated cost per one million tokens
- Power utilization
- Error rate
- SLO risk

These are **illustrative simulated values**, not NVIDIA product performance claims.

## NVIDIA technology direction

The PoC is designed around current NVIDIA building blocks:

- **NVIDIA NIM** - OpenAI-compatible inference API surface for model reasoning
- **NVIDIA Nemotron** - optional reasoning/summarization model family
- **NVIDIA DCGM / DCGM Exporter** - GPU health and Prometheus-oriented telemetry direction
- **NVIDIA Dynamo** - distributed inference platform
- **DynoSim** - Dynamo simulation stack for exploring serving configurations before spending GPU time
- **Spica / AI Simulate** - experimental replay-backed configuration search for Dynamo deployments

See [Technical References](docs/TECHNICAL_REFERENCES.md).

## Repository layout

```text
nvidia-ai-factory-guardian/
├── README.md
├── SECURITY.md
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── app.py
│   ├── agent.py
│   ├── audit.py
│   ├── models.py
│   ├── nvidia_client.py
│   ├── policy.py
│   └── simulator.py
├── tests/
│   ├── test_policy.py
│   └── test_simulator.py
├── scripts/
│   └── smoke_test.py
├── architecture/
│   └── ARCHITECTURE.md
├── demo/
│   ├── DEMO_SCRIPT.md
│   └── NINETY_SECOND_DEMO.md
├── docs/
│   ├── BUILD_AND_DEMO_RUNBOOK.md
│   ├── EXECUTIVE_BRIEF.md
│   ├── DECISION_RATIONALE.md
│   ├── INTERVIEW_DEFENSE.md
│   ├── DYNAMO_INTEGRATION_ROADMAP.md
│   └── TECHNICAL_REFERENCES.md
└── presentation/
    └── README.md
```

## Quick start - no GPU and no API key required

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run src/app.py
```

The app starts in deterministic simulation mode.

## Optional NVIDIA hosted model

Create a `.env` file from `.env.example` and supply an NVIDIA API key. The application sends only the simulated operational state and deterministic recommendations to the model for an executive-friendly explanation.

```bash
cp .env.example .env
```

Then set:

```text
NVIDIA_API_KEY=your_key_here
```

Model availability and trial terms can change. Select a currently available NVIDIA-hosted model in `NVIDIA_MODEL`.

## What this portfolio demonstrates

- AI infrastructure architecture
- Agentic operations patterns
- Site Reliability Engineering (SRE)
- AI-factory observability
- Capacity engineering
- Token economics / FinOps
- Deterministic control outside the LLM
- Human-in-the-loop governance
- Explainable remediation
- Multicloud / hybrid placement thinking
- A path from synthetic PoC to NVIDIA-native simulation and telemetry

## Portfolio thesis

> AI factories should be operated like mission-critical production systems: observable, economically measurable, policy-constrained, and resilient under failure.

The differentiator is not another chatbot. It is the intersection of **AI infrastructure + production operations + economics + governance**.
