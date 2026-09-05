# Executive Brief

## The problem

AI infrastructure is expensive enough that underutilized capacity, latency spikes, poor workload placement, and avoidable operational failures have direct business impact. Traditional dashboards show symptoms, but operators still have to assemble evidence across infrastructure, inference, cost, and facility constraints before deciding what to do.

## The idea

**AI Factory Guardian** is a portfolio proof of concept for an operations decision layer that converts AI-factory telemetry into an explainable, policy-constrained remediation plan.

It observes simulated GPU health, inference latency, queue depth, throughput, power, and token economics. It identifies the likely operating constraint, recommends actions, separates low-risk changes from consequential changes, and preserves human accountability.

## What makes it different from a chatbot

The project is not primarily a conversational interface. Its focus is an operational control pattern:

**Observe -> Reason -> Decide -> Approve -> Audit**

The Large Language Model is optional and is used to explain already-grounded findings. Authorization remains deterministic.

## Business outcomes demonstrated

- Higher effective utilization of scarce accelerator capacity
- Lower time-to-first-token under failure or burst demand
- Explicit cost-per-token visibility
- Better capacity-placement decisions
- Reduced mean time to understand an infrastructure incident
- Human control of high-impact operational changes
- Auditable AI-assisted decision making

## Why NVIDIA

The design aligns with NVIDIA's AI-infrastructure software direction: NIM for inference APIs, DCGM for GPU monitoring, and Dynamo for distributed inference and simulation. DynoSim and Spica provide a future path to replace simplistic synthetic capacity modeling with NVIDIA-native offline simulation.

## Portfolio message

> I am interested in the operating problem behind AI factories: how to keep expensive accelerated infrastructure healthy, highly utilized, economically efficient, and governed as it becomes mission-critical enterprise infrastructure.
