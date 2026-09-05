# Architecture

## Executive view

```text
                     NVIDIA AI FACTORY GUARDIAN

       AI FACTORY / INFERENCE ESTATE (simulated in v1)
                           |
         +-----------------+-----------------+
         |                 |                 |
         v                 v                 v
   GPU HEALTH          INFERENCE          POWER / COST
   utilization         TTFT               watts / headroom
   errors              queue depth        cost / token
   node health         tokens/sec         placement
         |                 |                 |
         +-----------------+-----------------+
                           |
                           v
                NORMALIZED FACTORY STATE
                           |
               +-----------+-----------+
               |                       |
               v                       v
      DETERMINISTIC DIAGNOSTICS   OPTIONAL NEMOTRON
      SLO / policy logic          explanation only
               |                       |
               +-----------+-----------+
                           |
                           v
                  RECOMMENDATION PLAN
                           |
                           v
                   POLICY / RISK GATE
                 +---------+---------+
                 |                   |
                 v                   v
          BOUNDED LOW-RISK      CONSEQUENTIAL
             AUTO-ELIGIBLE      HUMAN APPROVAL
                 |                   |
                 +---------+---------+
                           |
                           v
                 SIMULATED EXECUTION
                           |
                           v
                     AUDIT TRAIL
```

## Why this separation matters

The Large Language Model is useful for summarization, hypothesis articulation, and operator communication. It is deliberately **not** responsible for authorization.

A deterministic policy layer decides whether an action is auto-eligible or requires explicit approval. This mirrors the governance pattern used in the user's other enterprise AI portfolio demonstrations.

## Version 1 - laptop / zero-GPU mode

```text
Streamlit UI
    |
    +--> FactorySimulator (synthetic clusters)
    |
    +--> Deterministic diagnostics
    |
    +--> Policy engine
    |
    +--> Optional NVIDIA hosted model summary
    |
    +--> In-memory append-only-style audit events
```

This version is designed to be reproducible without CUDA, Kubernetes, or an NVIDIA GPU.

## Version 2 - NVIDIA-native simulation

```text
Workload trace / synthetic demand
              |
              v
       NVIDIA Dynamo DynoSim
              |
              v
   simulated serving configuration
              |
       +------+------+
       |             |
       v             v
    Planner        Router
    behavior       behavior
       |             |
       +------+------+
              v
        Guardian analysis
              |
              v
   capacity / SLO / cost decision
```

DynoSim is intended to explore serving configurations before spending GPU time. Guardian's role is to turn simulation output into an enterprise operations decision narrative and policy-controlled action plan.

## Version 3 - live telemetry integration

```text
NVIDIA DCGM / DCGM Exporter ----+
                                |
NIM metrics / inference stats --+--> Prometheus --> Guardian
                                |
Cluster / scheduler state -------+
```

At this stage the synthetic evidence adapters are replaced with read-only connectors. All write actions remain simulated until organization-specific controls, authentication, secrets, networking, change management, and approvals are designed.

## Version 4 - controlled action adapters

Potential bounded adapters could include:

- routing-weight changes within fixed safety bounds;
- queue priority changes for preapproved workload classes;
- workload-placement requests;
- replica-scale requests;
- node-drain workflows;
- ticket/change creation rather than direct execution.

Each adapter should have independent identity, authorization, blast-radius limits, and audit controls.
