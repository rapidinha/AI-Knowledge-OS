# Note templates

Every principle and case-study note in this wiki **must** follow one of the templates below.

## Shared structure

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

## Related

- [[principles/<related-slug>]]
- [[MOC/<domain-moc>]]
```

### Principle checklist

- [ ] Zero company leakage (no brands, repos, services, absolute paths)
- [ ] All required sections present
- [ ] Footer wikilinks include parent MOC

---

## Case study template

**Path:** `wiki/case-studies/<system>/<slug>.md`

**Hard rule:** Only publish when intentionally making a named system public. Cite repo-relative evidence paths; no secrets or copied source blobs.

```markdown
# <Title>

**When to use:** <When to read this case study instead of the principle alone.>

## Body

<How the named system implements or bends the pattern.>

## Trade-offs

- <Gains>
- <Costs>

## Anti-patterns

- <Observed or avoided mistakes>

## Evidence

| Area | Path | Notes |
|------|------|-------|
| <layer or concern> | `<repo-relative/path>` | <what to look at> |

## Deviations

- <Where the system diverges from the linked principle and why>

## Principles

- [[principles/<slug>]] — <one-line link hint>

## Related

- [[case-studies/<system>/<related-slug>]]
- [[MOC/<domain-moc>]]
```

### Case study checklist

- [ ] Intentional public disclosure of the named system
- [ ] Evidence table with repo-relative paths only
- [ ] No secrets, credentials, or source blobs
- [ ] Links back to principles and parent MOC
