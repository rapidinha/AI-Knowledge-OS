# Setup assist: Configure one provider

Work **one provider at a time**. Never commit secrets or live `journals/radar/config.yaml` to public upstream.

## Steps

1. **Read config** — Open `journals/radar/config.yaml` (copy from `templates/radar/config.example.yaml` if missing).
2. **Check readiness** — Use `radar.pipeline.provider_setup.check_provider_ready(name, providers.<name>)` logic or read its hint strings:
   - `product_hunt` → `PRODUCTHUNT_TOKEN`
   - `rss` → `providers.rss.feeds[]`
   - `youtube_api` → `YOUTUBE_API_KEY` + `queries` or `channel_ids`
   - `ga4` → `export_path` (local JSON export) **or** `GA4_ACCESS_TOKEN` / `GOOGLE_APPLICATION_CREDENTIALS` / `credentials_file` + `property_id`
   - `search_console` → `export_path` **or** `GSC_ACCESS_TOKEN` / `GOOGLE_APPLICATION_CREDENTIALS` / `credentials_file` + `site_url`
3. **Guide secrets via env** — Tell the user which env vars to set; never write tokens into tracked files.
4. **Enable only this provider** — Set `enabled: true` for the target provider; keep others `enabled: false` for the dry-run.
5. **Dry-run ingest**:

   ```bash
   python radar/pipeline/run_stages.py \
     --config journals/radar/config.yaml \
     --radar-root journals/radar \
     --date YYYY-MM-DD \
     --stage ingest
   ```

6. **Verify** — Inspect `run_meta.json`: provider should appear in `providers_ok`, not `providers_degraded`. Check `signals.jsonl` for expected rows.
7. **Re-enable** other providers the user wants for production runs.

## Bans

- **Never commit** API tokens, service-account JSON, or personal config to the public repo.
- **No** vendor LLM calls during setup.
