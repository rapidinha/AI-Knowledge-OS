# Getting Started

This guide walks you from the public **Protocol Kernel** to a running **private instance** and your first closed loop.

## 1. Clone or fork the public framework

The public repository ships contracts, engine protocol, agent packs, reference providers, wiki scaffold, and institutional docs — not anyone's living knowledge.

```bash
git clone https://github.com/rapidinha/AI-Knowledge-OS.git
cd AI-Knowledge-OS
```

Read the constitution first:

- [VISION.md](../VISION.md) — what AI Knowledge OS is and refuses to become
- [MISSION.md](../MISSION.md) — the problem and promise
- [ARCHITECTURE.md](../ARCHITECTURE.md) — Protocol Kernel layers

If you plan to contribute framework improvements, use a **public fork** for PR branches only. Your daily work lives in a **private instance** (see below).

## 2. Create a private instance from the template

GitHub does not allow a private fork of a public repo. Create a **private repository** that tracks upstream as a remote.

```bash
gh repo create <you>/AI-Knowledge-OS-instance --private --clone
cd AI-Knowledge-OS-instance
git remote add upstream https://github.com/rapidinha/AI-Knowledge-OS.git
git fetch upstream
git checkout -B main upstream/main
```

Copy the instance template into your repo root:

```bash
cp -R templates/instance/knowledge .
cp -R templates/instance/notes .
cp -R templates/instance/research .
cp -R templates/instance/journals .
cp -R templates/instance/experiments .
cp templates/instance/LAB.md ./LAB.md
cp templates/instance/AGENTS.private.md ./AGENTS.private.md
```

Edit `LAB.md` with your remotes and commit to your private origin. Your **living Knowledge Base** grows under `wiki/` in this private repo — never in the public upstream tree.

## 3. Sync policy — instance wiki wins

When you pull framework updates from upstream, **your instance wiki is never overwritten** with empty scaffold files. Upstream sync only fills in missing paths.

See [GOVERNANCE.md](../GOVERNANCE.md) for the full dual-identity model.

A sync script will ship at `templates/instance/scripts/sync-from-upstream.sh` (added in a later Phase 1 task). Until then, manually merge framework paths (`contracts/`, `engine/`, `agents/`, `providers/`, `docs/`, institutional root docs) and use `--ignore-existing` semantics for `wiki/`.

**Rule:** instance `wiki/` wins. Scaffold from OSS only creates files that do not yet exist.

## 4. Optional — enable Trend Radar / Leverage Radar

Leverage Radar is a **reference signal provider**, not the product identity. It fetches multi-source signals and feeds the Trend Radar agent pack.

To enable in your instance:

1. Copy radar config: `cp templates/radar/config.example.yaml journals/radar/config.yaml`
2. Enable desired sources in `config.yaml`
3. Install the Trend Radar agent skill from `agents/trend-radar/` (or `.cursor/skills/trend-radar/` / `.claude/skills/trend-radar/` adapter copies)
4. Run the daily fetch and agent clustering per [docs/radar/](radar/)

No provider is required to use the Protocol Kernel. Radar is optional reference infrastructure.

## 5. First loop — one signal → one insight note

Run a minimal closed loop to validate your instance:

1. **Capture** — obtain one Signal (from Trend Radar fetch, a manual URL, or any provider). See [contracts/signal.md](../contracts/signal.md).
2. **Contextualize** — skim what you already know in instance `wiki/` (principles, prior research, decision logs).
3. **Decide** — write one [Insight](../contracts/insight.md) answering an implicit question the signal raised: `question`, `answer`, `action`, `based_on[]`.
4. **Record** — save the insight as a note in your instance wiki (e.g. `wiki/trend-analysis/` or `wiki/research/`). Use [wiki/_meta/templates.md](../wiki/_meta/templates.md).
5. **Close** — link the insight back to the signal origin. Optionally log what you ignored in `wiki/decision-logs/`.

Personal knowledge stays in your private instance. The public OSS tree defines **shapes and protocols** only.

Next: read [cycle.md](cycle.md) for the full flow and wiki participation table.
