# Design: Public ↔ private laboratory governance

**Status:** Active (see also root [GOVERNANCE.md](../../GOVERNANCE.md))  
**Date:** 2026-07-10

This spec is the design record for the governance model. Normative rules for contributors live in:

- [README.md](../../README.md) — constitution
- [GOVERNANCE.md](../../GOVERNANCE.md) — full RFC
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [AGENTS.md](../../AGENTS.md)

## Locked decisions

| Decision | Choice |
|----------|--------|
| Public product | Engineering wiki (not an AI platform) |
| Lab model | A1-equivalent: private SoT + `upstream` (GitHub cannot private-fork a public repo) |
| Contribution isolation | P1 (semantic branches) + P2 (clean worktree) |
| Wiki editing | W2 — laborate on `wiki/` in the private SoT; promote via sanitized PR |
| Obsidian | Physical vault = private repo root; logical domains `wiki/` × personal trees |
| Hardening | G2 — defense in depth (CI path denylist, PR template, agent rules) |

## Non-goals

- Publishing the maintainer’s personal vault
- Requiring users to store personal knowledge in this repository
- Tool-specific PKM lock-in beyond optional Obsidian-friendly markdown
