---
name: trend-radar
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

2. **Topic store bootstrap**
   - If `journals/radar/topics.yaml` missing → copy `templates/radar/topics.example.yaml`.
   - Ensure `journals/radar/topics/` exists. If `_index.md` missing → copy `templates/radar/topics-index.md`.

3. **Fetch** — Run (today's date as `YYYY-MM-DD`):

   ```bash
   python providers/signals/fetch_enabled.py \
     --config journals/radar/config.yaml \
     --out journals/radar/_raw/YYYY-MM-DD.jsonl
   ```

   Note any `degraded` lines from stderr for the Executive Summary.

4. **Load** — Read jsonl + `topics.yaml` via reading files (optional: `providers.signals.lib.topics_io`). Dedupe URLs/titles if needed.

5. **Cluster and score (session model only)** — never OpenAI/Anthropic HTTP APIs or SDKs:
   - Cluster into ≤ `defaults.max_opportunities` Opportunities (ecosystem themes, not per-feed lists).
   - Prefer multi-provider Opportunities when evidence exists.
   - Bias YouTube-heavy themes toward **Influence** (content leverage).
   - Assign/create topic `slug` per Opportunity; merge with existing topics on alias/title/url overlap.
   - Update topic fields: `hit_count` (+1 once per distinct day), `last_seen`, `provider_set` union, `recent_urls` (cap 8), `status` hint (`emerging` / `validated` when hits≥3 and ≥2 providers).
   - Cap ~200 topics; set `status: retired` on oldest low-hit — **do not delete** Markdown notes.

6. **Persist topic memory (dual-write — required)**
   - Write `journals/radar/topics.yaml` (machine index).
   - For each touched topic, create/update `journals/radar/topics/<slug>.md` from `templates/radar/topic.md`:
     - Refresh **Rolling summary** (2–4 sentences; cumulative, not only today).
     - Append today's bullet under **Timeline** with wikilink to `[[journals/radar/YYYY-MM-DD]]`.
     - Merge **Sources** URLs.
   - Update `journals/radar/topics/_index.md` active/retired lists.
   - These notes are for **Obsidian and future AI summarization** — keep them readable without `_raw/`.

7. **Write daily note** — `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md`, including Topic wikilink + Recurrence from the topic graph.

8. **Stop** — No Stage 2 / wiki edits unless the user Decide's.

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
- v2 design spec: `docs/specs/2026-07-11-leverage-radar-v2-design.md`
