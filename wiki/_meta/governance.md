# Wiki governance

Rules for the **instance** Knowledge Base. Upstream ships this schema only; living notes live in your private instance.

## Create

- Use a required template from [[templates]] for every new note.
- Assign one **primary category** (directory) per note — no duplicate homes.
- Link to **origin**: signal, research brief, synthesis, or decision that prompted the note.
- MOCs (Maps of Content) are **indexes**, not copies of note bodies.

## Update

- Prefer **amending** existing notes over creating silent forks of the same concept.
- Set or refresh an `updated` date (frontmatter or footer) when meaning changes.
- If a note spans categories, pick one primary home and link from others.

## Review

- Run a **monthly** review (Knowledge Curator or Documentation Maintainer role).
- Check for: orphan notes, stale content, broken wikilinks, drift from templates.
- Flag duplicates and suggest merges; humans approve structural moves.

## Archive

- Move superseded notes to `_archive/` with a short **reason** in the commit or note header.
- Do not erase history without a corresponding **decision-log** entry when the choice mattered.
- Git in the instance is the version record; archive commits should be explicit.

## Version and schema

- **Git** in the private instance is the source of truth for note history.
- Structural schema changes (new categories, template fields) follow an **RFC** on the OSS framework.
- Sync from upstream must **never overwrite** living instance notes with empty scaffold files.

## Categorize

| Rule | Detail |
|------|--------|
| One primary home | Each concept lives in one category directory |
| MOCs as indexes | Curated link lists; no pasted duplicate bodies |
| Principles | Instance-only judgment — not published upstream |
| Case studies | Named evidence only when intentionally public |

See also: [GOVERNANCE.md](../../GOVERNANCE.md) (repository) · [contracts/knowledge-entry.md](../../contracts/knowledge-entry.md)
