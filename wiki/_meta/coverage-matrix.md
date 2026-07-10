# Coverage matrix

Tracks extraction status for every topic in the [design spec](../../docs/specs/2026-07-10-wiki-knowledge-os-design.md). Terminal statuses: `extracted`, `partial` (with gap note), `out-of-scope` (with reason). Initial state: all `pending`.

| Topic | Domain | Wave | Status | Principle note | Case study note | Gaps |
|-------|--------|------|--------|----------------|-----------------|------|
| Diplomat / layered I/O boundaries | Architecture | W1 | pending | — | — | — |
| Microservices + shared DB schemas | Architecture | W2 | pending | — | — | — |
| Git submodules monorepo | Architecture | W1 | pending | — | — | — |
| Shared auth library | Architecture | W1 | pending | — | — | — |
| Cognito + platform JWT | Security | W1 | pending | — | — | — |
| PBAC scopes | Security | W1 | pending | — | — | — |
| Service accounts / API keys | Security | W1 | pending | — | — | — |
| Contextual permissions | Security | W1 | pending | — | — | — |
| TypeORM entities / migrations | Data | W2 | pending | — | — | — |
| Lookup tables | Data | W2 | pending | — | — | — |
| Audit logs | Data | W2 | pending | — | — | — |
| Multi-channel content distribution | Data | W2 | pending | — | — | — |
| SQS webhooks & imports | Async / scale | W2 | pending | — | — | — |
| Redis cache | Async / scale | W2 | pending | — | — | — |
| Specialized read-model cache | Async / scale | W2 | pending | — | — | — |
| Workers / streaming imports | Async / scale | W2 | pending | — | — | — |
| terraform-v2 multi-env single state | Infra | W1 | pending | — | — | — |
| ECS / ALB / Cognito / SQS / RDS Proxy | Infra | W1 | pending | — | — | — |
| Feature flags (Unleash) | Infra | W3 | pending | — | — | — |
| Contract codegen + CI | Engineering | W1 | pending | — | — | — |
| Agent rules (`.cursor`) | Engineering | W3 | pending | — | — | — |
| Docs / ADRs | Engineering | W4 | pending | — | — | — |
| Automated-test seed scenarios | Engineering | W3 | pending | — | — | — |
| Observability | Engineering | W3 | pending | — | — | — |
| Challenge / session / resume | Product domain | W2 | pending | — | — | — |
| Olympiad cross-service | Product domain | W2 | pending | — | — | — |
| Enrollment / payment | Product domain | W2 | pending | — | — | — |
| Rewards / wallet / ranking | Product domain | W2 | pending | — | — | — |
| Notification channels | Product domain | W3 | pending | — | — | — |
| Frontends (web / admin / mobile) | Product domain | W3 | pending | — | — | — |

## Wave summary

| Wave | Focus |
|------|--------|
| W1 | Scaffold, Auth/PBAC, terraform-v2, Diplomat, contracts/monorepo |
| W2 | Enrollment async, Rewards ranking, Catalog, Learning |
| W3 | Notification, demo, frontends, DX, observability, `.cursor` / `.github` / `docs` |
| W4 | ADR sweep, hypothesis confirm/reject, coverage close-out |

## Status legend

| Status | Meaning |
|--------|---------|
| `pending` | Not yet extracted |
| `extracted` | Principle and case study complete per [[templates]] |
| `partial` | One side done or evidence thin — gap note required |
| `out-of-scope` | Explicitly excluded — reason required in Gaps column |
