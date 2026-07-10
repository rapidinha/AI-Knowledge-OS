# Engineering practice

Hub for contracts, CI, agent rules, ADRs, test seeds, and observability.

## Principles

- [[principles/generated-api-clients-and-contract-ci]] — Keeps generated clients aligned with provider contracts through codegen and CI drift checks.
- [[principles/git-submodules-as-service-boundaries]] — Keeps routine service CI in owned repositories while the root workspace checks integration compatibility.
- [[principles/multi-client-same-api-contracts]] — Keeps web, admin, mobile, and partner clients aligned to the same provider API shapes.
- [[principles/local-dev-presets-without-full-docker]] — Keeps local development fast with declarative native, hybrid, and full-stack presets.
- [[principles/agent-rules-as-living-standards]] — Keeps repository agent guidance scoped, reviewable, and deprecatable.
- [[principles/architecture-decision-records]] — Keeps durable technical decisions tied to status, context, consequences, and follow-ups.
- [[principles/reusable-pr-ci-with-patch-coverage]] — Shared callable PR pipeline with static checks, tests, and a patch-coverage merge gate.
- [[principles/deterministic-seed-scenarios-with-cleanup]] — Named seed scenarios with execute + delete-plan for QA teardown.
- [[principles/named-rate-limit-profiles]] — Named throttle profiles as engineering convention across services.

## Related

- [[index]]
- [[MOC/product-domain]]
- [[MOC/architecture]]
- [[_meta/coverage-matrix]]
