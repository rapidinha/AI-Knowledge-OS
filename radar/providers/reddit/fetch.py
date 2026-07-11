"""Reddit hot-listing fetch for leverage radar.

Connect path:
  Enable providers.reddit.enabled: true in config.yaml
  Public JSON: https://www.reddit.com/r/{sub}/hot.json
  User-Agent from --user-agent or default (Reddit requires a descriptive UA)
  Optional OAuth env REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET (v1 uses public JSON only)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://www.reddit.com"
DEFAULT_USER_AGENT = "ai-knowledge-os-radar/0.1"


def _reddit_permalink(permalink: str) -> str:
    if permalink.startswith("http"):
        return permalink
    return f"https://www.reddit.com{permalink}"


def parse_hot_listing(payload: dict) -> list[dict]:
    out: list[dict] = []
    for child in payload.get("data", {}).get("children", []):
        if child.get("kind") != "t3":
            continue
        data = child.get("data") or {}
        fullname = data.get("name") or f"t3_{data.get('id', '')}"
        permalink = data.get("permalink") or ""
        url = data.get("url") or _reddit_permalink(permalink)
        ts = datetime.fromtimestamp(data.get("created_utc", 0), tz=timezone.utc).isoformat()
        out.append(
            {
                "id": f"reddit:{fullname}",
                "provider": "reddit",
                "url": url,
                "title": data.get("title") or "",
                "ts": ts,
                "author": data.get("author"),
                "text": None,
                "metrics": {"score": data.get("score")},
                "provenance": {
                    "permalink": _reddit_permalink(permalink),
                    "subreddit": data.get("subreddit"),
                },
            }
        )
    return out


def get_json(url: str, user_agent: str) -> dict:
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch(subs: list[str], user_agent: str = DEFAULT_USER_AGENT, limit: int = 25) -> list[dict]:
    out: list[dict] = []
    for sub in subs:
        sub = sub.strip()
        if not sub:
            continue
        params = urlencode({"limit": limit})
        url = f"{BASE}/r/{sub}/hot.json?{params}"
        payload = get_json(url, user_agent=user_agent)
        out.extend(parse_hot_listing(payload))
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="reddit-fetch")
    p.add_argument("--subs", required=True, help="Comma-separated subreddit names")
    p.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    p.add_argument("--limit", type=int, default=25, help="Max posts per subreddit")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    subs = [s.strip() for s in args.subs.split(",") if s.strip()]
    signals = fetch(subs=subs, user_agent=args.user_agent, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} reddit signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
