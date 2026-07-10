# Contributing to AI-Knowledge-OS

Thank you for helping grow a **reusable engineering wiki**. Please read the [constitution in the README](README.md) and [GOVERNANCE.md](GOVERNANCE.md) before opening a PR.

## What to contribute

| Welcome | Not welcome |
|---------|-------------|
| Generic principles and patterns | Personal notes, journals, highlights |
| Public case studies with evidence paths | Secrets, credentials, private URLs |
| ADRs/RFCs/playbooks that strangers can apply | Content that only makes sense with your biography |
| Fixes to templates, MOCs, typos | Dumps from a private Obsidian vault |

## Classification (short)

1. Would a stranger reuse this without your personal context? If **no** → do not submit.
2. Prefer **principles** (no org names) over case studies when possible.
3. Case studies must stay free of secrets and copied source blobs.
4. When unsure → **do not** open a PR; ask in an issue.

## Pull request process

1. Branch from the latest `main`.
2. Keep the diff inside allowed paths (`wiki/`, `docs/`, top-level project docs).
3. Complete the PR template sanitization checklist (all answers **No** for private dependence).
4. Ensure CI `boundary-check` passes.
5. Link related issues; explain *why* the change is reusable.

## Dual-tree rules

- `wiki/principles/` — no company, product, or absolute paths.
- `wiki/case-studies/<org>/` — evidence allowed; no secrets.

Follow `wiki/_meta/templates.md`.

## Local preview

Open the `wiki/` folder as an Obsidian vault (or any markdown preview). Public contributions should not require files outside `wiki/` and `docs/`.
