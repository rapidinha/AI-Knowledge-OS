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
