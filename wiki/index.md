# Engineering Wiki

Portable, Obsidian-style engineering knowledge: reusable principles, optional public case studies, and maps of content.

For **this public repository**, the Obsidian vault root is the `wiki/` directory. Personal laboratories that consume this wiki use a separate private source of truth — see [GOVERNANCE.md](../GOVERNANCE.md).

## Dual-tree rules

| Tree | Allowed | Forbidden |
|------|---------|-----------|
| `wiki/principles/` | Generic names ("auth service", "user table") | Company names, repo names, service names, absolute paths, product brands |
| `wiki/case-studies/<name>/` | Named-system evidence when intentionally published | Secrets, copied source blobs, personal notes |

Cross-link with `[[wikilinks]]`: principles ↔ case studies ↔ MOCs.

## Start here

### Maps of content (MOCs)

- [[MOC/architecture]] — layering, monorepo, shared libraries
- [[MOC/security-authz]] — identity, JWT, PBAC, service accounts
- [[MOC/data-persistence]] — ORM, migrations, audit, content distribution
- [[MOC/async-scale]] — queues, cache, workers, imports
- [[MOC/infrastructure]] — IaC, multi-env, feature flags
- [[MOC/engineering-practice]] — contracts, CI, ADRs, observability
- [[MOC/product-domain]] — learning and product-shaped patterns

### Meta

- [[_meta/templates]] — required note structure
- [[_meta/coverage-matrix]] — topic coverage status
- [[_meta/extraction-ledger]] — change log for wiki waves

### Case studies

- See [[case-studies/README|case-studies hub]] — none published in this repository yet

## Design

Governance and lab boundaries: [GOVERNANCE.md](../GOVERNANCE.md)
