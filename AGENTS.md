# Agent rules — AI Knowledge OS (public)

These rules bind any coding or writing agent operating on the **public** repository. Private instances have additional rules; when both are mounted, **private wins on conflict**.

## Golden rule

**When unsure whether content is public or private, treat it as private. Do not open or propose a public PR.**

## Always

- Preserve kernel architecture and invariants
- Preserve the instance wiki (never overwrite with empty scaffold)
- Keep links current; avoid duplication; suggest reorganizations; flag orphans and stale knowledge
- Strengthen capture → contextualize → decide → learn → produce
- When classification is unclear, treat content as **private**
- Propose changes via `feature/public/*` (or equivalent) and a PR with the sanitization checklist

## Never

- Delete content without recorded justification
- Duplicate knowledge
- Move documents arbitrarily
- Change architectural decisions without RFC
- Promote instance principles/case studies/journals into OSS
- Bind the product to Obsidian, Cursor, Claude, or a specific LLM
- Create or commit forbidden paths at upstream root: `knowledge/`, `notes/`, `journals/`, `experiments/`, `obsidian/`, `vault/`, `raw/`
- Use personal notes, private vault files, or unpublished research as sources for public text
- Move files from a private instance into this repository
- Assume the maintainer's biography, employer secrets, or private decisions as facts
- Paste private Obsidian metadata, local absolute paths, or internal-only URLs into public files
- Suggest that private instance files "should be upstreamed" without a full sanitization rewrite
- Push directly to `main`

### Forbidden paths (upstream root)

| Path | Status |
|------|--------|
| `knowledge/`, `notes/`, `journals/`, `experiments/`, `obsidian/`, `vault/`, `raw/` | **Forbidden** |
| `research/` | Allowed **only** as scaffold (`README.md`, `.gitkeep`) |

## Domains

| Domain | Agent may | Agent must not |
|--------|-----------|----------------|
| Framework (`contracts/`, `engine/`, `agents/`, `providers/`, `docs/`, governance) | Edit, improve, document, suggest sanitized PRs | Import private context |
| Wiki scaffold (`wiki/` structure/templates) | Update scaffold, templates | Overwrite instance knowledge or import personal notes |
| Private instance (lab only) | N/A in this repo | Treat any forbidden path at upstream root as a hard error |

## Sanitization gate (before proposing a PR)

Answer explicitly:

1. Does this change depend on a private document?
2. Was any text inspired directly by personal notes?
3. Do examples contain non-case-study personal/employer context?
4. Was any private file used as reference?
5. Is any claim knowable only to the author without public evidence?

If any answer is **yes**, **block** the PR proposal and rewrite generically — or keep the work in the private instance.

## Output classification

If the agent read or cited any private instance path while producing text, that output is **private** and must not be committed here.
