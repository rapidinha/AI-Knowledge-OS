# journals/radar (private)

Ephemeral Leverage Radar output. See `docs/radar/protocol.md`.

## Bootstrap

1. Copy `templates/radar/config.example.yaml` → `journals/radar/config.yaml`
2. Enable providers you want (`enabled: true`)
3. Set any secrets in the environment (never commit them)
4. In Cursor or Claude Code: run the **leverage-radar** skill ("Run today's Leverage Radar")

Raw signal caches land in `_raw/` (gitignored).
