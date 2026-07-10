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
