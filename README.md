# AI-Knowledge-OS

Portable **engineering wiki**: reusable principles, architectural patterns, optional public case studies, ADRs/RFCs, playbooks, and generic examples. The product is **how to think** — not the maintainer’s personal knowledge.

Start at [wiki/index.md](wiki/index.md).

## Constitution

| This project **is** | This project **is not** |
|---------------------|-------------------------|
| A library of engineering judgment | A personal Obsidian vault |
| Principles and patterns anyone can reuse | A diary, career log, or research dump |
| Optional public case studies with evidence | A dump of any one employer’s internal wiki |
| A system others can fork to build *their* knowledge OS | A requirement that your knowledge live here |

**Personal knowledge systems are sovereign.** They may *consume* this wiki; they must never be merged into it by accident. Nothing becomes public except through an explicit generalization and promotion process.

### Architectural principles

1. **Library, not Laboratory** — the open repo is the library; personal labs stay private.
2. **Open by Default, Personal by Exception** — public trees are for reusable content only.
3. **Knowledge Sovereignty** — each person owns their knowledge; this repo does not claim it.
4. **Generic Before Specific** — if it only makes sense with one person’s biography, it stays private.
5. **Explicit Promotion** — use → implement → validate → generalize → PR. Never private → commit → public.
6. **Self-Contained Public Tree** — `wiki/` must not depend on private paths.
7. **Defense in Depth** — conventions + Git + hooks + CI + agent rules.
8. **Agents Inherit the Boundary** — when unsure, treat content as **private** and do not open a public PR.

Full governance: [GOVERNANCE.md](GOVERNANCE.md) · Contributing: [CONTRIBUTING.md](CONTRIBUTING.md) · Agents: [AGENTS.md](AGENTS.md)

**Personal lab (structure only):** copy [`templates/personal-lab/`](templates/personal-lab/) into a **private** repo — never commit those trees at the public repo root.
| [docs/radar/using-agents.md](docs/radar/using-agents.md) | Leverage Radar — run with Cursor or Claude Code |

## What this repo contains

- **Principles** (`wiki/principles/`) — company-agnostic patterns
- **Case studies** (`wiki/case-studies/`) — optional; none published yet
- **Meta** (`wiki/_meta/`) — templates, coverage matrix, change ledger
- **Project docs** (`docs/`) — design specs and plans for *this* repository

For contributors to the **public** wiki, the Obsidian vault root is the `wiki/` directory.

## Dual-tree rules (mandatory)

| Tree | Allowed | Forbidden |
|------|---------|-----------|
| `wiki/principles/` | Generic names ("auth service", "user table") | Company names, repo names, service names, absolute paths, product brands |
| `wiki/case-studies/<system>/` | Intentional public evidence for a named system | Secrets, Terraform state, copied source blobs, personal notes |

Link across trees with Obsidian-style `[[wikilinks]]`. Every note follows the templates in `wiki/_meta/templates.md`.

## Navigate

| Doc | Purpose |
|-----|---------|
| [wiki/index.md](wiki/index.md) | Wiki home |
| [wiki/_meta/templates.md](wiki/_meta/templates.md) | Note templates |
| [wiki/_meta/coverage-matrix.md](wiki/_meta/coverage-matrix.md) | Principle coverage |
| [wiki/_meta/extraction-ledger.md](wiki/_meta/extraction-ledger.md) | Public change log |
| [docs/specs/](docs/specs/) | Design specs |

## Status

Public tree focuses on reusable principles. Governance for public vs personal labs is defined in [GOVERNANCE.md](GOVERNANCE.md).
