# Stage: Enrich

## Input

- `journals/radar/_pipeline/YYYY-MM-DD/signals.jsonl` (or already-enriched batches from a prior partial run)

## Output expectations

- Refine `entities[]` and `topics_hint[]` **only when** Python heuristics (tags, title tokens, provenance) are insufficient.
- Preserve `canonical_url`, `norm_title`, and `enrich_meta` from the Python stage; do not re-fetch URLs.
- Write refined rows back to `enriched.jsonl` via the agent session (or instruct re-run of `--stage enrich` if no semantic changes needed).

## Caps

- Respect `defaults.max_signals_per_enrich_batch` from `journals/radar/config.yaml` (default 200).
- Process in batches; do not load the full raw corpus into one prompt if avoidable.

## Bans

- **No** OpenAI, Anthropic, or other vendor LLM HTTP calls from repo Python tools.
- **No** new LLM SDK dependencies in `radar/`.
- Enrichment LLM work is **session-only** (supervisor agent), not embedded in pipeline scripts.
