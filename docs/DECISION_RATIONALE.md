# Decision Rationale

## Why build this project

Many AI portfolio demonstrations stop at prompting, RAG, or a chatbot. This project intentionally moves down the stack into AI infrastructure operations.

The goal is to demonstrate the intersection of:

- data-center operations;
- enterprise architecture;
- site reliability engineering;
- multicloud capacity thinking;
- inference economics;
- agentic AI; and
- governance.

## Why simulate first

The business logic can be demonstrated without owning a large GPU cluster. A deterministic simulator gives a repeatable story, makes the demo safe to publish, and allows the control model to be tested before adding product-specific integrations.

## Why the LLM is optional

A good infrastructure-control demo should continue to operate when the model endpoint is unavailable. Root-cause rules, SLO thresholds, risk classification, and approval requirements therefore remain in code.

The model's role is operator communication, not control authority.

## Why human approval exists

Actions such as draining a node, changing a power policy, adding external capacity, or materially scaling serving infrastructure have availability, cost, and blast-radius implications. The demo therefore preserves a visible approval boundary.

## Why Dynamo simulation is phase 2

Dynamo's simulation tooling creates a credible NVIDIA-native path to explore serving configurations without immediately consuming live GPU time. The PoC first proves the enterprise operating model, then integrates deeper simulation once the user is comfortable with the Dynamo workflow and its evolving experimental interfaces.

## Why not duplicate NVIDIA Mission Control

The project should be positioned as an **enterprise reasoning, policy, and decision-defense layer** that can consume NVIDIA infrastructure signals. It should not claim to replace or re-create NVIDIA's own infrastructure-management products.
