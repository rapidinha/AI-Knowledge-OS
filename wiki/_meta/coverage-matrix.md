# Coverage matrix

Tracks extraction status for every topic in the [design spec](../../docs/specs/2026-07-10-wiki-knowledge-os-design.md). Terminal statuses: `extracted`, `partial` (with gap note), `out-of-scope` (with reason). Initial state: all `pending`.

| Topic | Domain | Wave | Status | Principle note | Case study note | Gaps |
|-------|--------|------|--------|----------------|-----------------|------|
| Diplomat / layered I/O boundaries | Architecture | W1 | extracted | [[principles/layered-io-boundaries-diplomat]], [[principles/pure-domain-logic-no-io]] | [[case-studies/tangram/diplomat-architecture]] | — |
| Microservices + shared DB schemas | Architecture | W2 | pending | — | — | — |
| Git submodules monorepo | Architecture | W1 | extracted | [[principles/git-submodules-as-service-boundaries]] | [[case-studies/tangram/monorepo-contracts-and-common]] | — |
| Shared auth library | Architecture | W1 | extracted | [[principles/shared-kernel-library-extraction]], [[principles/dual-channel-auth-jwt-and-service-credentials]] | [[case-studies/tangram/monorepo-contracts-and-common]], [[case-studies/tangram/identity-pbac-and-auth]] | — |
| Cognito + platform JWT | Security | W1 | extracted | [[principles/dual-channel-auth-jwt-and-service-credentials]] | [[case-studies/tangram/identity-pbac-and-auth]] | — |
| PBAC scopes | Security | W1 | extracted | [[principles/pbac-scopes-in-tokens]] | [[case-studies/tangram/identity-pbac-and-auth]] | — |
| Service accounts / API keys | Security | W1 | extracted | [[principles/service-accounts-for-s2s]] | [[case-studies/tangram/identity-pbac-and-auth]] | — |
| Contextual permissions | Security | W1 | partial | [[principles/pbac-scopes-in-tokens]] | [[case-studies/tangram/identity-pbac-and-auth]] | `contextType`/`contextId` are modeled but not enforced by the shared scope guard; endpoint-level checks remain to map. |
| TypeORM entities / migrations | Data | W2 | pending | — | — | — |
| Lookup tables | Data | W2 | partial | [[principles/content-distribution-by-channel]] | [[case-studies/tangram/catalog-and-learning]] | Catalog lookup endpoints and cached stable codes mapped; a standalone generic lookup-table principle remains to extract. |
| Audit logs | Data | W2 | partial | [[principles/temporal-orchestration-of-content]] | [[case-studies/tangram/catalog-and-learning]] | Catalog release schedule audit/version snapshots and ADR-005 mapped; broader cross-service audit-log pattern remains to extract. |
| Multi-channel content distribution | Data | W2 | extracted | [[principles/content-distribution-by-channel]], [[principles/temporal-orchestration-of-content]] | [[case-studies/tangram/catalog-and-learning]] | — |
| SQS webhooks & imports | Async / scale | W2 | extracted | [[principles/webhook-ingestion-via-queues]], [[principles/bulk-import-via-command-queues]] | [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] | Requested `terraform-v2/modules/sqs` and `terraform-v2/modules/asaas-events` source paths were not available in `tangram-platform` `origin/main`; extraction cites service, ADR, and script evidence. |
| Redis cache | Async / scale | W2 | partial | [[principles/specialized-read-model-cache]] | [[case-studies/tangram/rewards-ranking-cache]] | Rewards ranking/visibility Redis caches extracted; broader Redis usage outside Rewards remains to map. |
| Specialized read-model cache | Async / scale | W2 | extracted | [[principles/specialized-read-model-cache]] | [[case-studies/tangram/rewards-ranking-cache]] | — |
| Workers / streaming imports | Async / scale | W2 | extracted | [[principles/bulk-import-via-command-queues]], [[principles/streaming-bulk-file-import-workers]] | [[case-studies/tangram/enrollment-sqs-asaas-olympiad]], [[case-studies/tangram/catalog-and-learning]] | — |
| terraform-v2 multi-env single state | Infra | W1 | extracted | [[principles/multi-env-terraform-single-state]] | [[case-studies/tangram/terraform-v2-platform]] | README says production uses RDS Proxy, while `main.tf` currently enables the proxy for every environment; documented in case-study deviations. |
| ECS / ALB / Cognito / SQS / RDS Proxy | Infra | W1 | extracted | [[principles/modular-iaas-boundaries]], [[principles/ignore-changes-and-secret-hygiene-in-iac]] | [[case-studies/tangram/terraform-v2-platform]] | README references `modules/asaas-webhook/main.tf`, while the current root uses `modules/asaas-events/main.tf`; documented in case-study deviations. |
| Feature flags (Unleash) | Infra | W3 | pending | — | — | — |
| Contract codegen + CI | Engineering | W1 | extracted | [[principles/generated-api-clients-and-contract-ci]] | [[case-studies/tangram/monorepo-contracts-and-common]] | Root contract checks observed for backoffice; web app has generated-client config but no matching root web contract workflow in researched root files. |
| Agent rules (`.cursor`) | Engineering | W3 | pending | — | — | — |
| Docs / ADRs | Engineering | W4 | pending | — | — | — |
| Automated-test seed scenarios | Engineering | W3 | pending | — | — | — |
| Observability | Engineering | W3 | pending | — | — | — |
| Challenge / session / resume | Product domain | W2 | extracted | [[principles/temporal-orchestration-of-content]], [[principles/timed-session-resume]] | [[case-studies/tangram/catalog-and-learning]] | — |
| Olympiad cross-service | Product domain | W2 | extracted | [[principles/bulk-import-via-command-queues]], [[principles/specialized-read-model-cache]], [[principles/content-distribution-by-channel]], [[principles/temporal-orchestration-of-content]], [[principles/timed-session-resume]] | [[case-studies/tangram/enrollment-sqs-asaas-olympiad]], [[case-studies/tangram/rewards-ranking-cache]], [[case-studies/tangram/catalog-and-learning]] | — |
| Enrollment / payment | Product domain | W2 | extracted | [[principles/webhook-ingestion-via-queues]], [[principles/bulk-import-via-command-queues]] | [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] | — |
| Rewards / wallet / ranking | Product domain | W2 | extracted | [[principles/specialized-read-model-cache]], [[principles/wallet-ledger-style-balances]] | [[case-studies/tangram/rewards-ranking-cache]] | — |
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
