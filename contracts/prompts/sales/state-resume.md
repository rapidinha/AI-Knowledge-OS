# Stage: Estado & Retomada (S6)

## Input

- `raw/ops/sales/STATE.md` (bootstrap from `templates/sales/state.md` if missing)
- `raw/ops/sales/ledger.md`
- `raw/ops/sales/decisions.yaml` (for `last_verdict` / weeks-since-go)

## Output expectations

- Report current stage + pending human actions from `STATE.md`.
- Ask a short structured question to capture human-reported outcomes (replies,
  qualified conversations, payments) and update `ledger.md`.
- If `kill_check_weeks` has elapsed since the last `go`, surface the pivot/continue
  question — do not decide it.
- Ask explicitly what to do next: refresh signals (re-run S2→S3), chase an outcome,
  draft more, or run the kill-check.
- Rewrite `STATE.md` in place with the updated status.

## Caps

- This stage never drafts marketing content — that's S5.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **Never** auto-decide the kill/pivot check.
- **Never** auto-continue without the founder's answer to "what next."
