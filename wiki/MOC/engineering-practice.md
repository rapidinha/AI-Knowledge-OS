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

## Case studies

- [[case-studies/tangram/monorepo-contracts-and-common]] — Tangram's root contract workflows, generated clients, CODEOWNERS, PR checklist, and per-submodule CI split.
- [[case-studies/tangram/reusable-pr-pipeline]] — Org reusable PR workflow, service callers, and the web app's sharded fork with the same patch gate.
- [[case-studies/tangram/clients-dx-and-meta]] — Tangram's clients, local dev presets, agent rules, GitHub metadata, and ADR set.
- [[case-studies/tangram/adr-index]] — Tangram's ADR inventory with status, summaries, and related wiki-note links.

## Related

- [[index]]
- [[MOC/product-domain]]
- [[MOC/architecture]]
- [[_meta/coverage-matrix]]
