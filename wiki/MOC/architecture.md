# Architecture

Hub for structural patterns: service layering, monorepo layout, and cross-cutting libraries.

## Principles

- [[principles/layered-io-boundaries-diplomat]] — Separates transport, orchestration, domain logic, persistence, cache, and wire contracts.
- [[principles/pure-domain-logic-no-io]] — Keeps domain rules deterministic and free of infrastructure effects.

## Case studies

- [[case-studies/tangram/diplomat-architecture]] — Tangram's Diplomat implementation and documented async/cache deviations.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
