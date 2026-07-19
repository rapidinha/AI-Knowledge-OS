# Stage: Veredito (S4)

## Input

- `raw/ops/sales/_pipeline/YYYY-MM-DD/verdict_prep.json` (deterministic composite score +
  evidence-floor check per beachhead, from `salesmotion.pipeline.verdict.evaluate_beachhead`)
- `raw/ops/sales/config.yaml`'s `verdict` thresholds

## Output expectations

- Write `raw/ops/sales/_pipeline/YYYY-MM-DD/verdict.md` from `templates/sales/verdict.md`:
  score/evidence breakdown per beachhead.
- If overriding a threshold's recommendation, write the rationale in `verdict.md` —
  never a silent override.
- Ask the Go / Watch / Pivot / No-Go question **directly in chat**, one beachhead at a
  time if multiple exist.
- Write the founder's answer to `raw/ops/sales/decisions.yaml`
  (date, beachhead_slug, verdict, decided_by: human_chat).

## Caps

- Only verdict beachheads present in `verdict_prep.json`; do not invent new ones here.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **No** advancing to S5 without an explicit `go` recorded in `decisions.yaml`.
