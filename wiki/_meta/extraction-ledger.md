# Extraction ledger

Running log of knowledge-extraction waves. After each wave, append a new section at the bottom (newest last). Do not edit prior wave entries except to fix factual errors.

**Source corpus:** Tangram Platform monorepo (`tangram-platform`, branch `origin/main` unless noted)  
**Output:** This wiki (`AI-Knowledge-OS`)

---

## Wave protocol

When a wave completes, append a block with this shape:

```markdown
## Wave <N> — <YYYY-MM-DD>

**Scope:** <topics from coverage-matrix and any ad-hoc targets>

### Extracted

- [[principles/<slug>]] — <one-line summary>
- [[case-studies/tangram/<slug>]] — <one-line summary>

### Partial / gaps

- <topic>: <what is missing and why>

### Out of scope

- <topic>: <reason>

### Matrix updates

- <topic>: `pending` → `extracted` | `partial` | `out-of-scope`

### Next-wave brief

**Priority topics:**

1. <topic> — <why next>
2. <topic> — <why next>

**Hypotheses to confirm/reject:**

- <hypothesis>

**Risks / blockers:**

- <risk or none>
```

### Rules

1. Update [[coverage-matrix]] in the same commit as ledger append.
2. Every `extracted` row must link to both a principle note and a case study (or document exception in Gaps).
3. Principles must pass the no-leakage rule in [[templates]].
4. Case studies must include Evidence paths; no secrets or Terraform state.
5. Infra evidence uses **terraform-v2 only** (not legacy `terraform/`).

---

## Waves

<!-- Append new wave sections below. Wave 0 = scaffold only (Task 1). -->

## Wave 0 — 2026-07-10

**Scope:** Wiki skeleton, templates, coverage matrix, MOC stubs, dual-tree rules (no principle or case content yet).

### Extracted

- _(none — scaffold only)_

### Partial / gaps

- All 30 coverage-matrix topics remain `pending`.

### Out of scope

- _(none declared)_

### Matrix updates

- _(no status changes — all rows `pending`)_

### Next-wave brief

**Priority topics (W1):**

1. Diplomat / layered I/O boundaries — foundation for all service notes
2. Cognito + platform JWT + PBAC scopes — cross-cutting auth model
3. terraform-v2 multi-env single state — infra anchor (v2 only)
4. Contract codegen + CI + git submodules monorepo — engineering workflow baseline

**Hypotheses to confirm/reject:**

- Diplomat layers are consistently applied across NestJS services
- PBAC scopes map cleanly to backoffice vs product surfaces

**Risks / blockers:**

- None for W1 scaffold; source repo must be readable at `origin/main` paths

## Wave 1 — 2026-07-10

**Scope:** Auth/PBAC extraction: platform JWTs, dual-channel auth guards, PBAC scopes, service accounts, API keys, and contextual-permission gaps.

### Extracted

- [[principles/pbac-scopes-in-tokens]] — Token-embedded scope codes for fast PBAC checks, with contextual authorization caveats.
- [[principles/dual-channel-auth-jwt-and-service-credentials]] — One auth boundary for bearer JWT users and service credentials.
- [[principles/service-accounts-for-s2s]] — Service accounts with scoped API keys, revocation, hashing, and validation caches.
- [[case-studies/tangram/identity-pbac-and-auth]] — Tangram evidence for JWT issuance, shared guards, scope checks, service accounts, and API-key validation.

### Partial / gaps

- Shared auth library: auth guards, scope guard, decorator, strategy, and auth models were extracted; the broader shared package remains for the architecture wave.
- Contextual permissions: `expiresAt` is filtered before token issuance, but `contextType`/`contextId` are not represented in the shared `scopes[]` guard decision.
- Service-account IP constraints: `allowedIps` is modeled and documented, but the researched API-key validation path did not show enforcement.
- ADR-006 user lifecycle lazy expiration: file was not available in `origin/main` or `HEAD`; lifecycle behavior was cited from tracked controller code only.

### Out of scope

- Full user lifecycle extraction beyond the login/refresh auth touchpoints.

### Matrix updates

- Shared auth library: `pending` → `partial`
- Cognito + platform JWT: `pending` → `extracted`
- PBAC scopes: `pending` → `extracted`
- Service accounts / API keys: `pending` → `extracted`
- Contextual permissions: `pending` → `partial`

### Next-wave brief

**Priority topics:**

1. Diplomat / layered I/O boundaries — needed to frame service-specific notes consistently
2. terraform-v2 multi-env single state — W1 infra anchor with explicit v2-only evidence
3. Contract codegen + CI + git submodules monorepo — engineering workflow baseline

**Hypotheses to confirm/reject:**

- Contextual authorization may be enforced in endpoint-specific controllers outside the shared guard.
- Service-account `allowedIps` may be intended but not wired into API-key validation.

**Risks / blockers:**

- ADR-006 user lifecycle doc exists on disk but was not tracked in `origin/main` or `HEAD` during extraction.

## Wave 2 — 2026-07-10

**Scope:** terraform-v2 infrastructure extraction: multi-env single state, modular IaC boundaries, lifecycle drift exceptions, secret hygiene, ECS/ALB/Cognito/SQS/RDS Proxy, Cloudflare, Amplify admin, and New Relic notes.

### Extracted

- [[principles/multi-env-terraform-single-state]] — Environment fan-out from one locked IaC state.
- [[principles/modular-iaas-boundaries]] — Infrastructure modules aligned to ownership boundaries and composed by the root stack.
- [[principles/ignore-changes-and-secret-hygiene-in-iac]] — Secret ingress through local env files, managed secret storage, and documented lifecycle drift exceptions.
- [[case-studies/tangram/terraform-v2-platform]] — Tangram terraform-v2 evidence for remote state, `./tf`, `.env.example`, environment fan-out, module wiring, queues, hosted frontend CI, DNS, and observability.

### Partial / gaps

- terraform-v2 documentation drift: README says production uses RDS Proxy, while `main.tf` currently passes `enable_rds_proxy = true` for every environment.
- terraform-v2 documentation drift: README names `modules/asaas-webhook/main.tf`, while the current root module uses `modules/asaas-events/main.tf`.
- Observability wording drift: README describes New Relic as the active monitoring path and says the previous LGTM stack was removed, while `main.tf` still contains Grafana Cloud OTEL and deploy annotation code paths.

### Out of scope

- Legacy `terraform/` v1: explicitly excluded by task instructions.
- Feature flags: remained pending because this wave focused on terraform-v2 infrastructure, not the feature-flag runtime.

### Matrix updates

- terraform-v2 multi-env single state: `pending` → `extracted`
- ECS / ALB / Cognito / SQS / RDS Proxy: `pending` → `extracted`

### Next-wave brief

**Priority topics:**

1. Diplomat / layered I/O boundaries — needed to frame service-specific notes consistently.
2. Contract codegen + CI + git submodules monorepo — W1 engineering workflow baseline.
3. Feature flags — remaining infrastructure-adjacent topic with runtime behavior to map.

**Hypotheses to confirm/reject:**

- The README drift may be stale documentation rather than intentional infrastructure behavior.
- Grafana Cloud paths may be transitional observability code rather than the primary monitoring stack.

**Risks / blockers:**

- Source documentation and root Terraform code disagree in a few places; future infra changes should verify behavior from Terraform files, not README summaries alone.

## Wave 3 — 2026-07-10

**Scope:** Diplomat / layered I/O boundaries extraction: service layering, logic sandwich orchestration, pure logic, repositories, adapters, wire contracts, and documented async/cache deviations.

### Extracted

- [[principles/layered-io-boundaries-diplomat]] — Generic layered I/O boundary pattern for transport, orchestration, logic, persistence, cache, and wire contracts.
- [[principles/pure-domain-logic-no-io]] — Pure business rules without infrastructure effects.
- [[case-studies/tangram/diplomat-architecture]] — Tangram evidence for Diplomat layers, Catalog schedule flow, Enrollment queues, Learning workers, and Rewards ranking cache deviations.

### Partial / gaps

- Service source reads: service paths were available from each service repository's `origin/main`; the monorepo root `origin/main:path` did not contain those nested paths directly.

### Out of scope

- Broader shared auth library architecture remains covered by the existing partial architecture row and future architecture/engineering waves.

### Matrix updates

- Diplomat / layered I/O boundaries: `pending` → `extracted`

### Next-wave brief

**Priority topics:**

1. Contract codegen + CI — W1 engineering workflow baseline.
2. Git submodules monorepo — needed to clarify root repo versus service repo evidence paths.
3. Microservices + shared DB schemas — natural follow-up to service boundary extraction.

**Hypotheses to confirm/reject:**

- Queue and worker boundaries should be formalized as first-class Diplomat adapters rather than treated as service-specific exceptions.
- Specialized read-model caches may deserve a separate async/scale principle beyond the generic cache boundary.

**Risks / blockers:**

- Source evidence for service files should continue to use service-level `origin/main` when the monorepo root only tracks submodule pointers.

## Wave 4 — 2026-07-10

**Scope:** Monorepo and contract extraction: Git submodules as service/app/library boundaries, generated API clients, root contract CI, per-submodule CI ownership, and the shared backend kernel package.

### Extracted

- [[principles/git-submodules-as-service-boundaries]] — Root workspaces can pin independently owned nested repositories while reserving root checks for integration.
- [[principles/generated-api-clients-and-contract-ci]] — Generated clients and CI drift checks keep consumers aligned with provider contracts.
- [[principles/shared-kernel-library-extraction]] — Shared kernels should stay narrow, versioned, and package-bound.
- [[case-studies/tangram/monorepo-contracts-and-common]] — Tangram evidence for `.gitmodules`, root contract workflows, Orval configs, package scripts, per-service workflows, and `backend-common`.

### Partial / gaps

- Contract codegen + CI: root workflows validate backoffice generated clients and build compatibility; web has Orval scripts/config but no matching root web contract workflow in the researched root `.github/workflows` files.
- Contract service coverage: the researched backoffice contract workflows start identity, organization, enrollment, and catalog before generation; additional generated-client projects need owning workflow validation or root workflow extension.

### Out of scope

- Microservices + shared DB schemas: remains pending for a data/architecture wave beyond submodule and contract ownership.

### Matrix updates

- Git submodules monorepo: `pending` → `extracted`
- Shared auth library: `partial` → `extracted`
- Contract codegen + CI: `pending` → `extracted`

### Next-wave brief

**Priority topics:**

1. Microservices + shared DB schemas — natural continuation from submodule service boundaries.
2. TypeORM entities / migrations — needed to map persistence ownership and migration flow.
3. SQS webhooks & imports — async boundary evidence already appeared during Diplomat extraction.

**Hypotheses to confirm/reject:**

- Shared database schemas may be coordinated through service-level TypeORM entities and migrations rather than root-level database ownership.
- Async import and webhook workers may require their own boundary principle beyond HTTP contract CI.

**Risks / blockers:**

- Contract evidence is split across root workflows and submodule histories; future contract waves should keep using service-level `origin/main` when root paths are gitlinks.

## Wave 5 — 2026-07-10

**Scope:** Enrollment async extraction: SQS-backed Asaas payment webhooks, payment/subscription event idempotency, olympiad import command queues, Redis import payload cache, runtime queue guards, and demo-provisioning orchestration contrast.

### Extracted

- [[principles/webhook-ingestion-via-queues]] — Durable external webhook ingestion through a managed queue service, persisted idempotency claims, processing leases, and stale-event guards.
- [[principles/bulk-import-via-command-queues]] — Long-running imports split into bootstrap, orchestration, and chunk commands with small queue payloads and durable job status.
- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] — Tangram evidence for Asaas webhook SQS ingestion, webhook event leases, payment transitions, olympiad import queues, Redis payload cache, and runtime queue guards.

### Partial / gaps

- Workers / streaming imports: queue-backed olympiad import workers were extracted; non-queue streaming import workers remain for a later Learning/import wave.
- Olympiad cross-service: enrollment-side olympiad import orchestration was extracted; rewards/learning/catalog cross-service behavior remains to map.
- Requested terraform-v2 evidence: `terraform-v2/modules/sqs` and `terraform-v2/modules/asaas-events` were not available under `tangram-platform` `origin/main` or the source checkout during this task, so infra queue provisioning was not cited in the new case study.

### Out of scope

- Rewards ranking and wallet flows beyond the enrollment-side olympiad import entry points.
- Learning streaming imports, except as a future-work gap in the coverage matrix.

### Matrix updates

- SQS webhooks & imports: `pending` → `extracted`
- Workers / streaming imports: `pending` → `partial`
- Olympiad cross-service: `pending` → `partial`
- Enrollment / payment: `pending` → `extracted`

### Next-wave brief

**Priority topics:**

1. Rewards / wallet / ranking — follows olympiad import into ranking and award outcomes.
2. Learning streaming imports — completes the broader worker/streaming import matrix row.
3. Microservices + shared DB schemas — needed to clarify cross-service persistence boundaries.

**Hypotheses to confirm/reject:**

- Rewards consumes enrollment/olympiad outputs through explicit contracts rather than direct import-worker coupling.
- Learning VC imports use a different streaming-worker shape than Enrollment's command queues.

**Risks / blockers:**

- Infra queue provisioning could not be verified from `tangram-platform` `origin/main`; future infra-specific updates should use the infra source path that contains `terraform-v2`.

## Wave 6 — 2026-07-10

**Scope:** Rewards extraction: olympiad ranking read-model cache, ranking visibility cache, cache-isolation guardrails, wallet ledger balances, transaction statements, prize preferences, and prize distribution.

### Extracted

- [[principles/specialized-read-model-cache]] — Expensive user-facing reads served from bounded, periodically rebuilt projections with explicit miss behavior and guardrails.
- [[principles/wallet-ledger-style-balances]] — Product balances stored for fast reads while each mutation writes an auditable transaction ledger entry.
- [[case-studies/tangram/rewards-ranking-cache]] — Tangram evidence for Rewards ranking cache, visibility cache, guardrail tests, wallet transactions, and prize distribution.

### Partial / gaps

- Redis cache: Rewards ranking and ranking-visibility caches were extracted, but Redis usage outside Rewards remains to map before treating the broader cache topic as complete.
- Olympiad cross-service: Enrollment-side import orchestration and Rewards active ranking cache are mapped; Learning/Catalog olympiad behavior remains for a future cross-service wave.

### Out of scope

- Rewards code changes: this wave documented existing `origin/main` behavior only.
- Learning streaming imports and Catalog olympiad configuration beyond their future cross-service role.

### Matrix updates

- Redis cache: `pending` → `partial`
- Specialized read-model cache: `pending` → `extracted`
- Olympiad cross-service: remains `partial` with Rewards cache evidence added
- Rewards / wallet / ranking: `pending` → `extracted`

### Next-wave brief

**Priority topics:**

1. Learning streaming imports — completes the remaining worker/streaming import gap.
2. Microservices + shared DB schemas — clarifies service-owned schemas and cross-service persistence boundaries.
3. TypeORM entities / migrations — follows naturally from wallet, ranking, and transaction evidence.

**Hypotheses to confirm/reject:**

- Redis usage outside Rewards may be generic payload/session caching rather than specialized read models.
- Learning/Catalog olympiad behavior may complete the cross-service flow from enrollment import to ranking outcomes.

**Risks / blockers:**

- Rewards source is a submodule; future source evidence should keep using service-level `origin/main` paths when the monorepo root only exposes a gitlink.

## Wave 7 — 2026-07-10

**Scope:** Catalog and Learning extraction: challenge-seasonal temporal orchestration, trail/channel distribution, release schedules, lookups, session resume, unified session engine, VC XLSX streaming imports, and submission evaluation drafts.

### Extracted

- [[principles/content-distribution-by-channel]] — Content records separated from channel-specific distribution criteria and lookup-backed channel codes.
- [[principles/temporal-orchestration-of-content]] — Event windows, release calendars, regeneration previews, data-loss guards, and audit/version snapshots.
- [[principles/timed-session-resume]] — Backend-owned remaining time, idempotent session start, abandoned-session resume, and session lifecycle events.
- [[principles/streaming-bulk-file-import-workers]] — Spreadsheet/file imports processed as bounded validated chunks with row-level errors and chunk transactions.
- [[case-studies/tangram/catalog-and-learning]] — Tangram Catalog distribution/release/lookups and Learning session/import/evaluation evidence.

### Partial / gaps

- Lookup tables: Catalog lookup endpoints and cached stable codes were mapped, but a standalone generic lookup-table principle remains to extract.
- Audit logs: Catalog schedule audit/version snapshots and ADR-005 were mapped, but broader cross-service audit-log modeling remains for a later data/compliance wave.

### Out of scope

- Full TypeORM entities / migrations extraction beyond the entities needed to explain Catalog distribution, schedules, Learning sessions, and evaluations.
- Frontend challenge engine implementation details beyond ADR context.

### Matrix updates

- Lookup tables: `pending` → `partial`
- Audit logs: `pending` → `partial`
- Multi-channel content distribution: `pending` → `extracted`
- Workers / streaming imports: `partial` → `extracted`
- Challenge / session / resume: `pending` → `extracted`
- Olympiad cross-service: `partial` → `extracted`

### Next-wave brief

**Priority topics:**

1. TypeORM entities / migrations — complete the broader persistence model after this targeted Catalog/Learning entity slice.
2. Cross-service audit logs — turn ADR-005 and existing audit repositories into a generic audit principle.
3. Microservices + shared DB schemas — clarify when services query shared schemas directly versus through service APIs.

**Hypotheses to confirm/reject:**

- Lookup tables may deserve a small standalone principle focused on stable codes, seed data, cache invalidation, and generated client contracts.
- Catalog audit evolution may align with existing webhook/queue principles if audit events move to a broker-backed worker.

**Risks / blockers:**

- ADR-005 is proposed, not accepted, so future audit extraction should distinguish shipped behavior from target architecture.

## Wave 8 — 2026-07-10

**Scope:** Task 9 extraction: Notification providers and scheduling, web/backoffice/mobile clients, generated contracts, local dev presets, agent rules, GitHub metadata, contract workflows, PR template, CODEOWNERS, and brief ADR list.

### Extracted

- [[principles/pluggable-notification-providers]] — Generic channel-provider pattern for push, email, SMS, delivery attempts, metrics, and scheduled campaigns.
- [[principles/multi-client-same-api-contracts]] — Generic pattern for multiple clients sharing provider API contracts while adapting runtime URLs locally.
- [[principles/local-dev-presets-without-full-docker]] — Native/hybrid/full-stack preset pattern for faster monorepo development without requiring the full stack for every task.
- [[principles/agent-rules-as-living-standards]] — Repository-scoped agent rules with frontmatter, always-apply behavior, and explicit deprecation.
- [[principles/architecture-decision-records]] — Status-aware ADR pattern for context, decisions, consequences, and follow-ups.
- [[case-studies/tangram/clients-dx-and-meta]] — Tangram evidence for Notification providers, web/backoffice/mobile clients, DX presets, agent rules, GitHub workflows, and ADR files.

### Partial / gaps

- Docs / ADRs: brief governance and ADR file list extracted; full ADR index remains Task 10.
- Contract codegen + CI: new client evidence added, but the root contract workflows still directly gate backoffice only in researched files.

### Out of scope

- Full ADR index and per-ADR synthesis: deferred to Task 10 by task instruction.
- Observability extraction: web/backoffice Faro/New Relic references appeared in client/DX evidence but remain a separate pending topic.
- Automated-test seed scenarios: Notification seed endpoint evidence appeared but the broader topic remains pending.

### Matrix updates

- Agent rules (`.cursor`): `pending` → `extracted`
- Docs / ADRs: `pending` → `partial`
- Local dev presets / DX: added as `extracted`
- Notification channels: `pending` → `extracted`
- Frontends (web / admin / mobile): `pending` → `extracted`
- Contract codegen + CI: remains `extracted` with multi-client evidence added

### Next-wave brief

**Priority topics:**

1. Full ADR index — Task 10 should turn the brief ADR list into a navigable index.
2. Observability — client and infra references surfaced but were not extracted as a generic pattern.
3. Automated-test seed scenarios — Notification automated-test seed paths surfaced and should be mapped with other services.

**Hypotheses to confirm/reject:**

- Web contract validation may live in the app-level workflow rather than a root contract workflow.
- Notification scheduling failures may be intentionally best-effort or may need stronger campaign-state feedback.
- Mobile bridge logs may be development residue and should be audited before treating the bridge as production pattern evidence.

**Risks / blockers:**

- Source evidence includes provider-specific naming in Notification service code; the extracted principle intentionally generalizes those providers to avoid vendor lock-in.

## Wave 9 — 2026-07-10

**Scope:** Task 10 close-out: full ADR index, coverage-matrix terminal statuses, hypothesis resolution, MOC polish, README/navigation completion, and future extraction brief.

### Extracted

**Principle inventory now present:**

- [[principles/agent-rules-as-living-standards]] — Repository-scoped agent guidance as reviewable, deprecatable standards.
- [[principles/architecture-decision-records]] — Status-aware ADRs with context, decisions, consequences, follow-ups, and implementation links.
- [[principles/bulk-import-via-command-queues]] — Long-running imports split into queue commands and bounded chunks.
- [[principles/content-distribution-by-channel]] — Content separated from channel-specific distribution criteria.
- [[principles/dual-channel-auth-jwt-and-service-credentials]] — One auth boundary for user JWTs and service credentials.
- [[principles/generated-api-clients-and-contract-ci]] — Generated clients backed by contract drift checks.
- [[principles/git-submodules-as-service-boundaries]] — Root workspace as integration layer for independently owned submodules.
- [[principles/ignore-changes-and-secret-hygiene-in-iac]] — Secret ingress outside committed config plus documented lifecycle drift exceptions.
- [[principles/layered-io-boundaries-diplomat]] — Transport, orchestration, logic, persistence, cache, and wire-contract boundaries.
- [[principles/local-dev-presets-without-full-docker]] — Native/hybrid/full-stack local presets to avoid mandatory full Docker startup.
- [[principles/modular-iaas-boundaries]] — Infrastructure modules aligned to ownership boundaries.
- [[principles/multi-client-same-api-contracts]] — Web, admin, mobile, and partner clients sharing provider API contracts.
- [[principles/multi-env-terraform-single-state]] — Environment fan-out from one locked infrastructure state.
- [[principles/pbac-scopes-in-tokens]] — Token-embedded PBAC scope codes with contextual-permission caveats.
- [[principles/pluggable-notification-providers]] — Channel/provider notification delivery plus scheduler boundaries.
- [[principles/pure-domain-logic-no-io]] — Deterministic domain rules kept free of I/O.
- [[principles/service-accounts-for-s2s]] — Scoped service accounts and hashed API keys for service-to-service access.
- [[principles/shared-kernel-library-extraction]] — Narrow, versioned shared backend primitives.
- [[principles/specialized-read-model-cache]] — Expensive active reads served from explicit warmed projections.
- [[principles/streaming-bulk-file-import-workers]] — Spreadsheet/file imports parsed and persisted as bounded validated chunks.
- [[principles/temporal-orchestration-of-content]] — Product content released through event windows, calendars, and audit/version snapshots.
- [[principles/timed-session-resume]] — Backend-owned remaining time and idempotent resumable sessions.
- [[principles/wallet-ledger-style-balances]] — Fast wallet balance snapshots paired with transaction-ledger writes.
- [[principles/webhook-ingestion-via-queues]] — External webhook receipt decoupled from durable internal processing.

**Tangram case-study inventory now present:**

- [[case-studies/tangram/adr-index]] — All `docs/architecture/ADR-*.md` files indexed with status, one-line summary, and related wiki links.
- [[case-studies/tangram/catalog-and-learning]] — Catalog temporal/distribution modeling, Learning sessions, VC imports, and audit ADR evidence.
- [[case-studies/tangram/clients-dx-and-meta]] — Notification providers, client contracts, DX presets, agent rules, GitHub metadata, partial seed/observability evidence, and ADR links.
- [[case-studies/tangram/diplomat-architecture]] — Diplomat layers, logic sandwich, pure logic, and async/cache deviations.
- [[case-studies/tangram/enrollment-sqs-asaas-olympiad]] — Asaas webhook queues, idempotency, leases, SQS workers, Redis payload cache, and olympiad imports.
- [[case-studies/tangram/identity-pbac-and-auth]] — JWT auth, PBAC scopes, service accounts, API keys, contextual-scope limitations, and ADR-006 lifecycle behavior.
- [[case-studies/tangram/monorepo-contracts-and-common]] — Submodule boundaries, generated clients, contract CI, and `backend-common`.
- [[case-studies/tangram/rewards-ranking-cache]] — Ranking/visibility read-model caches, wallet ledger transactions, and prize distribution.
- [[case-studies/tangram/terraform-v2-platform]] — terraform-v2 state, modules, ECS/ALB/Cognito/SQS/RDS Proxy, secret handling, and observability drift.

### Hypotheses resolved

- **CQRS formal:** Rejected with high confidence. The wiki found specialized read models and generated contracts, but no formal CQRS vocabulary, command/query segregation framework, or separate write/read model architecture.
- **Event Sourcing:** Rejected as a platform-wide claim with high confidence; partial as local event-history/audit language. ADR-002 uses "event sourcing" wording for payment events, and the codebase has webhook events, session events, transactions, and proposed audit events, but no full event-sourced aggregate replay model.
- **Aggregate Root explicit:** Rejected with high confidence. No explicit aggregate-root terminology or DDD aggregate boundary was found in ADRs or wiki-backed source evidence.
- **Kafka vs SQS:** Resolved with high confidence for shipped webhook/import paths: SQS is the accepted/implemented queue. For future audit evolution, ADR-005 leaves broker choice open across Kafka/SQS/Rabbit/Kinesis.
- **Multi-DB physical vs schemas:** Resolved with medium-high confidence as schema-separated services on shared PostgreSQL/Aurora infrastructure, not clearly separate physical databases per service. ADR-001 says shared DB schemas and no cross-schema queries for that flow; ADR-006 names separate PostgreSQL schemas; terraform-v2 maps one database module per environment.
- **Diplomat 100% consistent:** Rejected with high confidence. The core HTTP/controller/logic/repository/wire pattern is strong, but queue consumers, streaming workers, ranking caches, seasonal logic I/O, and heavy schedule controllers are documented deviations.
- **ECS vs EKS coexistence:** Rejected with high confidence for researched evidence. terraform-v2 evidence shows ECS Fargate, ALB, Lambda/event modules, Amplify, and related AWS services; no EKS/Kubernetes implementation surfaced beyond package-lock noise.
- **Outbox pattern:** Rejected with medium-high confidence. The platform uses SQS producers/consumers, idempotency rows, leases, transactionally updated state, and proposed audit producers, but no transactional outbox table/dispatcher pattern was found.
- **UserScope `contextType`/`contextId` enforcement:** Resolved with high confidence as partial. `UserScope` stores `contextType` and `contextId`, and `expiresAt` is filtered before token issuance, but `UserRepository.findUserScopes` returns only scope codes and the shared `ScopesGuard` checks only `request.user.scopes`.

### Partial / gaps

- Microservices + shared DB schemas: service ownership, schema-level coupling, and cross-schema reads are documented, but no standalone physical-DB-versus-schema principle was extracted.
- TypeORM entities / migrations: representative entity/repository/migration/transaction evidence is distributed across service case studies; no complete TypeORM migration inventory was extracted.
- Lookup tables: Catalog lookup endpoints and stable codes are mapped; no generic lookup-table principle exists yet.
- Audit logs: Catalog audit snapshots and ADR-005 are mapped; no shipped cross-service audit principle exists yet.
- Redis cache: Rewards read models are extracted; Redis use outside Rewards remains only partially mapped.
- Automated-test seed scenarios: source evidence exists for automated-test scopes, modules, and deterministic seeds; no standalone note was extracted.
- Observability: New Relic/Faro/metrics evidence is scattered across infra, clients, shared packages, and services; no standalone observability principle was extracted.
- Contextual permissions: context fields are modeled but not enforced by the shared guard.

### Out of scope

- Feature flags (Unleash): no Unleash implementation was found in the researched source; only ad-hoc or optional feature-gate references surfaced.
- Legacy `terraform/` v1: excluded throughout in favor of terraform-v2 evidence.
- New source extraction beyond Task 10 ADR/matrix close-out: this wave did not create new standalone principles for seeds, observability, TypeORM inventory, or lookup tables.

### Matrix updates

- Microservices + shared DB schemas: `pending` → `partial`
- TypeORM entities / migrations: `pending` → `partial`
- Feature flags (Unleash): `pending` → `out-of-scope`
- Docs / ADRs: `partial` → `extracted`
- Automated-test seed scenarios: `pending` → `partial`
- Observability: `pending` → `partial`
- Coverage matrix invariant: no topic rows remain `pending`.

### Next extraction brief

**If extracting future Tangram deltas:**

1. Start from [[_meta/coverage-matrix]] and only reopen `partial` topics when the source delta contains material new evidence; do not create compatibility shims for stale branch work.
2. For each delta, update the matching case study first, then decide whether the evidence deserves a new generic principle. Keep principles company-agnostic and move Tangram service names, paths, ADR names, and vendor details into case studies.
3. Priority Tangram gaps: automated-test seed scenarios, observability, TypeORM/migration inventory, generic lookup-table governance, cross-service audit implementation if ADR-005 becomes accepted/shipped, and any real feature-flag implementation if Unleash or another flag service appears.
4. Re-check ADR statuses before citing them. Proposed or in-progress ADRs can explain intent, but shipped behavior should be grounded in source paths or accepted ADRs.
5. Preserve the hypothesis ledger pattern: for each claimed architecture style, state confirmed/partial/rejected plus confidence and evidence path family.

**If extracting a different company's repository using this wiki as latent knowledge:**

1. Treat this wiki as a pattern vocabulary, not a template to force-fit. Use existing principles as candidate labels only after evidence supports them.
2. Build a fresh coverage matrix for that company, then map each topic to `extracted`, `partial`, or `out-of-scope` with a gap/reason. Never leave terminal extraction rows as `pending`.
3. Keep the dual-tree rule: generic reusable knowledge belongs in `wiki/principles/`; company names, product names, repo paths, ADR ids, vendors, and operational caveats belong in `wiki/case-studies/<company>/`.
4. Prefer small case studies around real execution flows over broad architecture summaries. Each case study should cite paths, note deviations, and link to the generic principles it supports or bends.
5. When comparing to Tangram, write contrast explicitly: "same pattern", "different implementation", or "not present"; do not imply that absence of evidence is evidence of absence unless searches covered the relevant code/docs.

### Risks / blockers

- Some matrix rows are intentionally `partial` because Task 10 closed the wiki state rather than performing new deep extraction for every leftover topic.
- `ADR-002` and `ADR-005` statuses require care: source evidence may be newer than ADR-002's in-progress text, while ADR-005 remains proposed.

## Wave 10 — 2026-07-10

**Scope:** Delta extraction for the organization reusable PR Pipeline (`workflow_call`) with static checks, tests+coverage, and patch-coverage gate; consumer call sites; web fork.

### Extracted

- [[principles/reusable-pr-ci-with-patch-coverage]] — Callable PR CI with parameterized scripts, optional integration/test skips, artifact upload, and patch-coverage merge gate with PR comment.
- [[case-studies/tangram/reusable-pr-pipeline]] — `TangramEd/.github/.github/workflows/pr.yml` inputs/jobs; callers in catalog/enrollment/learning/organization/rewards/backoffice; web custom sharded Vitest + `diff-cover` at 80%.

### Partial / gaps

- Integration test lane in the reusable workflow is widely skipped (`skip-integration: true`) pending testcontainers/schema standardization across services.
- Org workflow source lives outside the platform monorepo (`.github` org repo); evidence for the YAML body was provided from the maintained workflow definition plus in-repo callers.

### Matrix updates

- Reusable PR CI + patch coverage: _(new row)_ → `extracted`

### Next-wave brief

**Priority topics:**

1. Re-enable integration tests in reusable PR callers once schema/testcontainers setup is shared.
2. Reconcile web custom PR CI with org workflow when shared workflow gains skip-DB / sharding inputs.
3. Continue prior partials: observability, automated-test seeds, TypeORM inventory.

**Hypotheses to confirm/reject:**

- Whether identity-service (and any other submodule) still calls the org reusable workflow or has a local variant not present in this workspace checkout.

**Risks / blockers:**

- None for this delta; do not treat the pasted workflow as a file inside `tangram-platform` — cite org path + local callers.

