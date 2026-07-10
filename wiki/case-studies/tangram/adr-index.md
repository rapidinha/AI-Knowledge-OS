# Tangram ADR Index

Navigable index of `docs/architecture/ADR-*.md` in the Tangram Platform source corpus.

## ADRs

| ADR | Status | Summary | Related wiki notes |
|-----|--------|---------|--------------------|
| `ADR-001-challenge-seasonal-temporal-orchestration.md` | Accepted | Introduces `ChallengeSeasonal` in Catalog as the temporal orchestration owner for seasonal challenges, with Learning enforcing participation policy and sessions. | [[principles/temporal-orchestration-of-content]], [[principles/content-distribution-by-channel]], [[case-studies/tangram/catalog-and-learning]] |
| `ADR-002-asaas-b2c-payment-integration.md` | In Progress | Chooses SQS-backed webhook ingestion, database idempotency, handler routing, public checkout hardening, and Localstack parity for B2C payment processing. | [[principles/webhook-ingestion-via-queues]], [[principles/bulk-import-via-command-queues]], [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] |
| `ADR-003-session-resume-time-is-money.md` | Implemented update log | Makes `POST /sessions/start` resumable/idempotent for timed sessions, with backend-owned remaining time and frontend resync from server state. | [[principles/timed-session-resume]], [[case-studies/tangram/catalog-and-learning]] |
| `ADR-004-challenge-engine.md` | Accepted | Consolidates challenge session lifecycle, time, pause/resume, abandonment, answer submission, and audit events into one backend/frontend challenge engine. | [[principles/timed-session-resume]], [[principles/temporal-orchestration-of-content]], [[case-studies/tangram/catalog-and-learning]] |
| `ADR-005-catalog-audit-system-evolution.md` | Proposed | Proposes evolving Catalog audit logs toward a cross-service event-driven audit pipeline with standardized audit events, retry/DLQ, trace metadata, and retention governance. | [[principles/architecture-decision-records]], [[principles/temporal-orchestration-of-content]], [[case-studies/tangram/catalog-and-learning]] |
| `ADR-006-user-lifecycle-lazy-expiration.md` | Accepted | Adds `statusExpiresAt` and lazy-only user lifecycle expiration at auth touchpoints instead of a scheduler or per-request identity revalidation. | [[principles/dual-channel-auth-jwt-and-service-credentials]], [[principles/pbac-scopes-in-tokens]], [[case-studies/tangram/identity-pbac-and-auth]] |
| `ADR-arc42-template.md` | Template | Provides the long-form arc42 decision-record structure for goals, constraints, context, building blocks, runtime, deployment, decisions, quality, and risks. | [[principles/architecture-decision-records]], [[case-studies/tangram/clients-dx-and-meta]] |

## Observations

- The ADR set is product-domain heavy: Catalog/Learning sessions, payment ingestion, audit evolution, and identity lifecycle dominate the documented decisions.
- Status matters. `ADR-005` is proposed and should not be treated as shipped behavior; `ADR-002` says in progress but source case-study evidence shows the service has evolved beyond the document with leases, stale-event guards, and Redis payload caching.
- The index supports [[principles/architecture-decision-records]] by making decision status, related implementation evidence, and downstream wiki notes explicit.

## Related

- [[case-studies/tangram/index]]
- [[case-studies/tangram/clients-dx-and-meta]]
- [[MOC/architecture]]
- [[MOC/engineering-practice]]
- [[_meta/coverage-matrix]]
