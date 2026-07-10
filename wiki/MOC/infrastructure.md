# Infrastructure

Hub for terraform-v2, ECS/ALB, managed services, and feature flags.

## Principles

- [[principles/multi-env-terraform-single-state]] — Manage environment fan-out from one locked infrastructure state.
- [[principles/modular-iaas-boundaries]] — Keep networking, persistence, identity, compute, routing, storage, async, and delivery concerns in clear modules.
- [[principles/ignore-changes-and-secret-hygiene-in-iac]] — Document lifecycle drift exceptions and keep secrets outside committed configuration.
- [[principles/event-capacity-overlay-on-baseline-autoscaling]] — Pre-warm and step-down capacity for known peak events without rewriting baseline sizing.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
