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
