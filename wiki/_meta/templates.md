# Note templates

Every principle and case-study note in this wiki **must** follow one of the templates below. Deviations break cross-linking, coverage tracking, and extraction review.

## Shared structure

Both templates use the same section order. Sections 5–6 differ by tree; section 7 is required on every note.

| # | Section | Required |
|---|---------|----------|
| 1 | Title + one-line **When to use** | Yes |
| 2 | Body (decisions, mechanics) | Yes |
| 3 | **Trade-offs** | Yes |
| 4 | **Anti-patterns** | Yes |
| 5 | Tree-specific (see below) | Yes |
| 6 | Tree-specific (see below) | Yes |
| 7 | `[[wikilinks]]` footer | Yes |

---

## Principle template

**Path:** `wiki/principles/<slug>.md`

**Hard rule:** No company names, repo names, service names, absolute paths, or product brands anywhere in the note.

```markdown
# <Title>

**When to use:** <One sentence describing the situation where this pattern applies.>

## Body

<Decisions, mechanics, and rationale. Use generic names only (e.g. "auth service", "user table").>

## Trade-offs

- <What you gain>
- <What you give up>

## Anti-patterns

- <What to avoid and why>

## Checklist for a new project

- [ ] <Concrete step an engineer can verify before shipping>
- [ ] <Another step>

## Case studies

- [[case-studies/tangram/<slug>]] — <one-line link hint>

## Related

- [[principles/<related-slug>]]
- [[MOC/<domain-moc>]]
```

### Principle enforcement checklist

Before marking a principle `extracted` in [[coverage-matrix]]:

- [ ] Zero Tangram leakage (no brands, repos, services, absolute paths)
- [ ] All seven sections present
- [ ] At least one `[[case-studies/tangram/...]]` link (or explicit "no case study yet" in matrix gap column)
- [ ] Footer wikilinks include parent MOC

---

## Case study template

**Path:** `wiki/case-studies/tangram/<slug>.md`

**Hard rule:** Must cite evidence paths under the Tangram Platform monorepo. Service names, ADRs, and repo-relative paths are allowed.

```markdown
# <Title> (Tangram)

**When to use:** <One sentence: when to read this case study instead of the principle alone.>

## Body

<How Tangram implements or bends the pattern. Name services, modules, and decisions explicitly.>

## Trade-offs

- <Tangram-specific gains>
- <Tangram-specific costs>

## Anti-patterns

- <Observed or avoided mistakes in this codebase>

## Evidence

| Area | Path | Notes |
|------|------|-------|
| <layer or concern> | `<repo-relative/path>` | <what to look at> |

## Deviations

- <Where Tangram diverges from the linked principle and why, if intentional>

## Principles

- [[principles/<slug>]] — <one-line link hint>

## Related

- [[case-studies/tangram/<related-slug>]]
- [[MOC/<domain-moc>]]
```

### Case study enforcement checklist

Before marking a case study `extracted` in [[coverage-matrix]]:

- [ ] Every claim backed by at least one evidence path
- [ ] Paths are repo-relative under `tangram-platform` (no secrets, no state files)
- [ ] Linked principle note exists or gap documented in matrix
- [ ] **Deviations** section explicit (use "None" if fully aligned)
- [ ] Footer wikilinks include parent MOC

---

## Wikilink conventions

- Principles → case studies: `[[case-studies/tangram/<slug>]]`
- Case studies → principles: `[[principles/<slug>]]`
- Both → MOCs: `[[MOC/<name>]]`
- Index hub: `[[index]]`

Use descriptive slugs (`layered-io-boundaries`, not `note-1`).
