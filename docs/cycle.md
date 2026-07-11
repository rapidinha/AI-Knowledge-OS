# Knowledge Cycle

The Context Engine closes a recurring loop: dispersed signals become actionable context, then learning and production, then updated memory.

## Full flow

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

Compact notation (see also [engine/cycle.md](../engine/cycle.md)):

```text
Signals → Research → Synthesis → Knowledge Base → Context → Insights → Content/Projects → Learning → Update
```

Every feature must strengthen this loop. Summaries without decision, learning, or production are incomplete.

## Stages and contracts

| Stage | Primary artifacts | Agent role (reference) |
|-------|-------------------|------------------------|
| Signals | [Signal](../contracts/signal.md) | Trend Radar |
| Research | [ResearchBrief](../contracts/research-brief.md) | Research Agent |
| Synthesis | [Synthesis](../contracts/synthesis.md) | Research Agent, Engineering Analyst |
| Knowledge Base | [KnowledgeEntry](../contracts/knowledge-entry.md) | Knowledge Curator |
| Context | (read phase — principles, ADRs, paths) | All agents |
| Insights | [Insight](../contracts/insight.md), [DecisionLog](../contracts/decision-log.md) | Trend Radar, Learning Coach |
| Production | [ContentBrief](../contracts/content-brief.md) | Content Strategist |
| Learning | [LearningUpdate](../contracts/learning-update.md) | Learning Coach |
| Update | KnowledgeEntry, DecisionLog | Knowledge Curator |

Providers emit Signals. Agents consume and emit contract artifacts. Almost all writes target the **instance** store, not OSS.

## Wiki participation per stage

The instance `wiki/` is the durable memory substrate — not documentation of the public repo.

| Stage | Instance wiki role |
|-------|--------------------|
| Research | Source of **already know / already decided** — principles, prior research, decision logs inform what to explore |
| Synthesis | Destination for **trend-analysis** and research notes — what changed, what matters |
| Context | **Canonical memory** — principles, ADRs, architecture notes, learning paths |
| Insights | Basis for **what to study / what to produce** — spawns learning-path drafts and content-ideas |
| Production | **content-ideas** plus evidence links back to synthesis and insights |
| Learning | Updates to principles, learning-paths, decision-logs — KB reflects what was learned |

### How categories map to the cycle

| Wiki category | Cycle touchpoints |
|---------------|-------------------|
| principles | Context, Learning — stable judgment |
| case-studies | Context, Production — evidence |
| architecture | Context — system shape |
| rfcs / adrs | Context, Synthesis — proposals and decisions |
| playbooks | Production, Learning — repeatable procedures |
| research | Research, Synthesis — durable research memory |
| learning-paths | Insights, Learning — study trajectories |
| trend-analysis | Synthesis — market/tech memory |
| content-ideas | Production — insight → content |
| decision-logs | Insights, Learning — prioritize / ignore |

Signals and working notes may live in instance `research/` or `journals/` during exploration. Durable outcomes land in `wiki/` categories via [KnowledgeEntry](../contracts/knowledge-entry.md) contracts.

## OSS vs instance boundary

**Personal knowledge is never written into OSS.** The kernel defines shapes, agents, and reference providers. The instance records facts.

- **OSS** — contracts, engine invariants, wiki scaffold, agent packs, reference providers, institutional docs
- **Instance** — living `wiki/`, personal trees (`knowledge/`, `notes/`, `journals/`, …), all curated knowledge

On upstream sync, instance `wiki/` **wins**. See [GOVERNANCE.md](../GOVERNANCE.md).

## Orchestration

No mandatory super-agent runs the cycle. Any adapter (Cursor, Claude Code, CLI, manual workflow) may execute one agent pack or a chain. The **cycle** is the orchestration; agents are roles.

See [agents/](../agents/) for portable skill packs and [docs/radar/](radar/) for the Trend Radar reference provider.
