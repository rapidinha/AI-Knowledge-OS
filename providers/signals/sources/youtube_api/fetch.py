from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://www.googleapis.com/youtube/v3/search"
UA = "ai-knowledge-os-radar/0.1"


def get_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_search(payload: dict) -> list[dict]:
    out: list[dict] = []
    for item in payload.get("items", []):
        video_id = (item.get("id") or {}).get("videoId")
        if not video_id:
            continue
        snippet = item.get("snippet") or {}
        description = snippet.get("description")
        text = description if description else None
        channel_title = snippet.get("channelTitle")
        out.append(
            {
                "id": f"youtube_api:{video_id}",
                "provider": "youtube_api",
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": snippet.get("title") or "",
                "ts": snippet.get("publishedAt") or "",
                "author": channel_title,
                "text": text,
                "metrics": {},
                "provenance": {
                    "video_id": video_id,
                    "channel_title": channel_title,
                },
            }
        )
    return out


def _search_url(*, api_key: str, max_results: int, q: str | None = None, channel_id: str | None = None) -> str:
    params: dict[str, str | int] = {
        "part": "snippet",
        "type": "video",
        "maxResults": max(1, max_results),
        "key": api_key,
    }
    if q is not None:
        params["q"] = q
    if channel_id is not None:
        params["channelId"] = channel_id
    return f"{BASE}?{urlencode(params)}"


def fetch(
    api_key: str | None = None,
    queries: list[str] | None = None,
    channel_ids: list[str] | None = None,
    max_results: int = 5,
) -> list[dict]:
    resolved = api_key or os.environ.get("YOUTUBE_API_KEY")
    if not resolved:
        raise RuntimeError("YOUTUBE_API_KEY is required")

    seen: set[str] = set()
    out: list[dict] = []
    for query in queries or []:
        query = query.strip()
        if not query:
            continue
        payload = get_json(_search_url(api_key=resolved, max_results=max_results, q=query))
        for signal in parse_search(payload):
            video_id = signal["provenance"]["video_id"]
            if video_id in seen:
                continue
            seen.add(video_id)
            out.append(signal)

    for channel_id in channel_ids or []:
        channel_id = channel_id.strip()
        if not channel_id:
            continue
        payload = get_json(
            _search_url(api_key=resolved, max_results=max_results, channel_id=channel_id)
        )
        for signal in parse_search(payload):
            video_id = signal["provenance"]["video_id"]
            if video_id in seen:
                continue
            seen.add(video_id)
            out.append(signal)

    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="youtube-api-fetch")
    p.add_argument("--api-key", default=None, help="YouTube Data API key (or YOUTUBE_API_KEY env)")
    p.add_argument("--query", action="append", default=[], dest="queries")
    p.add_argument("--channel-id", action="append", default=[], dest="channel_ids")
    p.add_argument("--max-results", type=int, default=5)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(
        api_key=args.api_key,
        queries=args.queries,
        channel_ids=args.channel_ids,
        max_results=args.max_results,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} youtube_api signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
