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
