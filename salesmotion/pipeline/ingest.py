from __future__ import annotations

from pathlib import Path
from typing import Any

from providers.signals.lib.dedupe import dedupe_signals
from providers.signals.sources.hn import fetch as hn_fetch
from providers.signals.sources.reddit import fetch as reddit_fetch
from providers.signals.sources.rss import fetch as rss_fetch

from salesmotion.providers.x_manual import fetch as x_manual_fetch


def fetch_channels(
    config: dict[str, Any], *, inbox_path: Path
) -> tuple[list[dict], dict[str, int], list[str]]:
    channels = config.get("channels") or {}
    raw: list[dict] = []
    counts: dict[str, int] = {}
    degraded: list[str] = []

    hn_cfg = channels.get("hn") or {}
    if hn_cfg.get("enabled"):
        try:
            signals = hn_fetch.fetch(limit=int(hn_cfg.get("limit") or 30))
            counts["hn"] = len(signals)
            raw.extend(signals)
        except Exception:
            counts["hn"] = 0
            degraded.append("hn")

    reddit_cfg = channels.get("reddit") or {}
    if reddit_cfg.get("enabled"):
        try:
            signals = reddit_fetch.fetch(
                subs=reddit_cfg.get("subreddits") or [],
                user_agent=reddit_cfg.get("user_agent") or reddit_fetch.DEFAULT_USER_AGENT,
                limit=int(reddit_cfg.get("limit") or 25),
            )
            counts["reddit"] = len(signals)
            raw.extend(signals)
        except Exception:
            counts["reddit"] = 0
            degraded.append("reddit")

    rss_cfg = channels.get("rss") or {}
    if rss_cfg.get("enabled"):
        try:
            signals = rss_fetch.fetch(
                feeds=rss_cfg.get("feeds") or [],
                limit_per_feed=int(rss_cfg.get("limit_per_feed") or 10),
            )
            counts["rss"] = len(signals)
            raw.extend(signals)
        except Exception:
            counts["rss"] = 0
            degraded.append("rss")

    x_manual_cfg = channels.get("x_manual") or {}
    if x_manual_cfg.get("enabled", True):
        signals = x_manual_fetch.fetch(inbox_path)
        counts["x_manual"] = len(signals)
        raw.extend(signals)

    return dedupe_signals(raw), counts, degraded
