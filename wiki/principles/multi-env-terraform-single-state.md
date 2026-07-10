# Multi-Environment IaC with a Single State

**When to use:** Use this pattern when multiple environments share the same topology and should be reviewed as one infrastructure release unit.

## Body

Model environments as data, not as copied root stacks. Keep a single environment map that captures per-environment names, hostnames, capacity, scaling limits, and feature toggles. Instantiate environment-scoped modules from that map so staging and production differ through inputs while sharing module code.

Keep shared primitives outside the environment loop when they are truly global: network foundations, encryption keys, certificate validation, and other account-level concerns. Environment-scoped modules should receive those shared outputs and produce their own persistence, identity, secrets, routing, compute, queues, storage, and deployment resources.

A single remote state with locking makes cross-environment changes visible in one plan. That is useful when a platform release intentionally changes both environments together, but it also means every plan can see and potentially touch both environments. Treat the state boundary as an operational boundary: small plans, explicit review, locked applies, and clear ownership of who may run them.

## Trade-offs

- One plan shows whether staging and production are drifting from the same declared topology.
- Shared modules reduce copy-paste and make environment parity easier to reason about.
- The state file becomes a larger blast-radius boundary.
- Environment-specific emergency changes are harder because unrelated drift can appear in the same plan.

## Anti-patterns

- Duplicating root stacks for each environment and then expecting them to stay aligned by convention.
- Mixing environment fan-out with ad hoc one-off resources that bypass the environment map.
- Treating a single state as permission to apply broad changes without reviewing which environment each resource belongs to.
- Hiding environment differences in scattered conditionals instead of naming them as inputs.

## Checklist for a new project

- [ ] Define the environment map before creating environment-scoped modules.
- [ ] Keep global resources outside the environment loop and pass their outputs explicitly.
- [ ] Use remote state with locking before more than one person can apply.
- [ ] Make production-only resources explicit with named toggles or environment checks.
- [ ] Review every plan by environment before applying.

## Case studies

- [[MOC/infrastructure]] — Evidence and implementation examples for this pattern.

## Related

- [[principles/modular-iaas-boundaries]]
- [[principles/ignore-changes-and-secret-hygiene-in-iac]]
- [[MOC/infrastructure]]
