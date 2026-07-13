# Note templates

Every Knowledge Base note in an **instance** must follow one of the templates below.

Upstream ships templates only — no living principles or case studies. Copy categories into your private instance and write notes there.

## Shared minimum

| Field | Required |
|-------|----------|
| Title | Yes |
| **When to use** | Yes — one line |
| **Body** | Yes |
| **Related** | Yes — `[[wikilinks]]` |
| **Origin** | Yes — signal, research, decision, or prior note |

Optional across categories: **Trade-offs**, **Anti-patterns**, frontmatter (`updated`, `category`, `slug`).

---

## Principle template

**Path (instance):** `wiki/principles/<slug>.md`

**Note:** Principles are **instance-only** content. Upstream does not store personal judgment notes.

```markdown
# <Title>

**When to use:** <One sentence describing the situation where this pattern applies.>

## Body

<Decisions, mechanics, and rationale. Use generic names only.>

## Trade-offs

- <What you gain>
- <What you give up>

## Anti-patterns

- <What to avoid and why>

## Related

- [[principles/<related-slug>]]
- [[architecture/<related-slug>]]

## Origin

- <Signal, research, or decision that led to this principle>
```

---

## Case study template

**Path (instance):** `wiki/case-studies/<system>/<slug>.md`

Publish only when intentionally making a named system public.

```markdown
# <Title>

**When to use:** <When to read this case study instead of the principle alone.>

## Body

<How the named system implements or bends the pattern.>

## Trade-offs

- <Gains>
- <Costs>

## Evidence

| Area | Path | Notes |
|------|------|-------|
| <layer> | `<repo-relative/path>` | <what to look at> |

## Related

- [[principles/<slug>]]
- [[case-studies/<system>/<related-slug>]]

## Origin

- <Research, project, or insight that prompted this case study>
```

---

## Architecture template

**Path:** `wiki/architecture/<slug>.md`

```markdown
# <Title>

**When to use:** <When this system shape or boundary doc applies.>

## Body

<Components, boundaries, data flows, and invariants.>

## Related

- [[principles/<slug>]]
- [[adrs/<slug>]]

## Origin

- <Signal, RFC, or engineering decision>
```

---

## RFC template

**Path:** `wiki/rfcs/<slug>.md`

```markdown
# RFC: <Title>

**When to use:** <Problem space requiring a proposal before implementation.>

## Body

<Problem, proposed change, alternatives, open questions.>

## Related

- [[adrs/<slug-if-accepted>]]
- [[architecture/<slug>]]

## Origin

- <Signal, trend, or stakeholder request>
```

---

## ADR template

**Path:** `wiki/adrs/<slug>.md`

```markdown
# ADR: <Title>

**When to use:** <Context where this decision applies.>

## Body

<Decision, status, consequences, and supersession notes.>

## Related

- [[rfcs/<slug>]]
- [[architecture/<slug>]]

## Origin

- <Meeting, incident, or RFC that drove the decision>
```

---

## Playbook template

**Path:** `wiki/playbooks/<slug>.md`

```markdown
# <Title>

**When to use:** <Procedure trigger — e.g. incident, release, onboarding.>

## Body

<Steps, checks, rollback, and owners.>

## Related

- [[principles/<slug>]]
- [[architecture/<slug>]]

## Origin

- <Incident, postmortem, or repeated manual process>
```

---

## Research template

**Path:** `wiki/research/<slug>.md`

```markdown
# <Title>

**When to use:** <Topic worth durable memory beyond a transient working note.>

## Body

<Questions, sources, findings, open questions.>

## Related

- [[synthesis-or-principle links]]
- [[trend-analysis/<slug>]]

## Origin

- <Signal or ResearchBrief id>
```

---

## Learning path template

**Path:** `wiki/learning-paths/<slug>.md`

```markdown
# <Title>

**When to use:** <Skill or domain someone should study over time.>

## Body

<Stages, resources, exercises, completion criteria.>

## Related

- [[research/<slug>]]
- [[principles/<slug>]]

## Origin

- <Insight, gap analysis, or career goal>
```

---

## Trend analysis template

**Path:** `wiki/trend-analysis/<slug>.md`

```markdown
# <Title>

**When to use:** <Market or technology shift worth tracking over months.>

## Body

<What changed, who cares, implications, watch signals.>

## Related

- [[research/<slug>]]
- [[decision-logs/<slug>]]

## Origin

- <Signal cluster or radar run date>
```

---

## Content idea template

**Path:** `wiki/content-ideas/<slug>.md`

```markdown
# <Title>

**When to use:** <Insight ready to become a post, talk, or project.>

## Body

<Angle, audience, outline, source insights.>

## Related

- [[principles/<slug>]]
- [[research/<slug>]]

## Origin

- <Insight or synthesis note>
```

---

## Decision log template

**Path:** `wiki/decision-logs/<slug>.md`

```markdown
# <Title>

**When to use:** <Choice to prioritize, defer, or explicitly ignore.>

## Body

<Decision, ignored alternatives, rationale, review date.>

## Related

- [[principles/<slug>]]
- [[trend-analysis/<slug>]]

## Origin

- <Signal, insight, or review session>
```

---

## Checklists

### Before creating any note

- [ ] Template matches primary category
- [ ] **When to use** is one clear sentence
- [ ] **Origin** links to source artifact or note
- [ ] **Related** wikilinks present (no orphan)

### Principles (instance)

- [ ] No company leakage unless intentional case-study cross-link
- [ ] Judgment is stable enough to reuse across projects

### Case studies (instance)

- [ ] Intentional public disclosure of named system
- [ ] Evidence uses repo-relative paths only; no secrets


---

## Concept template

**Path:** `wiki/concepts/<slug>.md` (instance Knowledge Base — not an upstream corpus requirement)

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

## Related

- [[concepts/<related>]]
- [[principles/<related>]]
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
