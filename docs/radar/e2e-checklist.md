> **Note:** Leverage Radar is a **reference signal provider** for AI Knowledge OS, not the product identity. See [ARCHITECTURE.md](../../ARCHITECTURE.md).

# Leverage Radar v2 — manual E2E checklist

Run this in a private lab worktree before merging v2 provider changes. No secrets or personal config should be committed.

## Prerequisites

- Python 3.10+
- Optional: `pip install pyyaml certifi` (PyYAML recommended for full config parsing)
- Repo root as working directory

## 1. Bootstrap private config (gitignored)

```bash
cp templates/radar/config.example.yaml journals/radar/config.yaml
cp templates/radar/topics.example.yaml journals/radar/topics.yaml
mkdir -p journals/radar/_raw
```

Edit `journals/radar/config.yaml`:

- `providers.lobsters.enabled: true`
- `providers.devto.enabled: true`
- Leave `providers.youtube.enabled: false` unless channel IDs are configured
- Disable other providers if you want a narrow smoke (optional)

**Do not commit** `config.yaml`, `topics.yaml`, or `_raw/`.

## 2. Smoke fetch (live network)

If TLS errors occur on macOS, set certifi:

```bash
export SSL_CERT_FILE="$(python3 -c 'import certifi; print(certifi.where())')"
python3 providers/signals/fetch_enabled.py \
  --config journals/radar/config.yaml \
  --out journals/radar/_raw/$(date +%Y-%m-%d)-v2-smoke.jsonl
```

**Pass criteria:**

- Exit code 0
- stderr shows non-zero counts for `lobsters` and/or `devto`
- No provider hard-crashes the whole run (per-provider degrade is OK)

Quick signal count (replace `SMOKE.jsonl` with your output path):

```bash
python3 - <<'PY'
import json, sys
from collections import Counter
path = sys.argv[1] if len(sys.argv) > 1 else "journals/radar/_raw/2026-07-11-v2-smoke.jsonl"
c = Counter()
with open(path) as f:
    for line in f:
        if line.strip():
            c[json.loads(line)["provider"]] += 1
print(dict(c), "total", sum(c.values()))
PY
```

Expect at least one signal with `"provider": "lobsters"` or `"provider": "devto"` in the JSONL.

## 3. Automated tests

```bash
python3 -m pytest tests/radar -q
```

**Pass criteria:** all tests green (offline fixtures + config wiring).

## 4. Agent path (optional full run)

1. Open the vault in Obsidian (or your editor).
2. Invoke the trend-radar skill: *"Run today's Leverage Radar"*.
3. Confirm the agent writes `journals/radar/YYYY-MM-DD.md` with Opportunities and topic dual-write under `journals/radar/topics/`.

## 5. Cleanup

- Keep `_raw/` and private YAML local only.
- Delete smoke JSONL if disk space matters; it is reproducible.

## Reference smoke (2026-07-11)

| Provider | Raw count | Notes |
|----------|-----------|-------|
| lobsters | 25 | live API returns string `submitter_user` |
| devto | 30 | tag filter `ai` |
| hn | 29 | enabled in default config |
| github_trending | 19 | enabled in default config |
| arxiv | 0 | may be empty depending on feed window |
| **deduped total** | **101** | |
