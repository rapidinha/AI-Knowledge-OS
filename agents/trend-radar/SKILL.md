---
name: trend-radar
description: Run daily Leverage / Trend Radar discovery (pipeline stages + session synthesis, write Obsidian journal). Use when user asks for leverage radar, trend radar, daily radar, configure radar providers, run radar stage, or what deserves attention today.
---

# Leverage / Trend Radar

Vault-native daily discovery. Python pipeline stages write auditable artifacts under `_pipeline/`; cluster refinement, judgement scoring, and synthesis run **inside this session**. No vendor LLM APIs from repo tools.

## Triggers

Run when the user asks for:

- leverage radar
- trend radar
- daily radar
- configure radar providers
- run radar stage
- what deserves attention today
- morning radar / radar report

## Workflow

1. **Config bootstrap** — Read `journals/radar/config.yaml`. If missing, copy from `templates/radar/config.example.yaml` and ask the user to enable providers before continuing.

2. **Topic bootstrap**
   - If `journals/radar/topics.yaml` missing → copy `templates/radar/topics.example.yaml`.
   - Ensure `journals/radar/topics/` exists. If `_index.md` missing → copy `templates/radar/topics-index.md`.

3. **Ingest** — Run (today's date as `YYYY-MM-DD`):

   ```bash
   python providers/signals/pipeline/run_stages.py \
     --config journals/radar/config.yaml \
     --radar-root journals/radar \
     --date YYYY-MM-DD \
     --stage ingest
   ```

   Writes `journals/radar/_pipeline/YYYY-MM-DD/signals.jsonl`, `run_meta.json`, and legacy `_raw/YYYY-MM-DD.jsonl`.

4. **Enrich** — Cheap Python enrich + cache; optional session refinement per `contracts/prompts/enrich.md`:

   ```bash
   python providers/signals/pipeline/run_stages.py \
     --config journals/radar/config.yaml \
     --radar-root journals/radar \
     --date YYYY-MM-DD \
     --stage enrich
   ```

5. **Correlate + score** — Python hint-cluster + deterministic scores:

   ```bash
   python providers/signals/pipeline/run_stages.py \
     --config journals/radar/config.yaml \
     --radar-root journals/radar \
     --date YYYY-MM-DD \
     --stage correlate
   ```

6. **Session LLM (supervisor)** — Read `clusters.json` + `topics.yaml` (+ `run_meta.json`); avoid full raw signals if not needed. Follow `contracts/prompts/correlate.md`, `score.md`, and `synthesize.md`:
   - Semantic merge/refine to ≤ `defaults.max_opportunities` Opportunities (ecosystem themes, not per-feed lists).
   - Prefer multi-provider Opportunities when evidence exists.
   - Bias YouTube-heavy themes toward **Influence** (content leverage).
   - Apply judgement dimensions (novelty, hype vs substance) on top of deterministic scores.
   - `personal_relevance` is boost-only — never leak GA4/GSC raw metrics into prose.
   - Assign/create topic `slug` per Opportunity; merge with existing topics on alias/title/url overlap.
   - Update topic fields: `hit_count` (+1 once per distinct day), `last_seen`, `provider_set` union, `recent_urls` (cap 8), `status` hint (`emerging` / `validated` when hits≥3 and ≥2 providers).
   - Cap ~200 topics; set `status: retired` on oldest low-hit — **do not delete** Markdown notes.
   - **Dual-write topics (required):**
     - Write `journals/radar/topics.yaml` (machine index).
     - For each touched topic, create/update `journals/radar/topics/<slug>.md` from `templates/radar/topic.md`:
       - Refresh **Rolling summary** (2–4 sentences; cumulative, not only today).
       - Append today's bullet under **Timeline** with wikilink to `[[journals/radar/YYYY-MM-DD]]`.
       - Merge **Sources** URLs.
     - Update `journals/radar/topics/_index.md` active/retired lists.
   - Write `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md` answering leverage questions (what changed, unnoticed, deserves attention, hype, will grow, engineer impact) — **not a news list**.

7. **Executive Summary** — Include degraded providers and counts from `run_meta.json` (`providers_degraded`, `providers_ok`, `counts`).

8. **Setup assist** — When `run_meta.providers_degraded` includes setup-related failures, follow `contracts/prompts/configure-provider.md`: one provider at a time, guide secrets via env, dry-run `--stage ingest` with only that provider enabled. Never commit secrets.

9. **Stop** — No Stage 2 / wiki edits unless the user Decide's.

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

- **Do not** call OpenAI or Anthropic HTTP APIs from repo Python tools.
- **Do not** install LLM SDKs (`openai`, `anthropic`, etc.).
- **Do not** add a user-facing `radar` CLI or daemon.

## References

- Protocol: `docs/radar/protocol.md`
- Scoring hints: `docs/radar/scoring.md`
- Providers: `docs/radar/providers.md`
- Stage prompts: `contracts/prompts/` (`enrich.md`, `correlate.md`, `score.md`, `synthesize.md`, `configure-provider.md`)
- v2 design spec: `docs/superpowers/specs/2026-07-11-trend-radar-v2-design.md`
- Trend Radar pipelines design: `docs/superpowers/specs/2026-07-12-trend-radar-pipelines-design.md`
- Implementation plan: `docs/superpowers/plans/2026-07-12-trend-radar-pipelines.md`
