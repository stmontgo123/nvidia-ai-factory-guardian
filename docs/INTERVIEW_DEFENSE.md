# Interview Defense

Use this document to explain the PoC under technical questioning.

## Thirty-second explanation

"AI Factory Guardian is a GPU-free operations PoC for AI infrastructure. It simulates two inference clusters, detects whether an incident is driven by hardware degradation, demand saturation, or facility power, and produces a policy-controlled remediation plan. The LLM is optional and only explains grounded findings. High-impact actions require human approval and everything is auditable. The next phase is to feed it NVIDIA Dynamo simulation and DCGM/NIM telemetry."

## Why is the first version synthetic?

Because the architecture and decision model should be testable without requiring a multimillion-dollar GPU environment. Synthetic evidence makes the demo reproducible and safe while preserving a clean adapter boundary for real telemetry later.

## Is the AI really agentic if the policy is deterministic?

Yes. Agentic behavior is in evidence assembly, diagnosis, planning, and orchestration. Authorization does not need to be probabilistic. In an enterprise system, separating flexible reasoning from deterministic control is a feature, not a limitation.

## Why not let the model call infrastructure APIs directly?

Infrastructure changes have blast radius. The model can propose a bounded action, but a separate policy layer evaluates the action type, risk, authorization, and approval requirement. This reduces the chance that a prompt, hallucination, or compromised knowledge source becomes an infrastructure command.

## What would you integrate first in a real NVIDIA environment?

Read-only telemetry. DCGM/DCGM Exporter and inference metrics are a safer first integration than write access. After the evidence pipeline is trusted, add Dynamo simulation for what-if capacity decisions. Direct actions come last.

## Where does Dynamo fit?

Dynamo is the distributed-inference platform direction. DynoSim can model serving configurations offline, and Spica can explore candidate configurations experimentally. Guardian would consume those outputs and add enterprise policy, cost framing, approval, and decision-defense.

## What metrics matter most?

For this PoC: TTFT, queue depth, GPU utilization, throughput, error rate, power headroom, and estimated cost per token. In a real implementation the metric set would be workload-specific and would include SLO percentiles, cache behavior, scheduler state, network/fabric signals, and workload priority.

## What is intentionally not production-ready?

- No production telemetry connectors
- No durable audit database
- No identity provider
- No secrets manager
- No Kubernetes control plane
- No real change-management integration
- No verified cost model
- No SLA prediction model

Those omissions are explicit so the PoC is not mistaken for a production control plane.

## Strong closing line

"The project is really about applying the operational rigor we learned running databases, clouds, and data centers to the new scarce resource: accelerated inference capacity producing tokens."
