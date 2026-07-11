from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# Allow `python radar/providers/fetch_enabled.py` from repo root (agent entrypoint).
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from radar.lib.dedupe import dedupe_signals
from radar.lib.io import enabled_providers, load_config
from radar.providers.arxiv import fetch as arxiv_fetch
from radar.providers.github_trending import fetch as github_trending_fetch
from radar.providers.hn import fetch as hn_fetch
from radar.providers.reddit import fetch as reddit_fetch


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


PROVIDER_FETCHERS: dict[str, Callable[[dict[str, Any]], list[dict]]] = {
    "hn": _fetch_hn,
    "github_trending": _fetch_github_trending,
    "arxiv": _fetch_arxiv,
    "reddit": _fetch_reddit,
}


def fetch_all(config: dict[str, Any]) -> tuple[list[dict], dict[str, int]]:
    providers = config.get("providers") or {}
    raw: list[dict] = []
    counts: dict[str, int] = {}

    for name in enabled_providers(config):
        fetcher = PROVIDER_FETCHERS.get(name)
        if fetcher is None:
            print(f"skip unknown provider: {name}", file=sys.stderr)
            continue
        meta = providers.get(name) or {}
        if not isinstance(meta, dict):
            meta = {}
        signals = fetcher(meta)
        counts[name] = len(signals)
        raw.extend(signals)

    return dedupe_signals(raw), counts


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
    signals, counts = fetch_all(config)
    write_jsonl(args.out, signals)

    for name, n in sorted(counts.items()):
        print(f"{name}: {n} raw", file=sys.stderr)
    print(f"deduped: {len(signals)} → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
