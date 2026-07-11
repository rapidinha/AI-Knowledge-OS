---
name: leverage-radar
description: Run daily Leverage Radar discovery (fetch signals, cluster/score in-session, write Obsidian journal). Use when user asks for leverage radar, daily radar, or what deserves attention today.
---

# Leverage Radar

Vault-native daily discovery. Fetch signals, cluster and score **inside this session**, write an Obsidian daily note. No external LLM APIs.

## Triggers

Run when the user asks for:

- leverage radar
- daily radar
- what deserves attention today
- morning radar / radar report

## Workflow

1. **Config** — Read `journals/radar/config.yaml`. If missing, copy from `templates/radar/config.example.yaml` and ask the user to enable providers before continuing.

2. **Fetch** — Run (use today's date as `YYYY-MM-DD`):

   ```bash
   python radar/providers/fetch_enabled.py \
     --config journals/radar/config.yaml \
     --out journals/radar/_raw/YYYY-MM-DD.jsonl
   ```

3. **Load signals** — Read the jsonl. Dedupe with `radar/lib/dedupe.py` if duplicate URLs or titles appear.

4. **Cluster and score (session model only)** — Using **this session's model** (never OpenAI/Anthropic HTTP APIs or SDKs):
   - Cluster signals into ≤ `defaults.max_opportunities` opportunities
   - Assign leverage categories: **Knowledge** | **Influence** | **Opportunity** | **Builder**
   - Fill score dimensions from `score_dimensions` in config
   - Write a short rationale per opportunity

5. **Write daily note** — Render `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md`. Fill frontmatter (`date`, `generated_by`, `providers`, `signal_count`, `opportunity_count`) and all body sections.

6. **Stop** — Do not research, draft wiki notes, or open Stage 2 work unless the user explicitly decides.

## HITL decisions (when user requests)

Apply decisions only when the user sets a **Decide** action (in chat or by editing the daily note). Parse opportunity rank/slug/title from `journals/radar/YYYY-MM-DD.md`.

Bootstrap `journals/radar/decisions.yaml` from `templates/radar/decisions.example.yaml` if missing.

| Action | Steps |
|--------|-------|
| **research** | Set `Decide: research` on the opportunity; append row to `decisions.yaml` (`date`, `slug`, `action`, `at`); create `research/radar/<slug>/README.md` from `templates/radar/research-stub.md` |
| **ignore** | Set `Decide: ignore`; move to Ignore section if needed; append `decisions.yaml` |
| **watch** | Set `Decide: watch`; add to Worth Watching; append `decisions.yaml` |
| **known** | Set `Decide: known`; link existing note if present; append `decisions.yaml` |
| **merge** | Set `Decide: merge`; add wikilink to existing topic only — **do not** auto-edit `wiki/` or principles; append `decisions.yaml` |

**No autonomous research.** Wait for explicit user approval before creating research stubs.

## Bans

- **Do not** call OpenAI or Anthropic HTTP APIs.
- **Do not** install LLM SDKs (`openai`, `anthropic`, etc.).
- **Do not** add a user-facing `radar` CLI or daemon.

## References

- Protocol: `docs/radar/protocol.md`
- Scoring hints: `docs/radar/scoring.md`
- Providers: `docs/radar/providers.md`
