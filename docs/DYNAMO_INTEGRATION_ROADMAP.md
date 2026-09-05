# NVIDIA Dynamo Integration Roadmap

## Objective

Replace parts of the hand-authored simulator with NVIDIA-native offline simulation while preserving Guardian's enterprise decision and governance layer.

## Phase 2A - DynoSim read-only ingestion

1. Install a supported Dynamo / AI Simulate environment.
2. Run a documented offline DynoSim prediction on CPU.
3. Store the resulting summary/JSON report as a fixture.
4. Build an adapter that converts the report into Guardian's `FactoryState` model.
5. Display predicted TTFT / throughput / topology choices in the Streamlit app.
6. Keep all recommendations simulated.

Success criterion: Guardian can compare two simulated Dynamo deployment choices without any live GPU cluster.

## Phase 2B - configuration comparison

Add a dashboard workflow:

```text
Current topology
      |
      v
DynoSim prediction
      |
      +--> candidate A
      +--> candidate B
      +--> candidate C
      |
      v
Guardian policy + economics
      |
      v
Recommended candidate + explanation
```

## Phase 2C - Spica experiment

Spica is experimental. Treat it as a research/demo integration rather than production capacity guidance.

Potential demonstration question:

> Under a fixed simulated GPU budget, which deployment configuration best improves goodput while meeting a TTFT objective?

Guardian should not claim the result is globally optimal or an SLA guarantee. It should display the Spica result as experimental evidence alongside explicit caveats.

## Phase 3 - real telemetry

Add read-only adapters for:

- DCGM / DCGM Exporter GPU metrics
- Prometheus query API
- NIM inference metrics where available
- cluster/scheduler inventory

The internal `FactoryState` model remains the normalization boundary so the UI and policy engine do not depend directly on one telemetry source.
