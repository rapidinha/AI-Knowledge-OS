# Stage: Qualificação (S3)

## Input

- `raw/ops/sales/_pipeline/YYYY-MM-DD/qualified.jsonl` (Python pain-lexicon scores already applied)
- `raw/ops/sales/_pipeline/YYYY-MM-DD/beachheads.json` (Python clustering already applied)

## Output expectations

- Merge near-duplicate beachheads that Python's jaccard clustering split apart.
- Discard false positives: sarcasm, off-topic lexicon matches, spam.
- Do not invent new beachheads from signals Python didn't cluster.

## Caps

- Refine only clusters already present in `beachheads.json`.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **No** pasting full raw signal text into promotable or OSS-bound text.
