# Using Leverage Radar with agents

This feature does **not** call LLM vendor APIs from the repo. Scoring and clustering run **inside Cursor or Claude Code** using the agent's session model.

**Do not** add `openai`, `anthropic`, or similar SDKs. **Do not** ship a user-facing `radar` CLI. Provider fetch scripts are shell-invoked **by the agent only**.

## Cursor IDE

1. Open the private lab repo root (vault root).
2. Ensure `.cursor/skills/leverage-radar/SKILL.md` is present (synced from `skills/leverage-radar/`).
3. Ask: **"Run today's Leverage Radar"** (the skill should attach).
4. Review `journals/radar/YYYY-MM-DD.md` in Obsidian.
5. When ready, request decisions: e.g. **"Research opportunity #1"**.

## Claude Code

1. Same vault root.
2. Ensure `.claude/skills/leverage-radar/SKILL.md` is present.
3. Invoke the leverage-radar skill / ask the same prompt.
4. Review the daily note in Obsidian.
5. Apply decisions through agent chat the same way as Cursor.

## What the agent does

1. Read or bootstrap `journals/radar/config.yaml` from `templates/radar/config.example.yaml`.
2. Run fetch aggregation:

   ```bash
   python radar/providers/fetch_enabled.py \
     --config journals/radar/config.yaml \
     --out journals/radar/_raw/YYYY-MM-DD.jsonl
   ```

3. Read the jsonl, dedupe if needed.
4. **Using this session's model** (not external APIs): cluster signals, assign categories, score dimensions, write rationale.
5. Write `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md`.
6. **Stop** — do not research unless the user decides.
7. On decision requests: update Decide fields, append `decisions.yaml`; on `research`, create `research/radar/<slug>/README.md` from `templates/radar/research-stub.md`.

## Headless schedule (optional)

Use your agent CLI's **non-interactive** mode to run the same skill prompt on a cron (e.g. nightly) so a report exists for morning Obsidian review.

- Cursor: use your project's documented headless / automation path for agent runs.
- Claude Code: use non-interactive invocation with the same vault root and skill.

Do **not** add a custom radar daemon or always-on service. The scheduled agent run **is** the scheduler.

## Triggers

Run when the user asks for:

- leverage radar
- daily radar
- what deserves attention today
- morning radar / radar report

## Install skill copies

Canonical skill: `skills/leverage-radar/SKILL.md`. Keep `.cursor/skills/leverage-radar/SKILL.md` and `.claude/skills/leverage-radar/SKILL.md` identical. See `skills/leverage-radar/README.md`.

## Related

- [Protocol](protocol.md)
- [Providers](providers.md)
- [Scoring](scoring.md)
- [Obsidian UX](obsidian.md)
