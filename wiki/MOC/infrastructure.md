# Infrastructure

Hub for terraform-v2, ECS/ALB, managed services, and feature flags.

## Principles

- [[principles/multi-env-terraform-single-state]] — Manage environment fan-out from one locked infrastructure state.
- [[principles/modular-iaas-boundaries]] — Keep networking, persistence, identity, compute, routing, storage, async, and delivery concerns in clear modules.
- [[principles/ignore-changes-and-secret-hygiene-in-iac]] — Document lifecycle drift exceptions and keep secrets outside committed configuration.

## Case studies

- [[case-studies/tangram/terraform-v2-platform]] — Tangram terraform-v2 evidence for multi-env state, module boundaries, lifecycle exceptions, and secret handling.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
