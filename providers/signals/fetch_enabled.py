from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# Allow `python providers/signals/fetch_enabled.py` from repo root (agent entrypoint).
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from providers.signals.lib.dedupe import dedupe_signals
from providers.signals.lib.io import enabled_providers, load_config
from providers.signals.pipeline.provider_setup import check_provider_ready
from providers.signals.sources.arxiv import fetch as arxiv_fetch
from providers.signals.sources.devto import fetch as devto_fetch
from providers.signals.sources.ga4 import fetch as ga4_fetch
from providers.signals.sources.github_trending import fetch as github_trending_fetch
from providers.signals.sources.hn import fetch as hn_fetch
from providers.signals.sources.lobsters import fetch as lobsters_fetch
from providers.signals.sources.product_hunt import fetch as product_hunt_fetch
from providers.signals.sources.reddit import fetch as reddit_fetch
from providers.signals.sources.rss import fetch as rss_fetch
from providers.signals.sources.search_console import fetch as search_console_fetch
from providers.signals.sources.youtube import fetch as youtube_fetch
from providers.signals.sources.youtube_api import fetch as youtube_api_fetch


def _fetch_hn(_meta: dict[str, Any]) -> list[dict]:
    return hn_fetch.fetch(limit=30)


def _fetch_github_trending(meta: dict[str, Any]) -> list[dict]:
    return github_trending_fetch.fetch(since=meta.get("since") or "daily")


def _fetch_arxiv(meta: dict[str, Any]) -> list[dict]:
    kwargs: dict[str, Any] = {}
    if meta.get("categories"):
        kwargs["categories"] = meta["categories"]
    if meta.get("max_results") is not None:
        kwargs["max_results"] = meta["max_results"]
    return arxiv_fetch.fetch(**kwargs)


def _fetch_reddit(meta: dict[str, Any]) -> list[dict]:
    subs = meta.get("subreddits") or meta.get("subs") or []
    return reddit_fetch.fetch(
        subs=subs,
        user_agent=meta.get("user_agent") or reddit_fetch.DEFAULT_USER_AGENT,
        limit=25,
    )


def _fetch_lobsters(meta: dict[str, Any]) -> list[dict]:
    return lobsters_fetch.fetch(tag=meta.get("tag") or "", limit=int(meta.get("limit") or 30))


def _fetch_devto(meta: dict[str, Any]) -> list[dict]:
    return devto_fetch.fetch(tag=meta.get("tag") or "", limit=int(meta.get("limit") or 30))


def _fetch_youtube(meta: dict[str, Any]) -> list[dict]:
    return youtube_fetch.fetch(
        channels=meta.get("channels") or [],
        max_videos_per_channel=int(meta.get("max_videos_per_channel") or 5),
    )


def _fetch_product_hunt(meta: dict[str, Any]) -> list[dict]:
    return product_hunt_fetch.fetch(limit=int(meta.get("limit") or 20))


def _fetch_rss(meta: dict[str, Any]) -> list[dict]:
    return rss_fetch.fetch(
        feeds=meta.get("feeds") or [],
        limit_per_feed=int(meta.get("limit_per_feed") or 10),
    )


def _fetch_youtube_api(meta: dict[str, Any]) -> list[dict]:
    return youtube_api_fetch.fetch(
        queries=meta.get("queries") or [],
        channel_ids=meta.get("channel_ids") or [],
        max_results=int(meta.get("max_results") or 5),
    )


def _fetch_ga4(meta: dict[str, Any]) -> list[dict]:
    return ga4_fetch.fetch(
        property_id=meta.get("property_id") or "",
        credentials_file=meta.get("credentials_file") or "",
        export_path=meta.get("export_path") or "",
        limit=int(meta.get("limit") or 20),
    )


def _fetch_search_console(meta: dict[str, Any]) -> list[dict]:
    return search_console_fetch.fetch(
        site_url=meta.get("site_url") or "",
        credentials_file=meta.get("credentials_file") or "",
        export_path=meta.get("export_path") or "",
        limit=int(meta.get("limit") or 20),
    )


PROVIDER_FETCHERS: dict[str, Callable[[dict[str, Any]], list[dict]]] = {
    "hn": _fetch_hn,
    "github_trending": _fetch_github_trending,
    "arxiv": _fetch_arxiv,
    "reddit": _fetch_reddit,
    "lobsters": _fetch_lobsters,
    "devto": _fetch_devto,
    "youtube": _fetch_youtube,
    "product_hunt": _fetch_product_hunt,
    "rss": _fetch_rss,
    "youtube_api": _fetch_youtube_api,
    "ga4": _fetch_ga4,
    "search_console": _fetch_search_console,
}


def fetch_all(config: dict[str, Any]) -> tuple[list[dict], dict[str, int], list[str]]:
    providers = config.get("providers") or {}
    raw: list[dict] = []
    counts: dict[str, int] = {}
    degraded: list[str] = []

    for name in enabled_providers(config):
        fetcher = PROVIDER_FETCHERS.get(name)
        if fetcher is None:
            print(f"skip unknown provider: {name}", file=sys.stderr)
            continue
        meta = providers.get(name) or {}
        if not isinstance(meta, dict):
            meta = {}
        ok, hint = check_provider_ready(name, meta)
        if not ok:
            print(f"{name}: degraded (setup: {hint})", file=sys.stderr)
            counts[name] = 0
            degraded.append(name)
            continue
        try:
            signals = fetcher(meta)
        except Exception as exc:
            print(f"{name}: degraded ({exc})", file=sys.stderr)
            counts[name] = 0
            degraded.append(name)
            continue
        counts[name] = len(signals)
        raw.extend(signals)

    return dedupe_signals(raw), counts, degraded


def write_jsonl(path: Path, signals: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for signal in signals:
            f.write(json.dumps(signal, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fetch-enabled")
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)

    config = load_config(args.config)
    signals, counts, _degraded = fetch_all(config)
    write_jsonl(args.out, signals)

    for name, n in sorted(counts.items()):
        print(f"{name}: {n} raw", file=sys.stderr)
    print(f"deduped: {len(signals)} → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
