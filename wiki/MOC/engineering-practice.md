# Engineering practice

Hub for contracts, CI, agent rules, ADRs, test seeds, and observability.

## Principles

- [[principles/generated-api-clients-and-contract-ci]] — Keeps generated clients aligned with provider contracts through codegen and CI drift checks.
- [[principles/git-submodules-as-service-boundaries]] — Keeps routine service CI in owned repositories while the root workspace checks integration compatibility.

## Case studies

- [[case-studies/tangram/monorepo-contracts-and-common]] — Tangram's root contract workflows, generated clients, CODEOWNERS, PR checklist, and per-submodule CI split.

## Related

- [[index]]
- [[_meta/coverage-matrix]]
