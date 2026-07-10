# Architecture

Hub for structural patterns: service layering, monorepo layout, and cross-cutting libraries.

## Principles

- [[principles/layered-io-boundaries-diplomat]] — Separates transport, orchestration, domain logic, persistence, cache, and wire contracts.
- [[principles/pure-domain-logic-no-io]] — Keeps domain rules deterministic and free of infrastructure effects.
- [[principles/git-submodules-as-service-boundaries]] — Uses pinned nested repositories as explicit service, app, and library ownership boundaries.
- [[principles/shared-kernel-library-extraction]] — Extracts only stable cross-service primitives into a versioned shared package.
- [[principles/architecture-decision-records]] — Records durable technical decisions with status, context, rationale, consequences, and follow-ups.

## Case studies

- [[case-studies/tangram/diplomat-architecture]] — Tangram's Diplomat implementation and documented async/cache deviations.
- [[case-studies/tangram/monorepo-contracts-and-common]] — Tangram's submodule platform workspace, root contract checks, generated clients, and shared backend package.
- [[case-studies/tangram/clients-dx-and-meta]] — Tangram's brief ADR set, agent standards, and CI/review metadata.

## Related

- [[index]]
- [[MOC/engineering-practice]]
- [[_meta/coverage-matrix]]
