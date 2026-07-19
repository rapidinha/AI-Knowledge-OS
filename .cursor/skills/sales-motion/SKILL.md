---
name: sales-motion
description: Run the sales-motion validation-first GTM loop (Demand Radar pipeline stages + conversational HITL gates + brand-voiced content, only after a Go verdict). Use when user asks for sales motion, demand radar, run sales motion, resume/continue sales motion, sales motion status, qualify leads, or sales verdict.
---

# Sales Motion (validation-first GTM)

Instance-native, validation-first sales motion. Python pipeline stages (`salesmotion/`) write
auditable artifacts under `raw/ops/sales/_pipeline/`; every judgement call — ICP definition,
verdict, content planning, drafting — runs **inside this session** as a conversational HITL
gate. No vendor LLM APIs from repo tools. The skill **never** auto-sends anything.

Sibling of the `trend-radar` agent pack (`agents/trend-radar/`): where Trend Radar finds
*trends*, Demand Radar (this skill's S2–S4) finds *pain/leads* to validate a market. Reuses
the `providers/signals/` pipeline primitives (Signal model, dedupe, io, HN/Reddit/RSS
fetchers, clustering) as-is.

## Triggers

- sales motion
- run sales motion
- demand radar
- resume sales motion / continue sales motion / sales motion status
- qualify leads
- sales verdict

## Workflow

1. **S1 — ICP & Dor (session, conversational gate).** If `raw/ops/sales/config.yaml` is
   missing, copy from `templates/sales/config.example.yaml` and run a short chat Q&A per
   `contracts/prompts/sales/icp.md`: `product`, `goal`, ICP by language (not demographics),
   pain lexicon seed terms, which channels to enable. Ask one question at a time. Write
   answers into `config.yaml`. **Gate:** founder approves the built config in chat before
   continuing.

2. **S2 — Escuta (Python).** Run:

   ```bash
   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage ingest
   ```

   Pulls enabled channels (`hn`, `reddit`, `rss` via the reused `providers/signals/` source
   fetchers; `x_manual` from `raw/ops/sales/inbox/x-manual.jsonl`, pasted by the founder —
   never scraped). Writes `signals.jsonl` + `run_meta.json`.

3. **S3 — Qualificação (Python hints + session).** Run:

   ```bash
   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage qualify

   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage beachheads
   ```

   Writes `qualified.jsonl` (pain-lexicon scores) and `beachheads.json` (clustered). Per
   `contracts/prompts/sales/qualify.md`, refine in session: merge near-duplicate beachheads,
   discard false positives (sarcasm, off-topic).

4. **S4 — Veredito (session, hard gate).** Run:

   ```bash
   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage verdict-prep
   ```

   Read `verdict_prep.json`'s per-beachhead score/evidence-floor breakdown. Per
   `contracts/prompts/sales/verdict.md`, write `verdict.md` from `templates/sales/verdict.md`
   and **ask the Go/Watch/Pivot/No-Go question directly in chat**. Write the answer to
   `raw/ops/sales/decisions.yaml`. **S5 cannot run without an explicit `go` answer recorded
   here.**

5. **S5 — Conteúdo (session, only if `go`).** Per `contracts/prompts/sales/content-plan.md`:
   build `raw/ops/sales/content-plan-YYYY-MM-DD.md` from `templates/sales/content-plan.md`,
   cross-referencing `raw/ops/radar/topics.yaml`, `wiki/`, `raw/ops/posts/` history, and
   your instance's own brand voice/visual canon (wherever you've defined it — this skill
   never invents tone or palette, it only reads what you've already set up). Walk the queue
   item-by-item in chat (soft gate). For each accepted item, draft per
   `contracts/prompts/sales/draft-lead.md` or `draft-post.md` into `leads/<slug>.md` (from
   `templates/sales/lead.md`) or `raw/ops/posts/YYYY-MM-DD-<slug>.md`, `state: drafted`.
   **Gate:** show each draft in chat; only set `state: approved` on explicit approval.
   **Never** set `state: sent` — only the founder does that, after publishing from their own
   account.

6. **S6 — Estado & Retomada (session + scheduled run).** On "resume sales motion" /
   "continue sales motion" / "sales motion status": read `raw/ops/sales/STATE.md` (bootstrap
   from `templates/sales/state.md` if missing) and report current stage + pending human
   actions per `contracts/prompts/sales/state-resume.md`. Ask what to do next — refresh
   signals (re-run S2→S3), chase a lead outcome (update `ledger.md` from a founder-reported
   answer), draft more, or run the kill-check (`kill_check_weeks`, default 3, since last
   `go`). **Never** auto-continue; the scheduled agent run **is** the scheduler (no daemon),
   it just resumes from `STATE.md`.

## HITL gates (every one is a chat conversation, not a silent file-edit)

Every gate — S1 config, S4 verdict, S5 plan items, S5 drafts, S6 resume — follows the same
pattern: present the artifact in chat, ask one explicit question (multiple-choice where
possible), write the human's answer to the audit-trail file. Never infer a gate from a
pre-edited file or from silence.

## Bans

- **Do not** call OpenAI or Anthropic HTTP APIs from repo Python tools.
- **Do not** install LLM SDKs (`openai`, `anthropic`, etc.).
- **Do not** add a user-facing `sales-motion` CLI or daemon.
- **Never** auto-send a DM, email, or reply — draft only; the founder sends from their own
  account.
- **Never** scrape or automate against X/Reddit/LinkedIn ToS — `x_manual` is paste-only.
- **Never** run S5 without an explicit `go` in `decisions.yaml`.
- **Never** invent brand tone/palette — S5 must read your instance's craft/voice files and
  brand visual canon before drafting; refuse if missing.
- **Never** promote brand-voice content into shared/public knowledge without explicit review.

## References

- Sibling: `agents/trend-radar/SKILL.md`
- Using agents: `docs/sales/using-agents.md`
- Stage prompts: `contracts/prompts/sales/` (`icp.md`, `qualify.md`, `verdict.md`,
  `content-plan.md`, `draft-lead.md`, `draft-post.md`, `state-resume.md`)
- Templates: `templates/sales/`
