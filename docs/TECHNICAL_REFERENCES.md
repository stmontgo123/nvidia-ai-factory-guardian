# Technical References

Official NVIDIA material used to ground the technology direction of this PoC.

## NVIDIA NIM

NIM for LLMs exposes OpenAI-compatible inference endpoints.

- https://docs.nvidia.com/nim/large-language-models/latest/api-reference.html
- https://docs.nvidia.com/nim/large-language-models/latest/reference/architecture.html
- https://build.nvidia.com/

The hosted API examples use an OpenAI-compatible client with:

```text
https://integrate.api.nvidia.com/v1
```

Availability and trial terms can change; verify the model selected in `.env` before a live demonstration.

## NVIDIA Nemotron

- https://developer.nvidia.com/topics/ai/nemotron
- https://build.nvidia.com/models

Nemotron is used only as an optional explanation layer in this PoC.

## NVIDIA DCGM and GPU telemetry

- https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
- https://docs.nvidia.com/datacenter/cloud-native/gpu-telemetry/latest/about-telemetry.html

DCGM provides GPU monitoring/health capabilities. DCGM Exporter exposes GPU metrics for Prometheus-oriented monitoring workflows.

## NVIDIA Dynamo / DynoSim

- https://docs.nvidia.com/dynamo/dev/cli/operations/dynosim/overview
- https://docs.nvidia.com/dynamo/dev/knowledge-base/concepts/simulation/simulation-runs

DynoSim is Dynamo's simulation stack for exploring serving configurations before validating them on real clusters. NVIDIA documentation describes offline simulation that can run on CPUs.

## AI Simulate / Spica

- https://docs.nvidia.com/dynamo/knowledge-base/modular-components/ai-simulate/spica/overview
- https://docs.nvidia.com/dynamo/knowledge-base/modular-components/ai-simulate/spica/optimization-goals

Spica is experimental and should not be presented as production capacity guidance or an SLA guarantee.
