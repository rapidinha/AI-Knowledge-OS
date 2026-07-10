# Engineering Wiki

Portable, Obsidian-style engineering knowledge extracted from a real SaaS monorepo. Two trees, one index.

Obsidian vault root should be the `wiki/` directory.

## Dual-tree rules

| Tree | Allowed | Forbidden |
|------|---------|-----------|
| `wiki/principles/` | Generic names ("auth service", "user table") | Company names, repo names, service names, absolute paths, product brands |
| `wiki/case-studies/tangram/` | Service names, ADRs, repo-relative evidence paths | Secrets, Terraform state, copied source blobs |

Cross-link with `[[wikilinks]]`: principles ↔ case studies ↔ MOCs.

## Start here

### Maps of content (MOCs)

- [[MOC/architecture]] — layering, monorepo, shared libraries
- [[MOC/security-authz]] — identity, JWT, PBAC, service accounts
- [[MOC/data-persistence]] — ORM, migrations, audit, content distribution
- [[MOC/async-scale]] — queues, cache, workers, imports
- [[MOC/infrastructure]] — terraform-v2, ECS, feature flags
- [[MOC/engineering-practice]] — contracts, CI, ADRs, observability
- [[MOC/product-domain]] — learning, olympiad, enrollment, rewards, frontends

### Meta

- [[_meta/templates]] — required note structure (enforceable)
- [[_meta/coverage-matrix]] — topic × wave × status (30 topics, all `pending`)
- [[_meta/extraction-ledger]] — wave log and next-wave brief

### Case study hub

- [[case-studies/tangram/index]] — Tangram-specific evidence index

## Extraction waves

| Wave | Focus |
|------|--------|
| W1 | Scaffold, Auth/PBAC, terraform-v2, Diplomat, contracts/monorepo |
| W2 | Enrollment async, Rewards ranking, Catalog, Learning |
| W3 | Notification, demo, frontends, DX, observability, `.cursor` / `.github` / `docs` |
| W4 | ADR sweep, hypotheses, coverage close-out |

## Design spec

Full goals and constraints: [docs/specs/2026-07-10-wiki-knowledge-os-design.md](../docs/specs/2026-07-10-wiki-knowledge-os-design.md)
