# Agent rules — personal laboratory

Extends root [AGENTS.md](../../AGENTS.md). When both apply in a private SoT, **this file wins**.

## Domains

### Public-capable (`wiki/`, shared project docs)

- May edit and improve for later sanitized promotion.
- Must not embed private wikilink targets that would break on upstream.
- Must not copy from `knowledge/`, `notes/`, `research/`, `journals/`, `experiments/` into `wiki/` without a full generic rewrite.

### Private (`knowledge/`, `notes/`, `research/`, `journals/`, `experiments/`)

- May organize, summarize, link, and expand **inside these trees only**.
- **Must never** propose commits, branches, or PRs that add these paths to upstream.
- **Must never** tell the user to push personal trees to the open-source repo.

## Golden rule

If any private path influenced the answer, classify the result as **private**. It is not PR material until the sanitization checklist is all **No**.
