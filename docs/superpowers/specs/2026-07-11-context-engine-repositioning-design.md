# Design: AI Knowledge OS as Context Engine (Protocol Kernel)

**Status:** Accepted  
**Date:** 2026-07-11  
**Approach:** Protocol Kernel (Approach 1)  
**Scope:** Strategic repositioning — identity, architecture, docs, governance, roadmap (not an implementation slice)

---

## 0. Decisions locked in brainstorming

| Decision | Choice |
|----------|--------|
| Public repo role | Open-source **Context Engine framework** (not a content library) |
| Runtime model | **Protocol-first** — contracts + schemas + portable agent skills; code/providers optional |
| Upstream wiki | **Scaffold only** — structure, templates, governance |
| Success metric | **Closed loop** — signals → learning → production, recurring and measurable |
| Maintainer knowledge | Principles, case studies, and living KB stay in the **private vault + private GitHub only** |
| Architecture style | **Protocol Kernel** — not full-stack opinionated runtime, not spec-only library |

### Immutable premises

1. The **instance wiki** remains the canonical long-term knowledge store for the user.
2. The project stays **tool-agnostic** (no hard dependency on Obsidian, Cursor, Claude, ChatGPT, or any single LLM).
3. Every feature must strengthen **capture → contextualize → decide → learn → produce**.
4. Documentation is a **product**, with structure, governance, and continuous maintenance.
5. AI engines, data sources, and interfaces must be **replaceable** without changing the essence of AI Knowledge OS.

---

## 1. Vision and positioning

### Product identity

| | |
|--|--|
| **Name** | AI Knowledge OS |
| **Category** | Context Engine (protocol kernel) for technology professionals |
| **Not** | A wiki product, a PKM app, a news aggregator, a prompt pack, or an “agent framework” brand |

### One-line positioning

An open-source system that turns dispersed signals into **actionable context** and closes the loop through **learning and production** — without locking users to a specific tool.

### Problem

Technology professionals have too much information and too little context. The bottleneck is not storing notes; it is continuously knowing what deserves attention, what changed, what to study next, and how to turn that into content, projects, or career progress.

### Mission

Help users continuously answer questions they have not asked yet — but should.

Examples of those questions:

- Which technology just left hype and entered real adoption?
- What actually deserves my attention this week?
- What changed since I last studied this topic?
- Is there a trend still being ignored?
- Which topic has low competition for content creation?
- Which technologies will likely matter in the next months?
- What should I study now given my history?
- How do I turn this learning into content, projects, or professional growth?

### North-star metric

**Closed loop, measurable:** signal → research → synthesis → knowledge base (instance wiki) → insight → content/project → learning → continuous update of context.

### Dual identity (OSS vs instance)

| Layer | What it is | Where it lives |
|-------|------------|----------------|
| **OSS Framework** | Protocols, schemas, wiki scaffold, agents, reference providers, institutional docs | Public repository |
| **Instance** | Living memory, principles, case studies, journals, personal research | Private vault + private GitHub |

The public repo does **not** host the maintainer’s knowledge. The public wiki is **structure + templates**. The instance wiki is the **Knowledge Base**.

### Positioning shift vs today

| Today | After |
|-------|--------|
| Identity = engineering wiki | Identity = Context Engine |
| Wiki = the product | Wiki = memory module (scaffold in OSS) |
| Leverage Radar = emerging feature | Radar = reference signal provider |
| Public principles in upstream | Principles/case studies only in private instance |
| “Library of judgment” | “Kernel of context protocols” |

---

## 2. Architecture — Protocol Kernel

### Mental model

```text
┌─────────────────────────────────────────────────────────┐
│                    INSTANCE (private)                     │
│  wiki/ (living KB) · research/ · journals/ · knowledge/ │
│  outputs: insights, content drafts, learning plans      │
└──────────────────────────▲──────────────────────────────┘
                           │ read/write via contracts
┌──────────────────────────┴──────────────────────────────┐
│              AI KNOWLEDGE OS — PROTOCOL KERNEL (OSS)     │
│  Contracts → Agents → Providers (ref) → Adapters         │
│  (schemas)   (skills)  (radar, …)        (IDE/CLI/…)   │
└─────────────────────────────────────────────────────────┘
```

The kernel does not “decide alone.” It defines **what** circulates (artifact types) and **how** the cycle closes. Any compatible agent/runtime executes the protocols.

### Layers

| Layer | Responsibility | Replaceable without breaking the product? |
|-------|----------------|-------------------------------------------|
| **Contracts** | Schemas: Signal, ResearchBrief, Synthesis, Insight, Decision, LearningUpdate, ContentBrief, KnowledgeEntry | No (core) |
| **Cycle** | Order and invariants: capture → contextualize → decide → learn → produce | No |
| **Wiki schema** | Categories, templates, frontmatter, memory rules | Evolves via RFC |
| **Agents** | Specialized roles as portable skill packs | Yes |
| **Providers** | Signal sources (HN, arXiv, …) — reference, not identity | Yes |
| **Adapters** | Cursor, Claude Code, CLI, hooks — optional | Yes |
| **Instance store** | User markdown/YAML following contracts | Yes |

### Decisions on current assets

| Asset | Decision | Why |
|-------|----------|-----|
| `wiki/` in OSS | **Repurpose** → Knowledge Base *scaffold* (empty/templates) | Remains central as memory shape; stops being the product |
| Current principles/case studies | **Remain private only** (not in OSS) | OSS = framework; maintainer knowledge stays sovereign |
| `radar/` | **Promote** → `providers/signals/` (reference) | Best existing embryo of signals → context |
| Skills (`leverage-radar`) | **Promote** → packs under `agents/` | Agents are protocol interfaces, not one-off features |
| `GOVERNANCE.md` dual-tree | **Keep essence**, rewrite narrative | Public/private boundary still critical; OSS ≠ principles library |
| `templates/personal-lab/` | **Promote** → `templates/instance/` | Lab becomes the instance model |
| Radar specs under `docs/` | **Demote** to provider docs | Must not compete with Vision/Architecture of the product |
| Private trees (`knowledge/`, `journals/`, …) | **Keep** instance-only; CI blocks on OSS root | Already aligned |

### Minimum contracts (artifacts)

1. **Signal** — typed raw event (source, URL, timestamp, tags)
2. **ResearchBrief** — focused exploration of a theme/signal
3. **Synthesis** — what changed / what matters (not a generic summary)
4. **KnowledgeEntry** — note in the instance wiki (category + links)
5. **Insight** — implicit question answered + suggested action
6. **DecisionLog** — what was decided or ignored, and why
7. **ContentBrief / ProjectBrief** — bridge to production
8. **LearningUpdate** — what was learned and how it updates the KB

Every provider/agent declares which artifacts it **emits** and **consumes**.

### Invariants (5–10 year)

1. Kernel is tool-agnostic — no adapter is mandatory  
2. Instance sovereignty — living memory never uploads without sanitization  
3. Cycle over features — new capability enters only if it strengthens the cycle  
4. Substitutability — providers, agents, and adapters are pluggable  
5. Docs as product — institutional documentation versioned with the kernel  

### Explicitly out of kernel scope

Proprietary UI, mandatory cloud sync, universal “trend ranking” as product identity, hosting user vaults, binding to a single LLM vendor.

### Private wiki guarantee (invariant)

The **instance private wiki** is the canonical place where the user records and maintains long-term knowledge. It:

- is **not removed** or replaced by the OSS framework  
- does **not migrate** into the public repository  
- remains the living Knowledge Base of the private vault/GitHub  
- is **read/written by the kernel via contracts**; never treated as “product content”

**Merge policy on upstream sync:** instance `wiki/` **wins**. Scaffold from OSS only creates files that do not yet exist. Sync must never overwrite living instance knowledge with empty templates.

---

## 3. Repository organization (OSS)

```text
AI-Knowledge-OS/                    # public — Protocol Kernel
├── README.md
├── VISION.md
├── MISSION.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── ROADMAP.md
├── FAQ.md
├── GLOSSARY.md
├── AGENTS.md
├── LICENSE
│
├── docs/
│   ├── index.md                    # Documentation Index
│   ├── getting-started.md
│   ├── cycle.md
│   ├── maintenance.md
│   ├── specs/
│   └── plans/
│
├── contracts/                      # schemas + cycle artifact definitions
├── engine/                         # cycle protocol (no mandatory runtime)
│   ├── cycle.md
│   └── invariants.md
│
├── wiki/                           # Knowledge Base SCAFFOLD only
│   ├── index.md
│   ├── _meta/
│   ├── principles/
│   ├── case-studies/
│   ├── architecture/
│   ├── rfcs/
│   ├── adrs/
│   ├── playbooks/
│   ├── research/
│   ├── learning-paths/
│   ├── trend-analysis/
│   ├── content-ideas/
│   └── decision-logs/
│
├── research/                       # research workspace scaffold (working notes; instance fills)
│                                   # distinct from wiki/research/ (durable KB category)
├── prompts/
├── agents/                         # portable skill packs
├── providers/                      # reference implementations
│   └── signals/                    # current radar migrated here
├── integrations/                   # optional adapters
├── templates/
│   └── instance/                   # former personal-lab template
├── examples/                       # sanitized demos (never maintainer vault)
└── assets/
```

**OSS root must never contain personal knowledge.** CI continues to reject `knowledge/`, `notes/`, `journals/`, `experiments/`, `obsidian/`, `vault/` at upstream root — and rejects a “full” wiki that is not scaffold/examples.

### Instance layout (private — preserved)

```text
(private-repo)/
├── wiki/                    # living KB (principles, case studies, MOCs, …)
├── knowledge/
├── notes/
├── research/
├── journals/
├── experiments/
├── …                        # selective sync of kernel (contracts, agents, providers)
└── LAB.md
```

**Sync rule:** pull from upstream only framework paths. Instance `wiki/` is never overwritten by empty OSS scaffold.

---

## 4. Wiki as system memory

### Upstream wiki

Scaffold: directories + `wiki/_meta/templates.md` + governance rules. No maintainer principles or case studies.

### Instance wiki categories

| Category | Role in the cycle |
|----------|-------------------|
| Principles | Stable reusable judgment |
| Case Studies | Contextualized evidence |
| Architecture | How this instance/system is modeled |
| RFCs / ADRs | Proposals and decisions |
| Playbooks | Repeatable procedures |
| Research | In-progress exploration → may become principle/insight |
| Learning Paths | Study trajectories tied to history |
| Trend Analysis | Signal syntheses → market memory |
| Content Ideas | Bridge insight → production |
| Decision Logs | What was prioritized or ignored |

### How documents relate

Signals/research feed Research & Trend Analysis → synthesis becomes Principle/ADR/Playbook or Decision Log → insights spawn Content Ideas / Learning Paths → production and learning update the KB again.

The wiki is not “documentation of the repo”; it is the **durable memory substrate** of the Context Engine for that instance.

---

## 5. Documentation strategy

| Document | Function |
|----------|----------|
| **README** | Entry: what it is / is not, 30-second cycle, essential links |
| **VISION** | 5–10 year future: Context Engine, tool-agnostic, instance sovereignty |
| **MISSION** | Problem + promise: continuous context → closed loop |
| **ARCHITECTURE** | Protocol Kernel, layers, contracts, what is pluggable |
| **docs/index** | Documentation Index |
| **docs/getting-started** | Clone kernel → create instance → first closed loop |
| **docs/cycle** | Knowledge flow + wiki roles |
| **CONTRIBUTING** | How to contribute to the *framework* (not anyone’s vault) |
| **GOVERNANCE** | OSS vs instance; promotion rules; sanitization; wiki merge policy |
| **ROADMAP** | Phased incremental value |
| **FAQ** | “Is this a PKM?”, “Do I need Obsidian?”, “Where does my knowledge live?” |
| **GLOSSARY** | Signal, Insight, Instance, Kernel, Provider, Agent pack, … |
| **AGENTS** | Always/Never rules for AIs on OSS and instance |
| **docs/maintenance** | How docs and scaffold avoid rot |

Radar/feature specs remain under `docs/specs/` and `docs/plans/` as framework history, not product identity.

---

## 6. Knowledge flow

```text
Market signals (providers)
    ↓
Research (Research Agent → ResearchBrief)
    ↓
Synthesis (what changed / what matters)
    ↓
Knowledge Base (INSTANCE wiki — long-term memory)
    ↓
Context (history + KB + recent signals)
    ↓
Insights (implicit questions answered + action)
    ↓
Content / Projects (ContentBrief, ProjectBrief)
    ↓
Learning (LearningUpdate)
    ↓
Continuous update of wiki + decision logs
```

### Wiki participation per stage

| Stage | Instance wiki role |
|-------|--------------------|
| Research | Source of “already know / already decided” |
| Synthesis | Destination for Trend Analysis / Research notes |
| Context | Canonical memory (principles, ADRs, learning paths) |
| Insights | Basis for “what to study / what to produce” |
| Production | Content Ideas + evidence links |
| Learning | Updates to principles, paths, decision logs |

Personal knowledge is never written into OSS. The kernel defines *shapes* and *agents*; the instance records *facts*.

---

## 7. Agents

Skill packs under `agents/`. Each agent: **inputs** (contracts) → **outputs** (contracts) → **write target** (almost always the instance).

| Agent | Responsibility | Emits | Never does |
|-------|----------------|-------|------------|
| **Trend Radar** | Capture/cluster/score signals; “what deserves attention” | Signal, Insight (attention) | Decide career alone; flood wiki without curation |
| **Research Agent** | Deepen a theme/signal | ResearchBrief, Synthesis | Publish to OSS; invent evidence |
| **Knowledge Curator** | Integrate syntheses into KB; links; anti-duplication; orphans | KnowledgeEntry | Delete without justification; move arbitrarily |
| **Learning Coach** | “What to study now” given history + gaps | LearningUpdate, Learning Path drafts | Replace human judgment |
| **Content Strategist** | Turn insights into ContentBrief / angles | ContentBrief, Content Ideas | Spam ideas unanchored in KB |
| **Engineering Analyst** | Technical signals/ADRs → actionable patterns | Synthesis, Principle *drafts* (instance) | Promote principles to OSS without sanitization |
| **Documentation Maintainer** | Keep kernel docs/scaffold and wiki meta healthy | Doc PRs, drift issues | Change ADRs/architecture without RFC |

**Orchestration:** no mandatory super-agent. Any adapter may run one pack or a chain. The **cycle** is the orchestration; agents are roles.

**Current Radar:** reference implementation under `providers/signals/` + skill `agents/trend-radar/`.

---

## 8. Maintenance

1. **Docs as product** — README/Vision/Architecture reviewed each roadmap phase  
2. **Drift checks** — Documentation Maintainer: dead links, orphan folders, docs contradicting ARCHITECTURE  
3. **Scaffold CI** — upstream fails on personal content or a non-scaffold “full” wiki  
4. **Semantic versioning of contracts** — breaking schema change = RFC + major  
5. **Reference providers** — optional; external API failure degrades, does not kill the kernel  
6. **One source of truth per concept** — no silent divergent duplicates across OSS docs and instance without links  

---

## 9. Wiki governance (instance)

| Action | Rule |
|--------|------|
| Create | Required template (`_meta/templates`); explicit category; link to origin (signal/research/decision) |
| Update | Prefer amend + `updated`; no silent forks of the same concept |
| Review | Cadence (e.g. monthly) via Curator/Documentation Maintainer: orphans, drift, broken links |
| Archive | Move to `_archive/` with reason; do not erase history without Decision Log |
| Version | Git in the instance; structural schema changes → RFC on OSS |
| Categorize | One primary home; MOCs as indexes, not copies |

Long-term consistency = stable templates + `KnowledgeEntry` contracts + agents that *suggest* reorg + humans who *approve* structural moves.

---

## 10. Rules for AI (`AGENTS.md`)

### Always

- Preserve kernel architecture and invariants  
- Preserve the instance wiki (never overwrite with empty scaffold)  
- Keep links current; avoid duplication; suggest reorganizations; flag orphans and stale knowledge  
- Strengthen capture → contextualize → decide → learn → produce  
- When classification is unclear, treat content as **private**

### Never

- Delete content without recorded justification  
- Duplicate knowledge  
- Move documents arbitrarily  
- Change architectural decisions without RFC  
- Promote instance principles/case studies/journals into OSS  
- Bind the product to Obsidian, Cursor, Claude, or a specific LLM  

---

## 11. Roadmap

| Phase | Delivery | Value |
|-------|----------|--------|
| **1 — Restructuring** | OSS = Protocol Kernel; institutional docs; wiki scaffold; private lab intact; Radar relocated as reference | Correct identity; zero loss of private KB |
| **2 — Research engine** | ResearchBrief/Synthesis contracts + Research Agent pack | Signals become structured exploration |
| **3 — Trend Radar** | Stable Trend Radar pack + pluggable providers | Recurring “what deserves attention” |
| **4 — Content Intelligence** | Content Strategist + Content Ideas in wiki | Insight → production |
| **5 — Learning Intelligence** | Learning Coach + Learning Paths | History → what to study |
| **6 — Context Engine** | Full measurable closed loop; loop metrics | North star proven |

Each phase requires: versioned contract, agent pack, updated docs, sanitized example — without depending on the maintainer’s private KB.

---

## 12. Philosophy

1. **Context over Information** — actionable context > more data  
2. **Signal over Noise** — attention is the scarce resource  
3. **Action over Summaries** — synthesis without decision/production is incomplete  
4. **Knowledge as Infrastructure** — instance wiki is infrastructure, not an optional diary  
5. **Cycle over Features** — features serve the cycle or do not enter  
6. **Instance Sovereignty** — user memory is sovereign  
7. **Protocol over Platform** — contracts > tools  
8. **Tool Agnostic** — adapters are peripheral  
9. **Knowledge Compounds** — each loop improves the KB  
10. **Docs as Product** — documentation governed like software  
11. **Human-Centered Intelligence** — AI proposes; humans approve structural change  
12. **Continuous Evolution** — RFCs, not silent rewrites  

Note: “open” applies to the **framework**, not to the user’s vault.

---

## 13. Risks and trade-offs

| Risk | Mitigation |
|------|------------|
| OSS looks “empty” | Getting Started + sanitized examples + cycle demos |
| Sync wipes private wiki | Merge policy *instance wins* + instance template tests |
| Radar reclaims product identity | Naming + README: provider ≠ product |
| Docs rot | Documentation Maintainer + per-phase checklist |
| Agent scope creep | Packs only enter when tied to a cycle contract |
| Public fork vs private lab confusion | GOVERNANCE + FAQ (existing dual-tree, new narrative) |

**Central trade-off:** protocol-first delays UI “wow,” but buys 5–10 years of substitutability.

---

## 14. Recommendations (after this spec)

1. Freeze this design; write the Phase 1 implementation plan next  
2. Do not move or empty the private instance wiki — only enforce sync policy  
3. Re-scaffold public `wiki/` only on a **public restructuring branch**, never inside the lab vault as a destructive overwrite  
4. Treat current principles/case studies as **out of OSS**  
5. Migrate `radar/` → `providers/signals/` + `agents/trend-radar/` across Phases 1–3 per the plan  

---

## 15. Success criteria for this repositioning

- A stranger reading README understands: Context Engine framework, not PKM/wiki product  
- Maintainer’s private wiki and principles remain intact and authoritative for personal knowledge  
- Clear separation: contracts/agents/providers (OSS) vs living KB (instance)  
- Roadmap phases each deliver closed-loop value without requiring private content upstream  
- Tool-agnostic claim holds: no required Obsidian/Cursor/Claude path to use the kernel  

---

## 16. Non-goals (this design)

- Implementing Phase 1–6 in this document  
- Migrating private principles into OSS examples  
- Building a hosted product or mandatory UI  
- Replacing Leverage Radar behavior in this spec (relocation only, behavior via later plans)  
