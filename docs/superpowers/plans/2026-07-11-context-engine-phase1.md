# Context Engine Phase 1 (Restructuring) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the public repository as a Protocol Kernel Context Engine (institutional docs, wiki scaffold, contracts/engine stubs, agent/provider layout, CI, instance sync policy) while leaving the maintainer’s private wiki and knowledge untouched.

**Architecture:** Work exclusively in a clean git worktree from `upstream/main` on `feature/public/context-engine-phase1`. OSS becomes framework-only: empty wiki scaffold + contracts + engine docs + agents/providers layout. Private SoT keeps living `wiki/` (principles, case studies). Sync script merges framework paths without overwriting instance wiki files.

**Tech Stack:** Git worktrees; Markdown docs; Python 3.11+ (existing radar package relocate); pytest; GitHub Actions boundary-check; portable agent skills (Cursor/Claude copies).

**Spec:** [`docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md`](../specs/2026-07-11-context-engine-repositioning-design.md)

**Out of scope (separate plans):** Phase 2 Research engine, Phase 3 Trend Radar productization beyond relocate, Phases 4–6 Content/Learning/full Context Engine metrics.

**Hard rules:**

1. **Never** delete, empty, or overwrite `wiki/` inside the private laboratory SoT as part of this work.
2. Wiki scaffold wipe runs **only** in the public worktree branched from `upstream/main`.
3. No personal principles, case studies, journals, or Tangram content in the public PR.
4. Stay tool-agnostic in all new docs (Obsidian/Cursor/Claude = optional adapters only).
5. Do not push to `main`; open PR to `rapidinha/AI-Knowledge-OS` via public contribution fork when ready.

---

## File structure (lock this first)

### Public worktree target layout

```text
AI-Knowledge-OS/                          # feature/public/context-engine-phase1
├── README.md                             # rewrite — Context Engine
├── VISION.md                             # new
├── MISSION.md                            # new
├── ARCHITECTURE.md                       # new
├── CONTRIBUTING.md                       # rewrite
├── GOVERNANCE.md                         # rewrite — OSS vs instance
├── ROADMAP.md                            # new
├── FAQ.md                                # new
├── GLOSSARY.md                           # new
├── AGENTS.md                             # rewrite — Always/Never + wiki preserve
├── LICENSE                               # keep
│
├── docs/
│   ├── index.md                          # new — Documentation Index
│   ├── getting-started.md                # new
│   ├── cycle.md                          # new
│   ├── maintenance.md                    # new
│   ├── specs/                            # keep existing + add pointer to repositioning spec
│   ├── plans/                            # keep
│   ├── radar/                            # keep; add note “reference provider docs”
│   └── superpowers/                      # specs/plans (include this plan + design)
│
├── contracts/
│   ├── README.md
│   ├── signal.md
│   ├── research-brief.md
│   ├── synthesis.md
│   ├── knowledge-entry.md
│   ├── insight.md
│   ├── decision-log.md
│   ├── content-brief.md
│   └── learning-update.md
│
├── engine/
│   ├── README.md
│   ├── cycle.md
│   └── invariants.md
│
├── wiki/                                 # SCAFFOLD ONLY on public tree
│   ├── index.md
│   ├── _meta/
│   │   ├── templates.md                  # expanded category templates
│   │   ├── governance.md                 # wiki KB rules
│   │   └── .gitkeep
│   ├── principles/.gitkeep
│   ├── case-studies/README.md            # empty hub
│   ├── architecture/.gitkeep
│   ├── rfcs/.gitkeep
│   ├── adrs/.gitkeep
│   ├── playbooks/.gitkeep
│   ├── research/.gitkeep
│   ├── learning-paths/.gitkeep
│   ├── trend-analysis/.gitkeep
│   ├── content-ideas/.gitkeep
│   └── decision-logs/.gitkeep
│
├── research/
│   └── README.md                         # scaffold only (CI-enforced)
│
├── prompts/
│   └── README.md
│
├── agents/
│   ├── README.md
│   ├── trend-radar/
│   │   ├── README.md
│   │   └── SKILL.md                      # moved from skills/leverage-radar
│   ├── research/README.md                # stub role
│   ├── knowledge-curator/README.md
│   ├── learning-coach/README.md
│   ├── content-strategist/README.md
│   ├── engineering-analyst/README.md
│   └── documentation-maintainer/README.md
│
├── providers/
│   ├── README.md
│   └── signals/                          # former radar/ package
│       ├── README.md
│       ├── __init__.py
│       ├── schema/
│       ├── lib/
│       ├── sources/                      # former radar/providers/
│       ├── fixtures/
│       └── fetch_enabled.py              # update imports
│
├── integrations/
│   └── README.md                         # adapters are optional
│
├── templates/
│   ├── instance/                         # renamed from personal-lab/
│   │   ├── README.md
│   │   ├── LAB.md
│   │   ├── scripts/
│   │   │   └── sync-from-upstream.sh     # instance wiki wins
│   │   └── …                             # knowledge/, notes/, etc. scaffolds
│   └── radar/                            # keep; paths updated to providers.signals
│
├── examples/
│   └── README.md                         # sanitized demos only
│
├── assets/
│   └── README.md
│
├── skills/                               # thin redirect README → agents/trend-radar
│   └── README.md
│
├── tests/
│   ├── providers/signals/                # moved from tests/radar/
│   ├── test_boundary_scaffold.py         # new — research/ + wiki scaffold rules
│   └── test_sync_policy.md               # or shell test for sync script dry-run
│
├── .cursor/skills/trend-radar/SKILL.md   # sync from agents/trend-radar
├── .claude/skills/trend-radar/SKILL.md
└── .github/
    ├── workflows/boundary-check.yml      # allow scaffold research/; forbid full wiki content heuristics
    └── PULL_REQUEST_TEMPLATE.md          # framework-oriented
```

### Private SoT (do not modify wiki content in this plan)

```text
(private-lab)/
├── wiki/                    # KEEP AS-IS — living KB
├── knowledge/, notes/, journals/, research/, experiments/
├── LAB.md
└── (later) pull framework via templates/instance/scripts/sync-from-upstream.sh
```

### Python import rename map

| Before | After |
|--------|--------|
| `radar.lib.*` | `providers.signals.lib.*` |
| `radar.providers.*` | `providers.signals.sources.*` |
| `radar/providers/fetch_enabled.py` | `providers/signals/fetch_enabled.py` |
| `tests/radar/` | `tests/providers/signals/` |
| `python radar/providers/fetch_enabled.py` | `python -m providers.signals.fetch_enabled` or `python providers/signals/fetch_enabled.py` |

---

### Task 0: Create isolated public worktree

**Files:** none in private SoT wiki

- [ ] **Step 1: Fetch upstream and create worktree**

```bash
cd /Users/matheusborges/github/AI-Knowledge-OS
git fetch upstream
git worktree add .worktrees/context-engine-phase1 -b feature/public/context-engine-phase1 upstream/main
cd .worktrees/context-engine-phase1
git status
```

Expected: clean worktree on `feature/public/context-engine-phase1`; root has `wiki/`, `radar/`, `docs/` — **no** `knowledge/`, `journals/` at root.

- [ ] **Step 2: Confirm you are NOT in the private lab root**

```bash
pwd
test ! -d knowledge && test ! -d journals && echo "OK: public-shaped tree"
ls wiki/principles | head
```

Expected: `OK: public-shaped tree`; principles list from upstream (will be removed later **in this worktree only**).

- [ ] **Step 3: Copy design + this plan into the worktree if missing**

If `docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md` is not on `upstream/main` yet, copy from the private SoT (sanitized — these files are public-safe):

```bash
mkdir -p docs/superpowers/specs docs/superpowers/plans
cp /Users/matheusborges/github/AI-Knowledge-OS/docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md docs/superpowers/specs/
cp /Users/matheusborges/github/AI-Knowledge-OS/docs/superpowers/plans/2026-07-11-context-engine-phase1.md docs/superpowers/plans/
git add docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md docs/superpowers/plans/2026-07-11-context-engine-phase1.md
git commit -m "$(cat <<'EOF'
docs: add Context Engine repositioning spec and Phase 1 plan

EOF
)"
```

---

### Task 1: Scaffold directory tree (empty shells)

**Files:**
- Create: `contracts/README.md`, `engine/README.md`, `prompts/README.md`, `integrations/README.md`, `examples/README.md`, `assets/README.md`, `agents/README.md`, `providers/README.md`, `research/README.md`

- [ ] **Step 1: Create directories and README stubs**

```bash
cd .worktrees/context-engine-phase1
mkdir -p contracts engine prompts integrations examples assets agents providers research
```

Write `contracts/README.md`:

```markdown
# Contracts

Canonical artifact schemas for the AI Knowledge OS Protocol Kernel.

Each file defines an artifact type that providers and agents emit or consume.
Contracts evolve via RFC; breaking changes require a major version note in the contract file.

See [ARCHITECTURE.md](../ARCHITECTURE.md) and [engine/cycle.md](../engine/cycle.md).
```

Write `engine/README.md`:

```markdown
# Engine

Protocol definitions for the closed loop:

**capture → contextualize → decide → learn → produce**

There is no mandatory runtime. Adapters and agents execute this protocol.
```

Write `research/README.md`:

```markdown
# Research (scaffold)

Working research notes for an **instance** belong in the private instance tree after copy from `templates/instance/`.

On the public repository this directory must remain scaffold-only (`README.md` and optional `.gitkeep`).
Durable research memory lives under `wiki/research/` in the instance Knowledge Base.
```

Write `prompts/README.md`:

```markdown
# Prompts

Versioned prompt fragments tied to contracts and agent packs.

Keep prompts tool-agnostic. Do not hardcode a vendor model name as a requirement.
```

Write `integrations/README.md`:

```markdown
# Integrations (optional adapters)

Adapters for specific tools (Cursor, Claude Code, CLIs, editors) live here.

No adapter is required to use the Protocol Kernel.
```

Write `examples/README.md`:

```markdown
# Examples

Sanitized demos of the closed loop. Never copy a maintainer’s private vault here.
```

Write `assets/README.md`:

```markdown
# Assets

Diagrams and static assets for institutional documentation.
```

Write `agents/README.md`:

```markdown
# Agents

Portable skill packs. Each agent declares which contracts it consumes and emits.
See role stubs in subdirectories and [docs/cycle.md](../docs/cycle.md).
```

Write `providers/README.md`:

```markdown
# Providers

Reference implementations that emit contract artifacts (especially Signals).

The Protocol Kernel does not depend on any single provider. See `signals/` for the Leverage Radar reference provider.
```

- [ ] **Step 2: Commit**

```bash
git add contracts engine prompts integrations examples assets agents providers research
git commit -m "$(cat <<'EOF'
chore: scaffold Protocol Kernel top-level directories

EOF
)"
```

---

### Task 2: Institutional vision docs

**Files:**
- Create: `VISION.md`, `MISSION.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `FAQ.md`, `GLOSSARY.md`

- [ ] **Step 1: Write `VISION.md`**

```markdown
# Vision

AI Knowledge OS is a **Context Engine** for technology professionals: an open-source Protocol Kernel that turns dispersed market and technical signals into actionable context, then closes the loop through learning and production.

## 5–10 year north star

- Any compatible agent or tool can execute the cycle using stable contracts.
- Each user runs a sovereign **instance** whose wiki is long-term memory.
- Providers, models, and UIs are replaceable without changing the product essence.
- Success is a measurable closed loop: signals become decisions, learning, and shipped work — not a larger pile of notes.

## What we refuse to become

- A PKM product identity
- A hosted personal-wiki SaaS
- A news aggregator
- A single-vendor agent framework
```

- [ ] **Step 2: Write `MISSION.md`**

```markdown
# Mission

Help technology professionals continuously answer questions they have not asked yet — but should — by producing **context**, not merely collecting information.

## Problem

Too much information. Too little context. Attention is the scarce resource.

## Promise

A recurring system that surfaces what deserves attention, what changed, what to study, and how to turn learning into content, projects, or professional growth — while keeping the user’s knowledge sovereign.
```

- [ ] **Step 3: Write `ARCHITECTURE.md`**

```markdown
# Architecture

AI Knowledge OS is a **Protocol Kernel**.

## Layers

| Layer | Role | Replaceable? |
|-------|------|--------------|
| Contracts | Artifact schemas | No (versioned) |
| Engine cycle | capture → contextualize → decide → learn → produce | No |
| Wiki schema | Knowledge Base categories + templates | Via RFC |
| Agents | Skill packs | Yes |
| Providers | Signal/source adapters | Yes |
| Integrations | Tool adapters | Yes |
| Instance store | User markdown/YAML | Yes |

## OSS vs instance

- **OSS** ships protocols, scaffold, reference providers, and docs.
- **Instance** holds the living Knowledge Base (`wiki/`) and personal trees.
- Sync policy: **instance wiki wins**; scaffold only creates missing files.

See [GOVERNANCE.md](GOVERNANCE.md) and [engine/invariants.md](engine/invariants.md).
```

- [ ] **Step 4: Write `ROADMAP.md`**

```markdown
# Roadmap

| Phase | Focus | Status |
|-------|--------|--------|
| 1 | Restructuring — Protocol Kernel identity | In progress |
| 2 | Research engine (ResearchBrief / Synthesis + agent) | Planned |
| 3 | Trend Radar pack stabilization | Planned |
| 4 | Content Intelligence | Planned |
| 5 | Learning Intelligence | Planned |
| 6 | Full Context Engine loop metrics | Planned |

Details: [docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md](docs/superpowers/specs/2026-07-11-context-engine-repositioning-design.md)
```

- [ ] **Step 5: Write `FAQ.md`**

```markdown
# FAQ

## Is this a PKM or wiki product?

No. It is a Context Engine (Protocol Kernel). The wiki is the instance’s long-term memory module, not the product identity.

## Do I need Obsidian, Cursor, or Claude?

No. Those are optional adapters. The kernel is tool-agnostic.

## Where does my knowledge live?

In your **private instance** (typically a private git repo). The public repository does not host your living Knowledge Base.

## What is Leverage Radar?

A reference **signal provider** plus agent pack. It is not the whole product.

## Can I contribute my principles upstream?

Not as personal knowledge. Contribute framework improvements (contracts, agents, providers, docs). Instance KB content stays private unless fully sanitized and intentionally published as an example.
```

- [ ] **Step 6: Write `GLOSSARY.md`**

```markdown
# Glossary

| Term | Meaning |
|------|---------|
| Protocol Kernel | Core contracts + cycle invariants of AI Knowledge OS |
| Instance | A user’s private deployment with living wiki and personal trees |
| Signal | Typed raw event from a provider |
| Insight | Answer to an implicit question plus a suggested action |
| Knowledge Base | Instance `wiki/` — durable memory |
| Provider | Component that emits contract artifacts (often Signals) |
| Agent pack | Portable skill defining a role in the cycle |
| Adapter / Integration | Optional bridge to a specific tool |
| Closed loop | Signals → … → learning/production → KB update |
```

- [ ] **Step 7: Commit**

```bash
git add VISION.md MISSION.md ARCHITECTURE.md ROADMAP.md FAQ.md GLOSSARY.md
git commit -m "$(cat <<'EOF'
docs: add Vision, Mission, Architecture, Roadmap, FAQ, Glossary

EOF
)"
```

---

### Task 3: Contracts + engine protocol files

**Files:**
- Create: `contracts/*.md`, `engine/cycle.md`, `engine/invariants.md`

- [ ] **Step 1: Write contract stubs**

Each contract file must include: purpose, required fields, emitters, consumers, wiki touchpoints.

`contracts/signal.md`:

```markdown
# Contract: Signal

**Purpose:** Typed raw event from the world (market, community, research feed).

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| id | string | Stable unique id |
| provider | string | Provider key |
| url | string | Canonical URL |
| title | string | |
| ts | string | ISO-8601 |

Optional: `author`, `text`, `metrics`, `provenance`.

## JSON schema (reference)

See `providers/signals/schema/signal.schema.json` after relocate.

## Emitters

Signal providers (e.g. Trend Radar sources).

## Consumers

Research Agent, Trend Radar clustering, Knowledge Curator (indirect).
```

Create the same pattern for:

- `contracts/research-brief.md` — focused exploration; fields: `topic`, `questions`, `sources[]`, `notes`, `open_questions`
- `contracts/synthesis.md` — what changed / what matters; fields: `claim`, `evidence[]`, `implications`, `confidence`
- `contracts/knowledge-entry.md` — wiki note metadata; fields: `category`, `slug`, `when_to_use`, `links[]`, `origin`
- `contracts/insight.md` — fields: `question`, `answer`, `action`, `based_on[]`
- `contracts/decision-log.md` — fields: `decision`, `ignored`, `rationale`, `date`
- `contracts/content-brief.md` — fields: `angle`, `audience`, `outline`, `source_insights[]`
- `contracts/learning-update.md` — fields: `learned`, `updates_paths[]`, `next_actions[]`

- [ ] **Step 2: Write `engine/cycle.md` and `engine/invariants.md`**

`engine/cycle.md`:

```markdown
# Cycle

```text
Signals → Research → Synthesis → Knowledge Base → Context → Insights → Content/Projects → Learning → Update
```

Every feature must strengthen this loop. Summaries without decision, learning, or production are incomplete.
```

`engine/invariants.md`:

```markdown
# Invariants

1. Tool-agnostic kernel — no mandatory adapter
2. Instance sovereignty — living memory never uploads without sanitization
3. Cycle over features
4. Substitutable providers/agents/adapters
5. Docs as product
6. Instance wiki wins on sync — never overwrite living KB with empty scaffold
```

- [ ] **Step 3: Commit**

```bash
git add contracts engine
git commit -m "$(cat <<'EOF'
docs: add cycle contracts and engine invariants

EOF
)"
```

---

### Task 4: Rewrite README, GOVERNANCE, CONTRIBUTING, AGENTS

**Files:**
- Modify: `README.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `AGENTS.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Replace `README.md` constitution**

```markdown
# AI Knowledge OS

**Context Engine** (Protocol Kernel) for technology professionals — not a PKM app, not a news aggregator, not a prompt pack.

It helps you turn dispersed signals into actionable context and close the loop through learning and production. The public repo is the **framework**. Your knowledge lives in your **private instance**.

## Constitution

| This project **is** | This project **is not** |
|---------------------|-------------------------|
| A Protocol Kernel for personal/professional context | A personal Obsidian vault |
| Contracts + cycle + agent/provider packs | A dump of one person’s notes |
| A system you instantiate privately | A requirement that your knowledge live upstream |
| Tool-agnostic by design | Locked to Cursor, Claude, Obsidian, or one LLM |

## Start

1. Read [VISION.md](VISION.md) and [MISSION.md](MISSION.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. Follow [docs/getting-started.md](docs/getting-started.md)
4. Copy [templates/instance/](templates/instance/) into a **private** repo for your living Knowledge Base

## Layout (public)

| Path | Role |
|------|------|
| `contracts/` | Artifact schemas |
| `engine/` | Cycle protocol |
| `wiki/` | Knowledge Base **scaffold** only |
| `agents/` | Skill packs |
| `providers/` | Reference providers |
| `docs/` | Institutional + feature docs |

Full governance: [GOVERNANCE.md](GOVERNANCE.md)
```

- [ ] **Step 2: Rewrite `GOVERNANCE.md` dual-identity sections**

Keep the private SoT + public contribution fork model (A1-equivalent). Update:

- Upstream role = Protocol Kernel framework (not principles library)
- Forbidden personal paths at OSS root remain
- **Exception:** `research/` allowed only as scaffold (`README.md`, `.gitkeep`)
- **Wiki merge policy:** instance wiki wins
- Promotion = framework PRs only by default (contracts, agents, providers, docs, scaffold)

Include explicit subsection:

```markdown
## Instance wiki preservation

The instance `wiki/` is the canonical long-term Knowledge Base.
Upstream sync must never replace living instance notes with empty scaffold files.
Use `templates/instance/scripts/sync-from-upstream.sh`.
```

- [ ] **Step 3: Rewrite `CONTRIBUTING.md` and `AGENTS.md`**

`AGENTS.md` must include Always/Never from the spec, especially:

- Always preserve instance wiki
- Never promote instance principles/journals to OSS
- Never bind product to a specific tool
- Doubt ⇒ private

Update forbidden paths note: `research/` at root is allowed **only** as scaffold.

- [ ] **Step 4: Update PR template**

Change summary prompt to framework contributions; allow paths: `contracts/`, `engine/`, `agents/`, `providers/`, `wiki/` (scaffold only), `docs/`, top-level institutional docs. Keep sanitization checklist.

- [ ] **Step 5: Commit**

```bash
git add README.md GOVERNANCE.md CONTRIBUTING.md AGENTS.md .github/PULL_REQUEST_TEMPLATE.md
git commit -m "$(cat <<'EOF'
docs: reposition README and governance for Context Engine

EOF
)"
```

---

### Task 5: Public wiki → scaffold only (WORKTREE ONLY)

**Files:**
- Delete (public worktree only): all content under `wiki/principles/*.md` except structure, `wiki/MOC/*` content notes, filled case-study bodies if any on upstream
- Create: scaffold categories + new `wiki/index.md`, `wiki/_meta/governance.md`, expanded `wiki/_meta/templates.md`

- [ ] **Step 1: Safety check**

```bash
pwd   # must be .worktrees/context-engine-phase1
test -f ../../LAB.md && echo "WARNING: unexpected" || echo "OK"
```

- [ ] **Step 2: Remove upstream principle/MOC content; keep scaffold**

```bash
# Remove living knowledge from PUBLIC tree only
git rm -r wiki/principles/*.md 2>/dev/null || true
git rm -r wiki/MOC 2>/dev/null || true
git rm -f wiki/_meta/coverage-matrix.md wiki/_meta/extraction-ledger.md 2>/dev/null || true
# Keep case-studies hub if only README; remove any filled case studies on upstream
mkdir -p wiki/principles wiki/architecture wiki/rfcs wiki/adrs wiki/playbooks \
  wiki/research wiki/learning-paths wiki/trend-analysis wiki/content-ideas wiki/decision-logs
touch wiki/principles/.gitkeep wiki/architecture/.gitkeep wiki/rfcs/.gitkeep \
  wiki/adrs/.gitkeep wiki/playbooks/.gitkeep wiki/research/.gitkeep \
  wiki/learning-paths/.gitkeep wiki/trend-analysis/.gitkeep \
  wiki/content-ideas/.gitkeep wiki/decision-logs/.gitkeep
```

Write `wiki/index.md`:

```markdown
# Knowledge Base (scaffold)

This tree is an empty **schema** for an instance Knowledge Base.

Copy categories into your private instance and write living notes there.
Upstream does not store personal principles or case studies.

## Categories

| Category | Role |
|----------|------|
| principles | Stable judgment |
| case-studies | Evidence |
| architecture | System shape |
| rfcs / adrs | Proposals and decisions |
| playbooks | Procedures |
| research | Durable research memory |
| learning-paths | Study trajectories |
| trend-analysis | Market/tech memory |
| content-ideas | Insight → production |
| decision-logs | Prioritize / ignore |

Templates: [[_meta/templates]] · Governance: [[_meta/governance]]
```

Write `wiki/_meta/governance.md` with create/update/archive/review rules from the design.

Expand `wiki/_meta/templates.md` with stubs for each new category (minimum: title, when_to_use, body, related, origin).

Write `wiki/case-studies/README.md` as empty hub (no Tangram).

- [ ] **Step 3: Commit**

```bash
git add wiki
git commit -m "$(cat <<'EOF'
refactor(wiki): replace public corpus with Knowledge Base scaffold

Living principles and case studies belong in private instances only.
EOF
)"
```

- [ ] **Step 4: Verify private lab wiki still intact**

```bash
ls /Users/matheusborges/github/AI-Knowledge-OS/wiki/principles | wc -l
# expect: still dozens of files — unchanged
```

---

### Task 6: Docs index, getting-started, cycle, maintenance

**Files:**
- Create: `docs/index.md`, `docs/getting-started.md`, `docs/cycle.md`, `docs/maintenance.md`
- Modify: `docs/radar/*.md` — add one-line banner: “Reference provider docs (not product identity)”

- [ ] **Step 1: Write the four institutional docs**

`docs/getting-started.md` must cover:

1. Clone/fork public framework  
2. Create private instance from `templates/instance/`  
3. Sync policy (wiki wins)  
4. Optional: enable Trend Radar provider  
5. Run first loop: one signal → one insight note in instance wiki  

`docs/cycle.md` — full flow + wiki participation table from the spec.

`docs/maintenance.md` — drift checks, contract versioning, Documentation Maintainer role.

`docs/index.md` — links to all institutional docs.

- [ ] **Step 2: Banner on radar docs**

Prepend to each file in `docs/radar/`:

```markdown
> **Note:** Leverage Radar is a **reference signal provider** for AI Knowledge OS, not the product identity. See [ARCHITECTURE.md](../../ARCHITECTURE.md).
```

- [ ] **Step 3: Commit**

```bash
git add docs/index.md docs/getting-started.md docs/cycle.md docs/maintenance.md docs/radar
git commit -m "$(cat <<'EOF'
docs: add documentation index, getting started, cycle, maintenance

EOF
)"
```

---

### Task 7: Rename `templates/personal-lab` → `templates/instance`

**Files:**
- Rename: `templates/personal-lab/` → `templates/instance/`
- Modify: READMEs inside template; references in GOVERNANCE/README/docs

- [ ] **Step 1: Rename and update copy**

```bash
git mv templates/personal-lab templates/instance
```

Update `templates/instance/README.md` to say **Instance template** (Context Engine), not merely “personal lab”. Point to sync script (added in Task 9).

Replace remaining references:

```bash
rg -n "personal-lab" -g '!docs/superpowers/**' -g '!docs/plans/**' -g '!docs/specs/**'
```

Update hits in active docs (`GOVERNANCE.md`, `README.md`, `AGENTS.md`, CI messages). Leave historical specs untouched or add a one-line “superseded name” note only if needed.

- [ ] **Step 2: Commit**

```bash
git add templates GOVERNANCE.md README.md AGENTS.md .github
git commit -m "$(cat <<'EOF'
refactor: rename personal-lab template to instance

EOF
)"
```

---

### Task 8: Relocate `radar/` → `providers/signals/`

**Files:**
- Move: `radar/**` → `providers/signals/**`
- Rename: `providers/signals/providers/` → `providers/signals/sources/`
- Move: `tests/radar/` → `tests/providers/signals/`
- Update imports across Python, skills, docs/radar, templates/radar

- [ ] **Step 1: Move tree**

```bash
mkdir -p providers
git mv radar providers/signals
git mv providers/signals/providers providers/signals/sources
git mv tests/radar tests/providers/signals
```

Add `providers/__init__.py` and ensure `providers/signals/__init__.py` exists (empty ok).

- [ ] **Step 2: Rewrite imports**

In all files under `providers/signals/` and `tests/providers/signals/`:

- `from radar.lib` → `from providers.signals.lib`
- `import radar.lib` → `import providers.signals.lib`
- `from radar.providers` → `from providers.signals.sources`
- `radar.providers` → `providers.signals.sources`

Update `providers/signals/fetch_enabled.py` accordingly.

Update tests’ `ROOT = Path(__file__).resolve().parents[N]` — after move, parents depth becomes `parents[3]` if path is `tests/providers/signals/test_*.py` (repo root). Verify:

```python
ROOT = Path(__file__).resolve().parents[3]  # tests/providers/signals -> repo root
sys.path.insert(0, str(ROOT))
```

- [ ] **Step 3: Run tests**

```bash
cd .worktrees/context-engine-phase1
pytest tests/providers/signals -v
```

Expected: PASS (all former radar tests).

If FAIL, fix imports until PASS before committing.

- [ ] **Step 4: Write `providers/signals/README.md`**

```markdown
# Signals provider (reference) — Leverage Radar

Reference implementation that fetches multi-source signals for the Trend Radar agent pack.

This is **not** the product identity of AI Knowledge OS. See root [README.md](../../README.md).
```

- [ ] **Step 5: Commit**

```bash
git add providers tests docs templates
git commit -m "$(cat <<'EOF'
refactor: move radar package to providers/signals

EOF
)"
```

---

### Task 9: Agent packs — Trend Radar move + role stubs

**Files:**
- Create: `agents/trend-radar/SKILL.md`, `agents/trend-radar/README.md`, stubs for other agents
- Modify: `.cursor/skills/`, `.claude/skills/`
- Replace: `skills/leverage-radar/` with redirect README

- [ ] **Step 1: Move skill and update paths**

```bash
mkdir -p agents/trend-radar
git mv skills/leverage-radar/SKILL.md agents/trend-radar/SKILL.md
```

Edit `agents/trend-radar/SKILL.md`:

- Frontmatter `name: trend-radar` (keep description mentioning leverage radar triggers)
- Replace `python radar/providers/fetch_enabled.py` with:

```bash
python providers/signals/fetch_enabled.py \
  --config journals/radar/config.yaml \
  --out journals/radar/_raw/YYYY-MM-DD.jsonl
```

- Replace `radar.lib.topics_io` with `providers.signals.lib.topics_io`

Write `agents/trend-radar/README.md` explaining sync:

```bash
cp agents/trend-radar/SKILL.md .cursor/skills/trend-radar/SKILL.md
cp agents/trend-radar/SKILL.md .claude/skills/trend-radar/SKILL.md
```

- [ ] **Step 2: Install adapter copies**

```bash
mkdir -p .cursor/skills/trend-radar .claude/skills/trend-radar
cp agents/trend-radar/SKILL.md .cursor/skills/trend-radar/SKILL.md
cp agents/trend-radar/SKILL.md .claude/skills/trend-radar/SKILL.md
# remove old leverage-radar skill paths if present
git rm -rf .cursor/skills/leverage-radar .claude/skills/leverage-radar skills/leverage-radar 2>/dev/null || true
```

Write `skills/README.md`:

```markdown
# Skills

Canonical agent packs live under [`agents/`](../agents/). This directory remains as a pointer for older links.
```

- [ ] **Step 3: Stub other agent READMEs**

For each of `research`, `knowledge-curator`, `learning-coach`, `content-strategist`, `engineering-analyst`, `documentation-maintainer`, create `agents/<name>/README.md` with: responsibility, emits, never-does (from the design table). No full SKILL.md yet (Phase 2+).

- [ ] **Step 4: Commit**

```bash
git add agents skills .cursor/skills .claude/skills
git commit -m "$(cat <<'EOF'
feat(agents): add Trend Radar pack and role stubs

EOF
)"
```

---

### Task 10: Instance sync script (wiki wins) + test

**Files:**
- Create: `templates/instance/scripts/sync-from-upstream.sh`
- Create: `tests/test_sync_from_upstream.sh`

- [ ] **Step 1: Write failing test script**

`tests/test_sync_from_upstream.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Fake upstream framework tree
mkdir -p "$TMP/upstream/wiki/principles" "$TMP/upstream/contracts"
echo "SCAFFOLD" > "$TMP/upstream/wiki/principles/.gitkeep"
echo "# contract" > "$TMP/upstream/contracts/signal.md"
echo "UPSTREAM_INDEX" > "$TMP/upstream/wiki/index.md"

# Fake instance with living wiki
mkdir -p "$TMP/instance/wiki/principles" "$TMP/instance/contracts"
echo "LIVING_PRINCIPLE" > "$TMP/instance/wiki/principles/my-principle.md"
echo "INSTANCE_INDEX" > "$TMP/instance/wiki/index.md"

"$ROOT/templates/instance/scripts/sync-from-upstream.sh" \
  --upstream "$TMP/upstream" \
  --instance "$TMP/instance"

# Living files must remain
grep -q LIVING_PRINCIPLE "$TMP/instance/wiki/principles/my-principle.md"
grep -q INSTANCE_INDEX "$TMP/instance/wiki/index.md"
# Framework file should arrive
test -f "$TMP/instance/contracts/signal.md"
# Scaffold .gitkeep may be created if missing, but must not delete living principle
test -f "$TMP/instance/wiki/principles/my-principle.md"
echo "PASS"
```

- [ ] **Step 2: Run test — expect FAIL (script missing)**

```bash
chmod +x tests/test_sync_from_upstream.sh
bash tests/test_sync_from_upstream.sh
```

Expected: FAIL (`No such file or directory` for sync script).

- [ ] **Step 3: Implement `templates/instance/scripts/sync-from-upstream.sh`**

```bash
#!/usr/bin/env bash
# Sync Protocol Kernel framework into an instance without overwriting living wiki files.
set -euo pipefail

UPSTREAM=""
INSTANCE=""
FRAMEWORK_DIRS=(contracts engine agents providers integrations prompts docs examples assets templates)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --upstream) UPSTREAM="$2"; shift 2 ;;
    --instance) INSTANCE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$UPSTREAM" && -n "$INSTANCE" ]] || { echo "Usage: $0 --upstream DIR --instance DIR" >&2; exit 2; }
[[ -d "$UPSTREAM" && -d "$INSTANCE" ]] || { echo "Dirs must exist" >&2; exit 2; }

# Copy framework dirs (overwrite framework files OK)
for d in "${FRAMEWORK_DIRS[@]}"; do
  if [[ -d "$UPSTREAM/$d" ]]; then
    mkdir -p "$INSTANCE/$d"
    rsync -a --delete "$UPSTREAM/$d/" "$INSTANCE/$d/"
  fi
done

# Institutional root docs (overwrite OK)
for f in README.md VISION.md MISSION.md ARCHITECTURE.md GOVERNANCE.md CONTRIBUTING.md \
         AGENTS.md ROADMAP.md FAQ.md GLOSSARY.md LICENSE; do
  if [[ -f "$UPSTREAM/$f" ]]; then
    cp "$UPSTREAM/$f" "$INSTANCE/$f"
  fi
done

# Wiki: never delete instance files; only copy missing paths (scaffold fill-in)
if [[ -d "$UPSTREAM/wiki" ]]; then
  mkdir -p "$INSTANCE/wiki"
  # copy files that do not exist in instance; do not overwrite
  rsync -a --ignore-existing "$UPSTREAM/wiki/" "$INSTANCE/wiki/"
fi

# research scaffold at root: ignore-existing only
if [[ -d "$UPSTREAM/research" ]]; then
  mkdir -p "$INSTANCE/research"
  rsync -a --ignore-existing "$UPSTREAM/research/" "$INSTANCE/research/"
fi

echo "Sync complete. Instance wiki preserved (ignore-existing)."
```

```bash
chmod +x templates/instance/scripts/sync-from-upstream.sh
```

Note: if `rsync` is unavailable in CI, implement with `find`+`cp` equivalent. Prefer documenting `rsync` requirement in template README; for macOS/Linux agents `rsync` is standard.

- [ ] **Step 4: Run test — expect PASS**

```bash
bash tests/test_sync_from_upstream.sh
```

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add templates/instance/scripts/sync-from-upstream.sh tests/test_sync_from_upstream.sh
git commit -m "$(cat <<'EOF'
feat(instance): add upstream sync script that preserves living wiki

EOF
)"
```

---

### Task 11: CI boundary-check — scaffold-aware `research/` + wiki heuristic

**Files:**
- Modify: `.github/workflows/boundary-check.yml`
- Create: `tests/test_boundary_scaffold.py`

- [ ] **Step 1: Write failing pytest for local boundary rules**

`tests/test_boundary_scaffold.py`:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ROOT = {"knowledge", "notes", "journals", "experiments", "obsidian", "vault"}
RESEARCH_ALLOWED = {".gitkeep", "README.md"}


def test_forbidden_personal_paths_absent():
    for name in FORBIDDEN_ROOT:
        assert not (ROOT / name).exists(), f"forbidden path present: {name}"


def test_research_is_scaffold_only_if_present():
    research = ROOT / "research"
    if not research.exists():
        return
    names = {p.name for p in research.iterdir() if p.name != ".DS_Store"}
    assert names <= RESEARCH_ALLOWED, f"research/ not scaffold-only: {names}"


def test_wiki_principles_has_no_markdown_corpus():
    principles = ROOT / "wiki" / "principles"
    if not principles.exists():
        return
    md = list(principles.glob("*.md"))
    assert md == [], f"public wiki/principles must be empty scaffold, found {md}"
```

- [ ] **Step 2: Run pytest**

```bash
pytest tests/test_boundary_scaffold.py -v
```

Expected: PASS on the public worktree after Task 5; FAIL if principles `.md` still present.

- [ ] **Step 3: Update `.github/workflows/boundary-check.yml`**

```yaml
name: Boundary check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  forbidden-paths:
    name: Reject private lab paths
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fail if forbidden paths exist at repo root
        run: |
          set -euo pipefail
          forbidden=(knowledge notes journals experiments obsidian vault)
          found=0
          for name in "${forbidden[@]}"; do
            if [ -e "$name" ]; then
              echo "::error::Forbidden path at repository root: $name/"
              found=1
            fi
          done
          # research/ allowed only as scaffold
          if [ -d research ]; then
            while IFS= read -r -d '' f; do
              base=$(basename "$f")
              case "$base" in
                README.md|.gitkeep) ;;
                *)
                  echo "::error::research/ must be scaffold-only; found: $f"
                  found=1
                  ;;
              esac
            done < <(find research -mindepth 1 -maxdepth 1 -print0)
          fi
          # public wiki/principles must not contain markdown corpus
          if ls wiki/principles/*.md >/dev/null 2>&1; then
            echo "::error::wiki/principles must be scaffold-only on upstream (no .md corpus)"
            found=1
          fi
          if [ "$found" -ne 0 ]; then
            echo "See GOVERNANCE.md"
            exit 1
          fi
          echo "Boundary check passed."
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/boundary-check.yml tests/test_boundary_scaffold.py
git commit -m "$(cat <<'EOF'
ci: allow research scaffold; reject public wiki corpus

EOF
)"
```

---

### Task 12: Final verification + PR prep

**Files:** none new

- [ ] **Step 1: Run full verification in worktree**

```bash
cd .worktrees/context-engine-phase1
pytest tests/providers/signals tests/test_boundary_scaffold.py -v
bash tests/test_sync_from_upstream.sh
rg -n "personal-lab|engineering wiki|Library of engineering" README.md GOVERNANCE.md CONTRIBUTING.md AGENTS.md || true
test ! -f wiki/principles/*.md 2>/dev/null || ls wiki/principles/*.md
# private lab still has principles:
test -n "$(ls /Users/matheusborges/github/AI-Knowledge-OS/wiki/principles/*.md | head -1)"
echo "Private wiki intact + public scaffold OK"
```

Expected: tests PASS; README no longer sells “engineering wiki” as identity; private principles still present.

- [ ] **Step 2: Sanitization gate (answer in PR body)**

1. Depends on private document? **No**  
2. Inspired by personal notes content? **No** (strategy only)  
3. Personal/employer examples? **No**  
4. Private file used as reference for wiki corpus? **No**  
5. Claims only author knows? **No**

- [ ] **Step 3: Push and open PR (when user requests)**

```bash
git push -u fork HEAD
gh pr create --repo rapidinha/AI-Knowledge-OS --title "feat: Context Engine Phase 1 — Protocol Kernel restructure" --body "$(cat <<'EOF'
## Summary
- Reposition public repo as Context Engine Protocol Kernel
- Institutional docs (Vision, Mission, Architecture, …)
- Public wiki → scaffold only; instance wiki preserved via sync script
- Relocate radar → providers/signals; skill → agents/trend-radar
- CI scaffold rules for research/ and wiki/principles

## Test plan
- [ ] `pytest tests/providers/signals tests/test_boundary_scaffold.py -v`
- [ ] `bash tests/test_sync_from_upstream.sh`
- [ ] Confirm private lab `wiki/principles` unchanged
- [ ] README identity reads as Context Engine, not PKM/wiki product

## Sanitization
All answers No (framework-only change).

EOF
)"
```

Do **not** push/create PR unless the user explicitly asks.

---

## Self-review (plan vs spec)

| Spec section | Task coverage |
|--------------|---------------|
| Vision/positioning | Task 2, 4 |
| Architecture Protocol Kernel | Task 2–3 |
| Repo layout | Task 1, 7–9 |
| Wiki scaffold + private preserve | Task 5, 10, 12 |
| Documentation strategy | Task 2, 4, 6 |
| Knowledge flow docs | Task 3, 6 |
| Agents | Task 9 (stubs + Trend Radar) |
| Maintenance/CI | Task 11, 6 |
| AI rules | Task 4 (`AGENTS.md`) |
| Roadmap | Task 2 |
| Philosophy | embedded in VISION/MISSION/ARCHITECTURE |
| Radar relocate | Task 8–9 |
| Phases 2–6 | Explicitly out of scope |

**Placeholder scan:** none intentional — contract field lists and doc bodies are specified.

**Type/import consistency:** `providers.signals.lib` / `providers.signals.sources` used uniformly in Tasks 8–9.

---

## Deferred to later plans

- Full Research / Learning / Content agent SKILL.md bodies (Phases 2, 4, 5)
- Loop metrics instrumentation (Phase 6)
- Expanding contracts beyond stubs into JSON Schema suite
- Historical `docs/plans` / `docs/specs` radar docs rewrite (banner only in Phase 1)
