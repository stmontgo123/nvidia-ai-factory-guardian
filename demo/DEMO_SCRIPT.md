# Eight-Minute Demo Script

## 0:00 - 0:45 | Set the problem

"AI factories turn GPU capacity into tokens, but they also introduce a new operations problem: utilization, latency, power, failures, and cost all interact. A normal dashboard tells me what is red. This PoC asks a harder question: what should the operator do, what is safe to automate, and what requires approval?"

## 0:45 - 1:30 | Establish normal state

Show **Baseline**.

Point out:

- two simulated 128-GPU-equivalent clusters;
- healthy TTFT and queue depth;
- normal power headroom;
- low SLO risk.

Say: "A good agent should also know when not to act."

## 1:30 - 3:30 | Killer scenario - GPU node failure

Click **Inject GPU node failure**.

Narrate the evidence:

- Cluster A utilization jumps above 90%;
- queue and TTFT spike;
- one node becomes unhealthy;
- Cluster B remains lightly utilized.

Show the probable cause and confidence score.

Highlight the remediation hierarchy:

1. Shift 15% traffic - bounded and auto-eligible.
2. Drain degraded node - high-risk and requires approval.
3. Add serving replicas - approval required.

Click **Approve simulated action** for the node drain.

Scroll to the audit trail.

Say: "The model can explain this plan, but it cannot authorize the drain."

## 3:30 - 5:15 | Demand event

Click **Inject 3x traffic spike**.

Say: "This looks superficially similar - latency is high - but the cause is different. Both clusters are healthy; demand is the constraint."

Show that Guardian first protects interactive work, then proposes capacity expansion/cloud burst with explicit approval.

## 5:15 - 6:30 | Power event

Click **Inject power constraint**.

Say: "Here adding more on-prem compute would be the wrong answer. Facility power is the binding constraint. The recommendation is to reduce noncritical load or move work."

## 6:30 - 7:15 | Optional NVIDIA model

If an API key is configured, enable **Use NVIDIA-hosted model summary**.

Explain that the model receives synthetic, grounded facts and the already-computed recommendations. It improves operator communication, not authorization.

If the API is unavailable, skip this section. That resilience is part of the design.

## 7:15 - 8:00 | Close with the roadmap

Show `architecture/ARCHITECTURE.md` or the executive deck.

"Version one proves the enterprise operating model for free on a laptop. The next step is to replace the hand-authored simulator with NVIDIA Dynamo DynoSim/Spica outputs and later read actual DCGM/NIM telemetry. The architecture is intentionally staged so real infrastructure write access is the last thing added, not the first."
