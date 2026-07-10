# Agent rules — AI-Knowledge-OS (public)

These rules bind any coding or writing agent operating on the **public** repository. Personal laboratories have additional private rules; when both are mounted, **private wins on conflict**.

## Golden rule

**When unsure whether content is public or private, treat it as private. Do not open or propose a public PR.**

## Never

- Create or commit paths: `knowledge/`, `notes/`, `research/`, `journals/`, `experiments/`, `obsidian/`, `vault/`
- Use personal notes, private vault files, or unpublished research as sources for public text
- Move files from a personal lab into this repository
- Assume the maintainer’s biography, employer secrets, or private decisions as facts in principles
- Paste private Obsidian metadata, local absolute paths, or internal-only URLs into `wiki/`
- Suggest that private lab files “should be upstreamed” without a full sanitization rewrite
- Push directly to `main`

## Always

- Prefer generic principles over org-specific detail
- Anonymize examples unless writing an intentional public case study under `wiki/case-studies/`
- Keep `wiki/` self-contained (no wikilinks to private paths)
- Follow dual-tree rules in the README
- Use note templates in `wiki/_meta/templates.md`
- Propose changes via `feature/public/*` (or equivalent) and a PR with the sanitization checklist

## Domains

| Domain | Agent may | Agent must not |
|--------|-----------|----------------|
| Public (`wiki/`, `docs/`, governance) | Edit, improve, document, suggest sanitized PRs | Import private context |
| Private (lab only) | N/A in this repo | Treat any such path as a hard error if it appears |

## Sanitization gate (before proposing a PR)

Answer explicitly:

1. Does this change depend on a private document?
2. Was any text inspired directly by personal notes?
3. Do examples contain non-case-study personal/employer context?
4. Was any private file used as reference?
5. Is any claim knowable only to the author without public evidence?

If any answer is **yes**, **block** the PR proposal and rewrite generically — or keep the work in the private lab.

## Output classification

If the agent read or cited any private lab path while producing text, that output is **private** and must not be committed here.
