# Stage: Correlate

## Input

- `journals/radar/_pipeline/YYYY-MM-DD/enriched.jsonl`
- `journals/radar/topics.yaml` (recent topics for merge hints)

## Output expectations

- Semantic merge and refine Python hint-clusters in `clusters.json`.
- Final opportunity count ≤ `defaults.max_opportunities` (typically 7).
- **Prefer multi-provider themes** when overlapping evidence exists across feeds.
- Assign or merge `slug` per cluster using topic alias/title overlap from `topics.yaml`.
- Set `rationale_hint` and `weak_signal` where a cluster is single-source or thin.

## Caps

- Start from Python `correlate` output (`defaults.max_clusters`, default 12); reduce to ≤ `max_opportunities` in session.
- Do not expand cluster count beyond config caps.

## Bans

- **No** vendor LLM HTTP from repo tools.
- Correlation prose and merge decisions are **session-only**.
