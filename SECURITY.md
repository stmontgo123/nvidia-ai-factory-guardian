# Security

This is an educational portfolio proof of concept using synthetic data.

## Safety model

- The application does not connect to production GPU clusters.
- The simulator contains no real infrastructure credentials.
- The optional LLM receives only synthetic metrics and precomputed recommendations.
- The LLM never decides whether an action is authorized.
- Consequential actions remain subject to deterministic policy and human approval.
- Actions are simulated; they do not modify real infrastructure.

## Never add

- Production API keys or credentials
- Customer data
- Proprietary infrastructure inventory
- Real incident data without approval
- Cloud access tokens
- NVIDIA NGC or enterprise credentials

Use environment variables for optional API keys and keep `.env` out of source control.
