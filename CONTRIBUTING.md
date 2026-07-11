# Contributing to AI Knowledge OS

Thank you for helping grow the **Context Engine** framework. Please read the [constitution in the README](README.md) and [GOVERNANCE.md](GOVERNANCE.md) before opening a PR.

This repository is a **Protocol Kernel** — contracts, cycle, agents, providers, and docs — not a personal knowledge base. Your living Knowledge Base belongs in a **private instance** copied from [`templates/instance/`](templates/instance/).

## What to contribute

| Welcome | Not welcome |
|---------|-------------|
| Contract schemas and engine protocol improvements | Personal notes, journals, highlights |
| Agent and provider packs | Secrets, credentials, private URLs |
| Wiki **scaffold** (templates, structure) | Living instance wiki content |
| Institutional and feature docs | Content that only makes sense with your biography |
| Generic examples strangers can apply | Dumps from a private vault |

## Classification (short)

1. Is this a **framework** artifact (contract, engine rule, agent, provider, doc, scaffold)? If **no** → do not submit.
2. Would a stranger reuse this without your personal context? If **no** → do not submit.
3. When unsure → **do not** open a PR; ask in an issue.

## Pull request process

1. Branch from the latest `main` (prefer `feature/public/<topic>`).
2. Keep the diff inside allowed paths: `contracts/`, `engine/`, `agents/`, `providers/`, `wiki/` (scaffold only), `docs/`, top-level institutional docs.
3. Complete the PR template sanitization checklist (all answers **No** for private dependence).
4. Ensure CI `boundary-check` passes.
5. Link related issues; explain *why* the change improves the framework.

## Private instance vs upstream

- **Instance `wiki/`** is your long-term Knowledge Base — it does not get promoted upstream by default.
- Upstream `wiki/` is **scaffold only** (templates, categories, empty structure).
- Sync policy: **instance wiki wins**. See [GOVERNANCE.md](GOVERNANCE.md) §4.

## Local preview

Open `wiki/` as a markdown preview or Obsidian vault to inspect scaffold structure. Framework contributions should not require files outside allowed public paths.
