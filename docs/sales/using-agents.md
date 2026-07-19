# Using Sales Motion with agents

This feature does **not** call LLM vendor APIs from the repo. Judgement (ICP framing,
qualification refinement, verdict, content planning, drafting) runs **inside Cursor or
Claude Code** using the agent's session model, through a conversational HITL gate at every
stage — never a silent file-edit.

**Do not** add `openai`, `anthropic`, or similar SDKs. **Do not** ship a user-facing
`sales-motion` CLI. Pipeline entrypoints are shell-invoked **by the agent only**.

## Cursor IDE

1. Open the private lab repo root (vault root).
2. Ensure `.cursor/skills/sales-motion/SKILL.md` is present (synced from `agents/sales-motion/`).
3. Ask: **"Run sales motion"** (the skill should attach).
4. Answer the S1 ICP Q&A in chat, then review `raw/ops/sales/_pipeline/YYYY-MM-DD/verdict.md`
   in Obsidian.
5. Answer the S4 Go/Watch/Pivot/No-Go question directly in chat.

## Claude Code

1. Same vault root.
2. Ensure `.claude/skills/sales-motion/SKILL.md` is present.
3. Invoke the sales-motion skill / ask the same prompt.
4. Same conversational gates as Cursor — every decision happens in chat, not by hand-editing
   a file.

## What the agent does

1. Read or bootstrap `raw/ops/sales/config.yaml` from `templates/sales/config.example.yaml`,
   built through the S1 chat Q&A.
2. Run pipeline stages (ingest → qualify → beachheads → verdict-prep):

   ```bash
   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage ingest

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

   python salesmotion/pipeline/run_stages.py \
     --config raw/ops/sales/config.yaml \
     --sales-root raw/ops/sales \
     --date YYYY-MM-DD \
     --stage verdict-prep
   ```

   Artifacts land under `raw/ops/sales/_pipeline/YYYY-MM-DD/` (`signals.jsonl`,
   `qualified.jsonl`, `beachheads.json`, `verdict_prep.json`, `run_meta.json`).
3. **Using this session's model** (not external APIs): refine beachheads, write
   `verdict.md`, ask the Go/Watch/Pivot/No-Go question in chat, write the answer to
   `decisions.yaml`.
4. If `go`: build `content-plan-YYYY-MM-DD.md`, walk it item-by-item in chat, draft approved
   items into `leads/<slug>.md` or `raw/ops/posts/`.
5. **Stop** — nothing is ever sent automatically. The founder sends from their own account
   and updates lead `state` by hand or via the S6 outcome-report chat.

## Headless schedule (optional)

Use your agent CLI's **non-interactive** mode to run "resume sales motion" on a cron (e.g.
weekly) so `STATE.md` and the kill-check stay current.

- Cursor: use your project's documented headless / automation path for agent runs.
- Claude Code: use non-interactive invocation with the same vault root and skill.

Do **not** add a custom sales-motion daemon or always-on service. The scheduled agent run
**is** the scheduler — it resumes from `STATE.md` instead of starting fresh.

## Triggers

- sales motion
- demand radar
- resume sales motion / continue sales motion / sales motion status
- qualify leads
- sales verdict

## Install skill copies

Canonical skill: `agents/sales-motion/SKILL.md`. Keep `.cursor/skills/sales-motion/SKILL.md`
and `.claude/skills/sales-motion/SKILL.md` identical. See `agents/sales-motion/README.md`.

## Related

- [Skill pack](../../agents/sales-motion/README.md)
- [Contracts](../../contracts/prompts/sales/)
