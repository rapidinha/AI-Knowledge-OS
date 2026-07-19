# Stage: Draft — lead reply (S5b)

## Input

- An accepted `content-plan-YYYY-MM-DD.md` item with `format: lead_reply`
- The originating signal's context (from `qualified.jsonl` / `beachheads.json`)
- `raw/ops/posts/_craft.md` (tone, Builder + Engineering Leader positioning)

## Output expectations

- Write `raw/ops/sales/leads/<slug>.md` from `templates/sales/lead.md`:
  context + draft + `state: drafted`.
- Permission-first tone: help before selling. No cold-pitch opener.
- Show the draft in chat; only set `state: approved` on explicit founder approval.

## Caps

- One lead draft per plan item.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **Never** set `state: sent` — only the founder does that, after sending from their own account.
- **Never** send, post, or reply automatically.
