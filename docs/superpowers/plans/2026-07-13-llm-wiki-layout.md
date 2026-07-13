# LLM Wiki Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the private lab into Karpathy-style `raw/` + `wiki/`, migrate existing personal trees, update schema/radar paths, and consolidate the `ai-advantage-expired` pilot into wiki concepts + one sanitized principle.

**Architecture:** Immutable sources and secondary research live under `raw/{sources,research}`; operational artifacts under `raw/ops/{daily,posts,radar,experiments}`; the LLM-maintained compile layer stays in `wiki/` (`concepts/`, `entities/`, `principles/`, `index.md`, `log.md`). Old roots become migration stubs. No upstream PR in this plan.

**Tech Stack:** Markdown + YAML (Obsidian vault); Git mv for history-friendly moves; existing Leverage Radar Python package under `radar/` (path strings only); GitHub Actions boundary-check; pytest only if radar path defaults break (they should not).

**Upstream note (Context Engine):** public `wiki/principles/` remains scaffold-only (CI). Living principles/concepts from the pilot stay in the private instance; this OSS change ships schema, instance `raw/` template, radar path convention, and docs.

**Spec:** [`docs/superpowers/specs/2026-07-13-llm-wiki-layout-design.md`](../specs/2026-07-13-llm-wiki-layout-design.md)

---

## File structure (lock this first)

```text
raw/
  README.md
  sources/
    README.md
    ai-advantage-expired/          # from research/radar/.../ingest
    career-beginning-tech/         # from knowledge/private/.../ingest
    _archives/                     # from knowledge/private/sources
    shared/                        # from knowledge/shared
    imported/                      # from knowledge/imported
    notes/                         # from notes/ if kept
  research/
    README.md
    ai-advantage-expired/          # README + guides (no ingest/)
    career-beginning-tech/         # profiles + patterns + _archive/consolidate
  ops/
    README.md
    daily/                         # journals/daily + week notes
    posts/                         # journals/post-ideas
    radar/                         # journals/radar (full tree)
    experiments/                   # experiments/

wiki/
  index.md                         # enrich into LLM catalog
  log.md                           # NEW append-only op log
  concepts/                        # NEW
  entities/                        # NEW (+ .gitkeep)
  _meta/
    templates.md                   # + concept/entity templates
    llm-wiki-schema.md             # NEW ops contract
  principles/judgment-over-generation.md   # NEW (pilot)
  MOC/engineering-practice.md      # + link to new principle/concepts

# Deprecated stubs (README only until links clean)
knowledge/README.md
research/README.md
journals/README.md
notes/README.md
experiments/README.md

# Schema / CI / radar docs (path string updates)
LAB.md
AGENTS.md
AGENTS.private.md
.gitignore
.github/workflows/boundary-check.yml
docs/radar/*.md
skills/leverage-radar/SKILL.md
.cursor/skills/leverage-radar/SKILL.md
.claude/skills/leverage-radar/SKILL.md
templates/radar/*.md
templates/personal-lab/**          # restructure scaffold to raw/
```

**Hard rules for implementers:**

1. Prefer `git mv` over copy+delete so history survives.
2. Do **not** rewrite named case studies.
3. Do **not** open an upstream public PR in this plan.
4. Do **not** put nominal X author tables into `wiki/principles/`.
5. `radar/` Python package stays at repo root; only markdown/config *paths* change to `raw/ops/radar/`.
6. On the private lab, `raw/` is allowed. CI deny-list must forbid `raw/` on **public** contribution trees (same as today’s `journals/`).

---

### Task 1: Scaffold `raw/` and wiki compile dirs

**Files:**
- Create: `raw/README.md`
- Create: `raw/sources/README.md`
- Create: `raw/research/README.md`
- Create: `raw/ops/README.md`
- Create: `wiki/concepts/.gitkeep`
- Create: `wiki/entities/.gitkeep`
- Create: `wiki/log.md`

- [ ] **Step 1: Create directories**

```bash
mkdir -p raw/sources raw/research raw/ops/daily raw/ops/posts raw/ops/radar raw/ops/experiments \
  wiki/concepts wiki/entities
```

- [ ] **Step 2: Write `raw/README.md`**

```markdown
# Raw layer (immutable inputs + ops)

Human-curated sources and operational artifacts. The LLM **reads** this layer; it does not rewrite history in place.

| Path | Role |
|------|------|
| `sources/<slug>/` | Ingest — primary sources |
| `research/<slug>/` | Secondary research (not wiki truth yet) |
| `ops/` | Daily notes, posts, Leverage Radar, experiments |

Compiled knowledge lives in [`wiki/`](../wiki/index.md). Schema: [`wiki/_meta/llm-wiki-schema.md`](../wiki/_meta/llm-wiki-schema.md).
```

- [ ] **Step 3: Write the three sub-READMEs**

`raw/sources/README.md`:

```markdown
# Sources (ingest)

Drop immutable primary sources here as `sources/<slug>/...`.
Run **Ingest** per `wiki/_meta/llm-wiki-schema.md`.
```

`raw/research/README.md`:

```markdown
# Research

Secondary surveys and drafts for `<slug>`. Promote to `wiki/` only via **Consolidate**.
```

`raw/ops/README.md`:

```markdown
# Ops

| Path | Was |
|------|-----|
| `daily/` | `journals/daily/` |
| `posts/` | `journals/post-ideas/` |
| `radar/` | `journals/radar/` |
| `experiments/` | `experiments/` |
```

- [ ] **Step 4: Write starter `wiki/log.md`**

```markdown
# Wiki log

Append-only timeline of ingest / research / consolidate / query / lint operations.

| Date | Op | Slug | Pages touched | Note |
|------|----|------|---------------|------|
| 2026-07-13 | scaffold | — | `wiki/log.md`, `wiki/concepts/`, `wiki/entities/` | LLM wiki layout bootstrap |
```

- [ ] **Step 5: Touch gitkeeps**

```bash
touch wiki/concepts/.gitkeep wiki/entities/.gitkeep
```

- [ ] **Step 6: Verify scaffold**

```bash
test -f raw/README.md && test -f wiki/log.md && test -d wiki/concepts && ls raw
```

Expected: `ops  README.md  research  sources`

- [ ] **Step 7: Commit**

```bash
git add raw wiki/log.md wiki/concepts wiki/entities
git commit -m "$(cat <<'EOF'
chore: scaffold raw/ + wiki concepts/entities/log

Bootstrap Karpathy-style lab layers before migrating personal trees.
EOF
)"
```

---

### Task 2: Migrate ops (`journals/` → `raw/ops/`, `experiments/` → `raw/ops/experiments/`)

**Files:**
- Move: `journals/daily/` → `raw/ops/daily/`
- Move: `journals/post-ideas/` → `raw/ops/posts/`
- Move: `journals/radar/` → `raw/ops/radar/`
- Move: `journals/2026-07-W3.md` → `raw/ops/daily/2026-07-W3.md` (if present)
- Move: `experiments/` contents → `raw/ops/experiments/`
- Modify: `.gitignore`

- [ ] **Step 1: Move trees with git mv**

```bash
# Ensure targets empty of real content (only scaffold dirs from Task 1)
git mv journals/daily raw/ops/daily 2>/dev/null || mv journals/daily/* raw/ops/daily/ && rmdir journals/daily
git mv journals/post-ideas raw/ops/posts 2>/dev/null || { mkdir -p raw/ops/posts && mv journals/post-ideas/* raw/ops/posts/ && rmdir journals/post-ideas; }

# Radar: move whole directory over scaffold
rmdir raw/ops/radar 2>/dev/null || true
git mv journals/radar raw/ops/radar

# Week note if present at journals root
if [ -f journals/2026-07-W3.md ]; then git mv journals/2026-07-W3.md raw/ops/daily/2026-07-W3.md; fi

# Experiments
if [ -f experiments/README.md ]; then git mv experiments/README.md raw/ops/experiments/README.md; fi
```

If `git mv` fails on untracked files, use plain `mv` then `git add`.

- [ ] **Step 2: Update `.gitignore`**

Replace radar ignore block with:

```gitignore
# Leverage Radar (personal lab — never commit raw/config)
raw/ops/radar/_raw/
raw/ops/radar/config.yaml
raw/ops/radar/topics.yaml
__pycache__/
*.py[cod]
```

Remove duplicate `journals/radar/...` lines.

- [ ] **Step 3: Verify radar config path**

```bash
test -f raw/ops/radar/topics/_index.md
ls raw/ops/radar/
# config.yaml may be gitignored — check filesystem:
test -f raw/ops/radar/config.yaml && echo "config ok" || echo "config missing — copy from templates/radar/config.example.yaml"
```

- [ ] **Step 4: Commit**

```bash
git add -A raw/ops .gitignore journals experiments
git commit -m "$(cat <<'EOF'
refactor: move journals and experiments under raw/ops

Daily, posts, radar, and experiments now live in the ops layer.
EOF
)"
```

---

### Task 3: Update Leverage Radar path strings

**Files:**
- Modify: `skills/leverage-radar/SKILL.md`
- Modify: `.cursor/skills/leverage-radar/SKILL.md`
- Modify: `.claude/skills/leverage-radar/SKILL.md`
- Modify: `docs/radar/protocol.md`
- Modify: `docs/radar/using-agents.md`
- Modify: `docs/radar/obsidian.md`
- Modify: `docs/radar/providers.md`
- Modify: `docs/radar/scoring.md`
- Modify: `docs/radar/e2e-checklist.md`
- Modify: `templates/radar/daily.md`
- Modify: `templates/radar/research-stub.md`
- Modify: `templates/radar/topic.md`
- Modify: `templates/radar/topics-index.md`
- Modify: `templates/radar/config.example.yaml` (comments only if any)
- Modify: `LAB.md` (radar section path — full LAB rewrite in Task 6; here only radar one-liner if needed)

- [ ] **Step 1: Bulk replace in radar docs/skills/templates**

```bash
for f in \
  skills/leverage-radar/SKILL.md \
  .cursor/skills/leverage-radar/SKILL.md \
  .claude/skills/leverage-radar/SKILL.md \
  docs/radar/protocol.md \
  docs/radar/using-agents.md \
  docs/radar/obsidian.md \
  docs/radar/providers.md \
  docs/radar/scoring.md \
  docs/radar/e2e-checklist.md \
  templates/radar/daily.md \
  templates/radar/research-stub.md \
  templates/radar/topic.md \
  templates/radar/topics-index.md \
  templates/radar/config.example.yaml \
  templates/radar/decisions.example.yaml \
  templates/radar/topics.example.yaml
do
  [ -f "$f" ] || continue
  sed -i '' 's|journals/radar|raw/ops/radar|g' "$f"
done
```

On Linux use `sed -i` without `''`.

- [ ] **Step 2: Fix research stub path in skill if it still says `research/radar/`**

In all three SKILL.md copies, ensure Decide=research creates stubs under:

`raw/research/<slug>/README.md`

Replace any `research/radar/<slug>/` with `raw/research/<slug>/`.

```bash
for f in skills/leverage-radar/SKILL.md .cursor/skills/leverage-radar/SKILL.md .claude/skills/leverage-radar/SKILL.md templates/radar/research-stub.md; do
  sed -i '' 's|research/radar/|raw/research/|g' "$f"
done
```

- [ ] **Step 3: Verify no stale journals/radar in active radar docs**

```bash
rg -n 'journals/radar' skills/leverage-radar .cursor/skills/leverage-radar .claude/skills/leverage-radar docs/radar templates/radar || true
```

Expected: no matches (or only historical notes in unrelated old plans — do not rewrite old plans unless they are operational).

- [ ] **Step 4: Commit**

```bash
git add skills/leverage-radar .cursor/skills/leverage-radar .claude/skills/leverage-radar docs/radar templates/radar
git commit -m "$(cat <<'EOF'
docs: point Leverage Radar paths at raw/ops/radar

Keep the Python package at radar/; only vault paths move.
EOF
)"
```

---

### Task 4: Migrate knowledge + research into `raw/sources` and `raw/research`

**Files:**
- Move: `knowledge/private/career-beginning-tech/ingest/` → `raw/sources/career-beginning-tech/`
- Move: `knowledge/private/career-beginning-tech/patterns/` → `raw/research/career-beginning-tech/patterns/`
- Move: `knowledge/private/career-beginning-tech/consolidate/` → `raw/research/career-beginning-tech/_archive/consolidate/`
- Move: `knowledge/private/career-beginning-tech/README.md` → `raw/research/career-beginning-tech/README.md` (then edit paths)
- Move: `knowledge/private/sources/` → `raw/sources/_archives/`
- Move: `knowledge/shared/` → `raw/sources/shared/`
- Move: `knowledge/imported/` → `raw/sources/imported/`
- Move: `research/career-beginning-tech/` → merge into `raw/research/career-beginning-tech/`
- Move: `research/radar/ai-advantage-expired/ingest/` → `raw/sources/ai-advantage-expired/`
- Move: remainder of `research/radar/ai-advantage-expired/` → `raw/research/ai-advantage-expired/`
- Move: `notes/README.md` → `raw/sources/notes/README.md` (optional keep)

- [ ] **Step 1: Career-beginning-tech sources + research**

```bash
mkdir -p raw/sources/career-beginning-tech \
  raw/research/career-beginning-tech/_archive \
  raw/sources/_archives raw/sources/shared raw/sources/imported

git mv knowledge/private/career-beginning-tech/ingest/* raw/sources/career-beginning-tech/
git mv knowledge/private/career-beginning-tech/patterns raw/research/career-beginning-tech/patterns
git mv knowledge/private/career-beginning-tech/consolidate raw/research/career-beginning-tech/_archive/consolidate
git mv knowledge/private/career-beginning-tech/README.md raw/research/career-beginning-tech/README.md

# private sources archives
git mv knowledge/private/sources/* raw/sources/_archives/ 2>/dev/null || mv knowledge/private/sources/* raw/sources/_archives/

# shared / imported
git mv knowledge/shared/README.md raw/sources/shared/README.md
git mv knowledge/imported/README.md raw/sources/imported/README.md

# existing research corpus
mkdir -p raw/research/career-beginning-tech
# If research/career-beginning-tech already has profiles/, move into place:
git mv research/career-beginning-tech/profiles raw/research/career-beginning-tech/profiles
git mv research/career-beginning-tech/community-emotional-themes.md raw/research/career-beginning-tech/community-emotional-themes.md
# If research/career-beginning-tech/README.md exists, merge manually into raw/research/career-beginning-tech/README.md (keep both sections)
```

- [ ] **Step 2: ai-advantage-expired split**

```bash
mkdir -p raw/sources/ai-advantage-expired raw/research/ai-advantage-expired
git mv research/radar/ai-advantage-expired/ingest/* raw/sources/ai-advantage-expired/
# Move research hub + guides (not ingest)
git mv research/radar/ai-advantage-expired/README.md raw/research/ai-advantage-expired/README.md
git mv research/radar/ai-advantage-expired/guides raw/research/ai-advantage-expired/guides
rmdir research/radar/ai-advantage-expired/ingest 2>/dev/null || true
rmdir research/radar/ai-advantage-expired 2>/dev/null || true
rmdir research/radar 2>/dev/null || true
```

- [ ] **Step 3: Notes**

```bash
mkdir -p raw/sources/notes
git mv notes/README.md raw/sources/notes/README.md
```

- [ ] **Step 4: Rewrite hub READMEs for new paths**

Update `raw/research/career-beginning-tech/README.md` layers table to:

| Layer | Path |
|-------|------|
| Primary | `raw/sources/career-beginning-tech/` |
| Secondary | `raw/research/career-beginning-tech/` |
| Tertiary archive | `raw/research/career-beginning-tech/_archive/consolidate/` |

Update `raw/research/ai-advantage-expired/README.md` provenance table:

| Layer | Path |
|-------|------|
| Primary ingest | `raw/sources/ai-advantage-expired/` |
| Research | `raw/research/ai-advantage-expired/` |
| Topic note | `raw/ops/radar/topics/ai-advantage-expired.md` |

Replace wikilinks `journals/radar` → `raw/ops/radar`, `knowledge/private` → `raw/sources` or `raw/research` as appropriate, `research/radar` → `raw/research`.

- [ ] **Step 5: Commit**

```bash
git add raw knowledge research notes
git commit -m "$(cat <<'EOF'
refactor: migrate knowledge and research into raw/

Sources under raw/sources; secondary corpora under raw/research.
EOF
)"
```

---

### Task 5: Deprecation stubs for old roots

**Files:**
- Replace: `knowledge/README.md`, `research/README.md`, `journals/README.md`, `notes/README.md`, `experiments/README.md`
- Delete: empty leftover dirs under those roots (keep only README)

- [ ] **Step 1: Write identical-pattern stubs**

`knowledge/README.md`:

```markdown
# Moved

Personal knowledge trees moved to [`raw/sources/`](../raw/sources/) and [`raw/research/`](../raw/research/).

See [`raw/README.md`](../raw/README.md) and [`docs/superpowers/specs/2026-07-13-llm-wiki-layout-design.md`](../docs/superpowers/specs/2026-07-13-llm-wiki-layout-design.md).
```

`research/README.md`:

```markdown
# Moved

Research corpora live under [`raw/research/`](../raw/research/).
Radar research stubs: `raw/research/<slug>/`.
```

`journals/README.md`:

```markdown
# Moved

- Daily → [`raw/ops/daily/`](../raw/ops/daily/)
- Posts → [`raw/ops/posts/`](../raw/ops/posts/)
- Radar → [`raw/ops/radar/`](../raw/ops/radar/)
```

`notes/README.md`:

```markdown
# Moved

See [`raw/sources/notes/`](../raw/sources/notes/).
```

`experiments/README.md`:

```markdown
# Moved

See [`raw/ops/experiments/`](../raw/ops/experiments/).
```

- [ ] **Step 2: Remove empty leftover nested dirs**

```bash
# After moves, only READMEs should remain under old roots
find knowledge research journals notes experiments -type d -empty -delete 2>/dev/null || true
```

- [ ] **Step 3: Commit**

```bash
git add knowledge research journals notes experiments
git commit -m "$(cat <<'EOF'
docs: stub deprecated knowledge/research/journals roots

Point readers at raw/ until stubs can be removed.
EOF
)"
```

---

### Task 6: Schema — LAB, AGENTS, CI, personal-lab templates

**Files:**
- Modify: `LAB.md`
- Modify: `AGENTS.private.md`
- Modify: `AGENTS.md` (Never list: add `raw/`; keep old names as also-forbidden)
- Modify: `.github/workflows/boundary-check.yml`
- Rewrite: `templates/personal-lab/` scaffold to `raw/` layout
- Create: `wiki/_meta/llm-wiki-schema.md`
- Modify: `wiki/_meta/templates.md` (append concept + entity templates)

- [ ] **Step 1: Replace LAB domains table**

Domains section becomes:

```markdown
## Domains

| Path | Domain |
|------|--------|
| `wiki/` | Compiled LLM wiki — promote principles/case studies only after sanitization |
| `raw/sources/` | Ingest — never promote |
| `raw/research/` | Secondary research — never promote |
| `raw/ops/` | Daily, posts, radar, experiments — never promote |
| `docs/`, `radar/` | Repo product (library code/docs) |
```

Update Leverage Radar section path to `raw/ops/radar/`.

- [ ] **Step 2: Rewrite `AGENTS.private.md`**

```markdown
# Agent rules — personal laboratory

Extends root [AGENTS.md](AGENTS.md). When both apply in a private SoT, **this file wins**.

## Domains

### Compiled (`wiki/`)

- May create/update concepts, entities, principles, MOCs, `index.md`, `log.md`.
- Must not copy from `raw/` into `wiki/principles/` without a full generic rewrite.
- Follow `wiki/_meta/llm-wiki-schema.md` for ingest / research / consolidate / query / lint.

### Private (`raw/**`)

- May organize, summarize, link, and expand **inside `raw/` only**.
- **Must never** propose commits, branches, or PRs that add `raw/` to upstream.
- **Must never** tell the user to push personal trees to the open-source repo.

## Golden rule

If any `raw/` path influenced the answer, classify the result as **private**. It is not PR material until the sanitization checklist is all **No**.
```

- [ ] **Step 3: Update root `AGENTS.md` Never list**

Add `raw/` to the Never paths bullet. Keep `knowledge/`, `notes/`, `research/`, `journals/`, `experiments/` as never (stubs may exist privately; must not appear on upstream contribution PRs).

- [ ] **Step 4: Update boundary-check**

In `.github/workflows/boundary-check.yml`, set:

```bash
forbidden=(
  knowledge
  notes
  research
  journals
  experiments
  obsidian
  vault
  raw
)
```

- [ ] **Step 5: Write `wiki/_meta/llm-wiki-schema.md`**

```markdown
# LLM wiki schema

## Layers

| Layer | Path | Rule |
|-------|------|------|
| Raw sources | `raw/sources/` | Immutable ingest |
| Research | `raw/research/` | Drafts — not wiki truth |
| Ops | `raw/ops/` | Daily / posts / radar / experiments |
| Wiki | `wiki/` | Compiled graph |

## Operations

1. **Ingest** — read `raw/sources/<slug>/`; update concepts/entities; update `wiki/index.md`; append `wiki/log.md`.
2. **Research** — write under `raw/research/<slug>/` only.
3. **Consolidate** — promote stable synthesis to `wiki/concepts/` and optionally sanitized `wiki/principles/`; MOC link; log.
4. **Query** — answer from wiki; file good answers as new pages when asked.
5. **Lint** — fix orphans, contradictions, stale paths; suggest gaps.

## Frontmatter

```yaml
type: concept | entity | principle | moc | case-study
status: draft | active | deprecated
sources: []
private: false
```

## Dual-tree

`private: true` or any `raw/` dependency ⇒ do not open a public PR.
```

- [ ] **Step 6: Append concept + entity templates to `wiki/_meta/templates.md`**

```markdown
---

## Concept template

**Path:** `wiki/concepts/<slug>.md`

```markdown
---
type: concept
status: active
sources: []
private: false
---

# <Title>

**When to use:** <One sentence>

## Body

<Synthesis>

## Claims and tensions

- <Claim>
- <Counter / bias>

## Related

- [[concepts/<related>]]
- [[principles/<related>]]
- [[MOC/<moc>]]
```

## Entity template

**Path:** `wiki/entities/<slug>.md`

```markdown
---
type: entity
status: active
sources: []
private: false
---

# <Name>

**What it is:** <One sentence>

## Notes

<Facts worth keeping>

## Related

- [[concepts/<related>]]
```
```

- [ ] **Step 7: Restructure `templates/personal-lab/`**

Replace `knowledge/`, `notes/`, `journals/`, `research/`, `experiments/` scaffolds with:

```text
templates/personal-lab/
  raw/README.md
  raw/sources/README.md
  raw/research/README.md
  raw/ops/README.md
  raw/ops/radar/README.md   # pointer to templates/radar
  LAB.md                    # domains match new layout
  AGENTS.private.md
  README.md                 # update tree diagram
```

Remove or stub old `templates/personal-lab/knowledge|notes|journals|research|experiments` with “see raw/”.

- [ ] **Step 8: Commit**

```bash
git add LAB.md AGENTS.md AGENTS.private.md .github/workflows/boundary-check.yml \
  wiki/_meta templates/personal-lab
git commit -m "$(cat <<'EOF'
docs: adopt raw/+wiki schema in lab agents and CI

Document ingest/research/consolidate ops; forbid raw/ on public trees.
EOF
)"
```

---

### Task 7: Pilot consolidate — wiki pages for `ai-advantage-expired`

**Files:**
- Create: `wiki/concepts/post-ai-competitive-advantage.md`
- Create: `wiki/concepts/career-advantage-ladder.md`
- Create: `wiki/principles/judgment-over-generation.md`
- Modify: `wiki/MOC/engineering-practice.md`
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`
- Modify: `raw/ops/radar/topics/ai-advantage-expired.md`
- Modify: `wiki/_meta/coverage-matrix.md` (add principle row)

- [ ] **Step 1: Write `wiki/concepts/post-ai-competitive-advantage.md`**

```markdown
---
type: concept
status: active
sources:
  - raw/sources/ai-advantage-expired/x-2026-07-12-community-signal.md
  - raw/research/ai-advantage-expired/README.md
private: false
---

# Post-AI competitive advantage

**When to use:** When explaining what differentiates builders after AI access becomes universal.

## Body

AI access is infrastructure, not a moat. Community and essay consensus shifts advantage toward problem selection, judgment, taste, shipping speed, trust/distribution, and domain understanding.

## Consensus map

| Strength | Signals |
|----------|---------|
| Strongest | Problem solving · Judgment · Taste · Distribution · Shipping · Product thinking |
| Medium | AI infrastructure · Capital · Debugging · Requirements · Testing |
| Minority | Skilled trades · Recursive automation |

## Claims and tensions

- Company moats (distribution, switching costs) ≠ individual moats (judgment, audience, domain).
- “Stop learning to code” is false; code becomes floor, not ceiling.
- X/community samples over-represent vocal builders.

## Related

- [[concepts/career-advantage-ladder]]
- [[principles/judgment-over-generation]]
- [[MOC/engineering-practice]]
```

- [ ] **Step 2: Write `wiki/concepts/career-advantage-ladder.md`**

```markdown
---
type: concept
status: active
sources:
  - raw/research/ai-advantage-expired/README.md
private: false
---

# Career advantage ladder

**When to use:** Framing skill investment for engineers and juniors in the AI era.

## Body

| Stage | Advantage |
|-------|-----------|
| Previous | Knowing how to code |
| Current | Knowing how to use AI |
| Emerging | Choosing problems · judgment · shipping · trust · distribution · taste |

Treat coding + AI literacy as **floor**. Emerging skills are **ceiling**.

## Claims and tensions

- Junior anxiety (“is coding worth it?”) is the distribution channel for this idea — answer without hustle cosplay.
- AI literacy alone is not a lasting moat once everyone has it.

## Related

- [[concepts/post-ai-competitive-advantage]]
- [[principles/judgment-over-generation]]
- [[MOC/engineering-practice]]
```

- [ ] **Step 3: Write sanitized `wiki/principles/judgment-over-generation.md`**

Follow existing principle template (When to use, Body, Trade-offs, Anti-patterns, Checklist, Related). Content must have:

- Zero X handles, personal biography, employer names
- Thesis: when generation is cheap, scarce value is specifying, reviewing, selecting, and shipping outcomes
- Trade-offs: slower than raw vibe-coding; higher trust
- Anti-patterns: prompt-trick catalogs without workflow redesign; treating AI access as differentiation
- Checklist: written accept/reject rubric for model output; problem statement before generation; ship/validate loop
- Related: `[[concepts/post-ai-competitive-advantage]]`, `[[MOC/engineering-practice]]`, optionally skills principles

- [ ] **Step 4: Link from MOC**

Add under Principles in `wiki/MOC/engineering-practice.md`:

```markdown
- [[principles/judgment-over-generation]] — When generation is cheap, judgment and outcome selection become the scarce skill.
- [[concepts/post-ai-competitive-advantage]] — Post-AI moat map (concept).
- [[concepts/career-advantage-ladder]] — Career skill ladder after AI access commoditizes.
```

- [ ] **Step 5: Enrich `wiki/index.md`**

Add a **Concepts** section listing the two new concepts; ensure principles list can discover `judgment-over-generation` (or point to MOC/coverage-matrix). Keep existing dual-tree / start-here structure; do not delete existing case-study navigation.

- [ ] **Step 6: Append log + update radar topic**

Append to `wiki/log.md`:

```markdown
| 2026-07-13 | consolidate | ai-advantage-expired | `concepts/post-ai-competitive-advantage`, `concepts/career-advantage-ladder`, `principles/judgment-over-generation` | Pilot consolidate after layout migration |
```

Update `raw/ops/radar/topics/ai-advantage-expired.md` Research dossier links to `raw/sources/...`, `raw/research/...`, and wiki concepts/principle.

- [ ] **Step 7: Coverage matrix row**

Add `judgment-over-generation` as `present` in `wiki/_meta/coverage-matrix.md`.

- [ ] **Step 8: Dual-tree smoke on principle**

```bash
rg -n 'personal names|employer brands|social handles' wiki/principles/judgment-over-generation.md || echo "clean"
```

Expected: `clean`

- [ ] **Step 9: Commit**

```bash
git add wiki/concepts wiki/principles/judgment-over-generation.md wiki/MOC/engineering-practice.md \
  wiki/index.md wiki/log.md wiki/_meta/coverage-matrix.md raw/ops/radar/topics/ai-advantage-expired.md
git commit -m "$(cat <<'EOF'
feat: consolidate ai-advantage-expired into wiki concepts

Add judgment-over-generation principle and career advantage concepts.
EOF
)"
```

---

### Task 8: Lint — fix stale wikilinks and path strings

**Files:** any remaining live references under `raw/`, `wiki/`, skills, LAB (exclude historical `docs/superpowers/plans/*` and old specs unless they are operational runbooks)

- [ ] **Step 1: Grep stale paths**

```bash
rg -n 'journals/radar|knowledge/private|research/radar|journals/daily|journals/post-ideas' \
  raw wiki skills .cursor/skills .claude/skills LAB.md AGENTS.md AGENTS.private.md docs/radar templates \
  || true
```

- [ ] **Step 2: Fix every hit in operational files**

Replace with `raw/ops/radar`, `raw/sources/...`, `raw/research/...`, `raw/ops/daily`, `raw/ops/posts` as appropriate. Update `raw/ops/radar/topics/_index.md` morning link paths.

- [ ] **Step 3: Layout smoke**

```bash
ls -1 | rg '^(raw|wiki|docs|radar|knowledge|research|journals|notes|experiments)$'
test -f raw/sources/ai-advantage-expired/x-2026-07-12-community-signal.md
test -f raw/research/ai-advantage-expired/README.md
test -f wiki/concepts/post-ai-competitive-advantage.md
test -f wiki/principles/judgment-over-generation.md
test -f raw/ops/radar/topics/_index.md
```

- [ ] **Step 4: Radar unit tests still pass (no Python path deps)**

```bash
python -m pytest tests/radar -q
```

Expected: PASS (or same as pre-migration baseline).

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "$(cat <<'EOF'
fix: clear stale vault paths after LLM wiki migration

Lint pass for raw/ops and raw/research link targets.
EOF
)"
```

---

### Task 9: Final verification checklist (no code)

- [ ] **Step 1: Done criteria from spec**

```bash
echo "1. Root navigable:"; ls -d raw wiki docs radar
echo "2. Pilot files:"; \
  ls raw/sources/ai-advantage-expired/ raw/research/ai-advantage-expired/guides/; \
  ls wiki/concepts/post-ai-competitive-advantage.md wiki/concepts/career-advantage-ladder.md wiki/principles/judgment-over-generation.md
echo "3. index+log:"; rg -n 'ai-advantage|judgment-over-generation|post-ai-competitive' wiki/index.md wiki/log.md
echo "4. schema ops:"; rg -n 'Ingest|Consolidate|Lint' wiki/_meta/llm-wiki-schema.md
echo "5. stubs:"; head -n 3 knowledge/README.md research/README.md journals/README.md
```

- [ ] **Step 2: Stop**

Do **not** open upstream PR. If principle should go public later, create a separate Decide + sanitization pass.

---

## Self-review (plan vs spec)

| Spec section | Task coverage |
|--------------|---------------|
| §4 Architecture scaffold | Task 1 |
| §6 Migration ops | Task 2 |
| §6.2 Radar path updates | Task 3 |
| §6 Migration knowledge/research | Task 4 |
| §6.1 Deprecation stubs | Task 5 |
| §5 Schema + CI deny `raw/` | Task 6 |
| §7 Pilot consolidate | Task 7 |
| §9 Verification / lint | Tasks 8–9 |
| Non-goal: no upstream PR | Task 9 Step 2 |
| Non-goal: no named case-study rewrite | Hard rule + Task 7 scope |

Placeholder scan: none intentional. Career consolidate archive path uses `_archive/consolidate` (explicit). MOC `career-leverage` deferred per spec §13 — only `engineering-practice` links.
