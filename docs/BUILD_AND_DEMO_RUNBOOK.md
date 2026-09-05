# Build and Demo Runbook

## Goal

Run the complete portfolio demonstration on a laptop without an NVIDIA GPU. The optional hosted model is an enhancement, not a requirement.

## Prerequisites

- Python 3.10 or newer
- Git
- Internet access only if using the optional NVIDIA-hosted model

## 1. Create the environment

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Run automated checks

```bash
pytest -q
python scripts/smoke_test.py
```

Expected result: all tests pass and all four scenarios print deterministic recommendations.

## 3. Start the dashboard

```bash
streamlit run src/app.py
```

Open the local URL shown by Streamlit.

## 4. Demo without an API key

Use the sidebar buttons in this order:

1. Baseline
2. GPU Node Failure
3. Traffic Spike
4. Power Constraint

The deterministic diagnostic and policy layers are fully functional.

## 5. Optional NVIDIA-hosted model

Copy the environment template:

```bash
cp .env.example .env
```

Set `NVIDIA_API_KEY`. The default base URL uses NVIDIA's OpenAI-compatible hosted API surface.

Model availability can change, so set `NVIDIA_MODEL` to a model that is currently available in the NVIDIA API catalog.

Restart Streamlit and enable **Use NVIDIA-hosted model summary** in the sidebar.

Important: the model receives synthetic metrics and deterministic recommendations. It does not authorize actions.

## 6. Recommended live demo sequence

### Baseline

Point out that the system is healthy and the agent does not manufacture an incident.

### GPU failure

Click **Inject GPU node failure**.

Emphasize:

- Cluster A is saturated.
- Cluster B has spare capacity.
- A bounded routing shift is auto-eligible.
- Draining a node requires human approval.
- Predicted recovery is shown separately from current evidence.

Approve the simulated node-drain action and show the audit event.

### Traffic spike

Click **Inject 3x traffic spike**.

Emphasize that the system differentiates a demand problem from a hardware problem. It prioritizes interactive work before recommending additional capacity.

### Power constraint

Click **Inject power constraint**.

Emphasize that adding more local compute is the wrong answer when facility power is the binding constraint.

## 7. Streamlit Community Cloud

The deterministic app is suitable for a public demo because it needs no secret. If the optional NVIDIA API is enabled in a hosted deployment, store the key using the hosting platform's secret-management feature rather than committing `.env`.

## 8. Failure fallback

If the hosted model is unavailable, disable the model toggle. The core demo remains intact because the LLM is intentionally outside the control path.

## 9. Production disclaimer

This PoC does not execute infrastructure actions. A production implementation requires enterprise identity, secrets management, network segmentation, durable telemetry, change-management controls, policy review, resilience testing, and organization-specific approval rules.
