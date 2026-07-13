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
