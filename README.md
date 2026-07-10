# AI-Knowledge-OS

Portable engineering wiki extracted from real production codebases. Principles stay company-agnostic; case studies carry evidence. Start at [wiki/index.md](wiki/index.md).

## What this repo is

- **Principles** (`wiki/principles/`) — reusable patterns with no vendor or product leakage
- **Case studies** (`wiki/case-studies/tangram/`) — how Tangram Platform implements or bends those patterns, with file paths
- **Meta** (`wiki/_meta/`) — templates, coverage matrix, extraction ledger

Source corpus for the first wave: [Tangram Platform](https://github.com/tangram-education/tangram-platform) monorepo.

Obsidian vault root should be the `wiki/` directory.

## Dual-tree rules (mandatory)

| Tree | Allowed | Forbidden |
|------|---------|-----------|
| `wiki/principles/` | Generic names ("auth service", "user table") | Company names, repo names, service names, absolute paths, product brands |
| `wiki/case-studies/tangram/` | Service names, ADRs, repo-relative evidence paths | Secrets, Terraform state, copied source blobs |

Link across trees with Obsidian-style `[[wikilinks]]`. Every note follows [[_meta/templates|the template]].

## Navigate the wiki

Open **[wiki/index.md](wiki/index.md)** — MOC hubs, meta docs, and wave plan.

| Doc | Purpose |
|-----|---------|
| [wiki/index.md](wiki/index.md) | Wiki home |
| [wiki/_meta/templates.md](wiki/_meta/templates.md) | Principle + case-study note templates |
| [wiki/_meta/coverage-matrix.md](wiki/_meta/coverage-matrix.md) | 30 topics × extraction status |
| [wiki/_meta/extraction-ledger.md](wiki/_meta/extraction-ledger.md) | Wave log + next-wave brief |

## Design

- Spec: [docs/specs/2026-07-10-wiki-knowledge-os-design.md](docs/specs/2026-07-10-wiki-knowledge-os-design.md)
- Plans: `docs/plans/`

## Status

Tangram extraction waves W1-W4 are closed. The coverage matrix has no topic rows left as `pending`; remaining non-extracted topics are marked `partial` with gaps or `out-of-scope` with reasons.
