# Private instance (SoT)

**Visibility:** private GitHub repository  
**Vault:** open **this repository root** in Obsidian (`wiki/` + `raw/`)  
**Upstream library:** `rapidinha/AI-Knowledge-OS` (fetch only)

## Domains

| Path | Domain |
|------|--------|
| `wiki/` | Compiled LLM wiki — promote only after sanitization |
| `raw/sources/` | Ingest — never promote |
| `raw/research/` | Secondary research — never promote |
| `raw/ops/` | Daily, posts, radar, experiments — never promote |
| `docs/`, framework dirs | Repo product from upstream |

## Trend Radar

Copy `templates/radar/config.example.yaml` → `raw/ops/radar/config.yaml`, enable providers, run the **trend-radar** skill. See `docs/radar/using-agents.md`.

## Sync

Use `templates/instance/scripts/sync-from-upstream.sh`. Instance `wiki/` wins.

## Golden rule

Doubt ⇒ private. Never push `raw/` to upstream.
