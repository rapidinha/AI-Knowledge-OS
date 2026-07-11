# Leverage Radar skill — install and sync

Canonical skill body: `skills/leverage-radar/SKILL.md`.

## Install

- **Cursor:** skill lives at `.cursor/skills/leverage-radar/SKILL.md` (committed in repo)
- **Claude Code:** skill lives at `.claude/skills/leverage-radar/SKILL.md` (committed in repo)

Both copies must stay **identical** to the canonical file.

## Sync after edits

1. Edit `skills/leverage-radar/SKILL.md`
2. Copy to both agent paths:

   ```bash
   cp skills/leverage-radar/SKILL.md .cursor/skills/leverage-radar/SKILL.md
   cp skills/leverage-radar/SKILL.md .claude/skills/leverage-radar/SKILL.md
   ```

3. Commit all three files together.

## Usage

Open the private lab repo root in Cursor or Claude Code, then ask: **"Run today's Leverage Radar"**.

See `docs/radar/using-agents.md` for the full workflow.
