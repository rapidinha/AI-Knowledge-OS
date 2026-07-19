# Stage: Content plan (S5a)

## Input

- `raw/ops/sales/_pipeline/YYYY-MM-DD/verdict.md` + `beachheads.json` (only if verdict is `go`)
- `raw/ops/radar/topics.yaml` (optional trend cross-pollination)
- `wiki/` concepts/principles touching the pain/product domain
- `raw/ops/posts/` history (anti-repetition check)
- Your brand voice/visual canon files (wherever your instance defines them, e.g.
  `wiki/concepts/<brand>-visual-system.md`, `raw/ops/posts/_craft.md`) — this stage never
  invents tone or palette, it only reads what you've already defined
- `raw/ops/sales/config.yaml`'s `product` / `goal`

## Output expectations

- Write `raw/ops/sales/content-plan-YYYY-MM-DD.md` from `templates/sales/content-plan.md`:
  queue of `beachhead → angle → format (lead_reply | brand_post | series)`.
- Every item must trace to a validated beachhead — never freelance an angle with no pain evidence.
- Check each angle against `raw/ops/posts/` history; skip angles already published.
- Walk the queue item-by-item in chat: accept / skip / hold. Write status back to the plan.

## Caps

- Do not draft full copy in this stage — that's S5b (`draft-lead.md` / `draft-post.md`).

## Bans

- **No** vendor LLM HTTP from repo tools.
- **No** drafting without first reading the brand canon files above — refuse if missing.
