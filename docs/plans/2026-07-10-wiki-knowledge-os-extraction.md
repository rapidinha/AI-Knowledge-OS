# Wiki Knowledge OS Extraction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract portable engineering principles and Tangram case studies from the full Tangram Platform monorepo into an Obsidian-style wiki in AI-Knowledge-OS, with a coverage matrix and extraction ledger for subsequent waves.

**Architecture:** Dual-tree wiki (`principles/` zero-company; `case-studies/tangram/` evidence-backed) + MOCs + `_meta` ledger/matrix. Research source: `/Users/matheusborges/github/tangram-platform` (prefer `origin/main` in submodules). Infra case studies: `tangram-api-infra-prod/terraform-v2` only.

**Tech Stack:** Markdown + wikilinks; git in AI-Knowledge-OS; read-only research in tangram-platform.

**Spec:** `docs/specs/2026-07-10-wiki-knowledge-os-design.md`

---

## File structure (create)

- `README.md` — project purpose + how to navigate wiki
- `wiki/index.md` — entry hub
- `wiki/_meta/templates.md`
- `wiki/_meta/coverage-matrix.md`
- `wiki/_meta/extraction-ledger.md`
- `wiki/MOC/*.md` — seven MOCs from spec
- `wiki/principles/*.md` — one file per principle topic
- `wiki/case-studies/tangram/index.md` + `wiki/case-studies/tangram/*.md`

---

### Task 1: Scaffold wiki skeleton + templates + coverage matrix

**Files:**
- Create: `README.md`
- Create: `wiki/index.md`
- Create: `wiki/_meta/templates.md`
- Create: `wiki/_meta/coverage-matrix.md` (all topics `pending`)
- Create: `wiki/_meta/extraction-ledger.md` (empty wave log + instructions)
- Create: `wiki/MOC/{architecture,security-authz,data-persistence,async-scale,infrastructure,engineering-practice,product-domain}.md` (stub hubs)
- Create: `wiki/case-studies/tangram/index.md`
- Create: `wiki/principles/.gitkeep` if needed

**Work from:** `/Users/matheusborges/github/AI-Knowledge-OS`

- [ ] **Step 1:** Write `wiki/_meta/templates.md` with principle + case-study templates matching the spec
- [ ] **Step 2:** Write `coverage-matrix.md` listing every topic from the design spec Domain table as rows with columns: Topic | Domain | Wave | Status | Principle note | Case study note | Gaps
- [ ] **Step 3:** Stub all seven MOC files with title, purpose, empty `## Principles` / `## Case studies` link sections
- [ ] **Step 4:** Write `wiki/index.md` and root `README.md` explaining dual-tree rules
- [ ] **Step 5:** Init `extraction-ledger.md` with Wave protocol (what to append after each wave)
- [ ] **Step 6:** Commit: `docs: scaffold wiki skeleton, templates, and coverage matrix`

**Acceptance:** No principle/case content yet; matrix has all topics `pending`; templates enforceable.

---

### Task 2: Extract Auth / PBAC (research + notes)

**Source (read-only):**
- `tangram-platform/services/identity-service` @ `origin/main` (scopes seed, entities, auth/token/scope logic, cognito)
- `tangram-platform/libs/backend-common` @ `origin/main` (JwtAuthGuard, ScopesGuard, ApiKeyGuard, decorators)
- `tangram-platform/docs/architecture/service-accounts.md`
- `tangram-platform/docs/architecture/ADR-006-user-lifecycle-lazy-expiration.md`

**Files:**
- Create: `wiki/principles/pbac-scopes-in-tokens.md`
- Create: `wiki/principles/dual-channel-auth-jwt-and-service-credentials.md`
- Create: `wiki/principles/service-accounts-for-s2s.md`
- Create: `wiki/case-studies/tangram/identity-pbac-and-auth.md`
- Modify: MOC `security-authz.md`, coverage-matrix, extraction-ledger

**Work from:** AI-Knowledge-OS; research tangram-platform via absolute paths / `git show origin/main:...`

- [ ] **Step 1:** Research evidence; note facts vs hypotheses (especially `UserScope.contextType/contextId` usage)
- [ ] **Step 2:** Write three principle notes (no Tangram names)
- [ ] **Step 3:** Write Tangram case study with Evidence paths + Deviations
- [ ] **Step 4:** Update MOC, matrix (`extracted`/`partial`), ledger W1 bullet
- [ ] **Step 5:** Grep principles for forbidden strings: `Tangram`, `tangram`, `identity-service`, `Cognito` in principles only — Cognito may appear in case study; principles say "managed IdP"
- [ ] **Step 6:** Commit: `docs(wiki): extract auth and PBAC principles + Tangram case study`

---

### Task 3: Extract terraform-v2 infrastructure

**Source:**
- `tangram-platform/tangram-api-infra-prod/terraform-v2/` (README, main.tf, modules/*)
- Do **not** deep-dive `terraform/` v1

**Files:**
- Create: `wiki/principles/multi-env-terraform-single-state.md`
- Create: `wiki/principles/modular-iaas-boundaries.md`
- Create: `wiki/principles/ignore-changes-and-secret-hygiene-in-iac.md`
- Create: `wiki/case-studies/tangram/terraform-v2-platform.md`
- Modify: MOC infrastructure, matrix, ledger

- [ ] **Step 1:** Research module map and staging/prod `for_each` pattern
- [ ] **Step 2:** Write principle notes
- [ ] **Step 3:** Write case study (ECS, Cognito module, SQS olympiad, RDS Proxy, Cloudflare, Amplify)
- [ ] **Step 4:** Update MOC/matrix/ledger; commit: `docs(wiki): extract terraform-v2 principles + case study`

---

### Task 4: Extract Diplomat / layered service architecture

**Source:**
- `docs/SERVICE_STANDARDS.md`, `.cursor/rules/nestjs-architecture.mdc`
- Any service `src/{diplomat,controllers,logic,adapters,wire}`
- Note pragmatic escapes: enrollment `diplomat/queue`, learning `worker/`, rewards `src/services/` ranking cache

**Files:**
- Create: `wiki/principles/layered-io-boundaries-diplomat.md`
- Create: `wiki/principles/pure-domain-logic-no-io.md`
- Create: `wiki/case-studies/tangram/diplomat-architecture.md`
- Modify: MOC architecture, matrix, ledger

- [ ] Research + write principles + case study (include deviations)
- [ ] Update meta; commit: `docs(wiki): extract diplomat layered architecture`

---

### Task 5: Extract monorepo submodules + API contracts

**Source:**
- `.gitmodules`, README, `.github/workflows/*contract*`, Orval in apps
- `docs/USING_COMMON_LIB.md`, `libs/backend-common`

**Files:**
- Create: `wiki/principles/git-submodules-as-service-boundaries.md`
- Create: `wiki/principles/generated-api-clients-and-contract-ci.md`
- Create: `wiki/principles/shared-kernel-library-extraction.md`
- Create: `wiki/case-studies/tangram/monorepo-contracts-and-common.md`
- Modify: MOC engineering-practice + architecture, matrix, ledger

- [ ] Research + write; commit: `docs(wiki): extract monorepo and contract practices`

---

### Task 6: Extract Enrollment async (SQS / payments / olympiad import)

**Source:** `services/enrollment-service` queue/, ADR-002, demo-provisioning (brief), terraform-v2 sqs/asaas modules

**Files:**
- Create: `wiki/principles/webhook-ingestion-via-queues.md`
- Create: `wiki/principles/bulk-import-via-command-queues.md`
- Create: `wiki/case-studies/tangram/enrollment-sqs-asaas-olympiad.md`
- Modify: MOC async-scale + product-domain, matrix, ledger

- [ ] Research + write; commit: `docs(wiki): extract enrollment async patterns`

---

### Task 7: Extract Rewards ranking cache + wallet domain

**Source:** `services/rewards-service` ranking-cache*, wallet/prize entities, visibility

**Files:**
- Create: `wiki/principles/specialized-read-model-cache.md`
- Create: `wiki/principles/wallet-ledger-style-balances.md`
- Create: `wiki/case-studies/tangram/rewards-ranking-cache.md`
- Modify: MOC async-scale + product-domain, matrix, ledger

- [ ] Research + write; commit: `docs(wiki): extract rewards ranking cache and wallet`

---

### Task 8: Extract Catalog modeling + Learning sessions

**Source:** catalog entities/distributions/ADR-001/004/005; learning challenge-session/ADR-003/worker xlsx

**Files:**
- Create: `wiki/principles/content-distribution-by-channel.md`
- Create: `wiki/principles/temporal-orchestration-of-content.md`
- Create: `wiki/principles/timed-session-resume.md`
- Create: `wiki/principles/streaming-bulk-file-import-workers.md`
- Create: `wiki/case-studies/tangram/catalog-and-learning.md`
- Modify: MOCs data + product, matrix, ledger

- [ ] Research + write; commit: `docs(wiki): extract catalog and learning domain patterns`

---

### Task 9: Extract Notification, frontends, DX, agent/docs/CI meta

**Source:** notification providers; apps web/backoffice/mobile; Makefile/dev workflow; `.cursor/rules`; `.github`; `docs/`

**Files:**
- Create: `wiki/principles/pluggable-notification-providers.md`
- Create: `wiki/principles/multi-client-same-api-contracts.md`
- Create: `wiki/principles/local-dev-presets-without-full-docker.md`
- Create: `wiki/principles/agent-rules-as-living-standards.md`
- Create: `wiki/principles/architecture-decision-records.md`
- Create: `wiki/case-studies/tangram/clients-dx-and-meta.md`
- Modify: MOCs, matrix, ledger

- [ ] Research + write; commit: `docs(wiki): extract notification, clients, DX, and meta practices`

---

### Task 10: ADR sweep, hypothesis close-out, MOC polish, final ledger

**Source:** `docs/architecture/ADR-*`; prior hypotheses (CQRS, Event Sourcing, Kafka, Aggregate Root, ECS vs EKS)

**Files:**
- Create: `wiki/case-studies/tangram/adr-index.md`
- Modify: all MOCs (ensure links complete), coverage-matrix (no `pending` left), extraction-ledger (final summary + **Next extraction brief**)
- Modify: `wiki/index.md` if needed

- [ ] **Step 1:** For each ADR, ensure linked from case study or adr-index; extract any missing principle
- [ ] **Step 2:** Resolve hypotheses in ledger (confirm/reject/partial with confidence)
- [ ] **Step 3:** Zero `pending` in coverage-matrix
- [ ] **Step 4:** Write **Next extraction brief** section in ledger (what a future agent should do on a new repo or Tangram delta)
- [ ] **Step 5:** Commit: `docs(wiki): close coverage matrix and write extraction ledger summary`

---

## Verification (every content task)

1. Principles: no `Tangram|tangram-platform|*-service` company leakage (allow generic words like "JWT")
2. Case studies: at least 3 evidence paths each
3. Wikilinks resolve to existing notes or MOCs
4. Matrix + ledger updated in same commit

## Note on tests

This is a documentation wiki. "TDD" = write template compliance checklist first in Task 1; each later task verifies against templates + leakage grep before commit.
