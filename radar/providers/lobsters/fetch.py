from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

BASE = "https://lobste.rs"
UA = "ai-knowledge-os-radar/0.1"


def get_json(url: str) -> Any:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_hottest(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    for item in items:
        sid = item.get("short_id") or ""
        if not sid:
            continue
        submitter = item.get("submitter_user")
        if isinstance(submitter, dict):
            author = submitter.get("username")
        elif isinstance(submitter, str):
            author = submitter or None
        else:
            author = None
        story_url = item.get("url") or f"{BASE}/s/{sid}"
        out.append(
            {
                "id": f"lobsters:{sid}",
                "provider": "lobsters",
                "url": story_url,
                "title": item.get("title") or "",
                "ts": item.get("created_at") or "",
                "author": author,
                "text": None,
                "metrics": {
                    "score": item.get("score"),
                    "comment_count": item.get("comment_count"),
                },
                "provenance": {
                    "short_id": sid,
                    "lobsters_url": f"{BASE}/s/{sid}",
                    "tags": item.get("tags") or [],
                },
            }
        )
    return out


def fetch(tag: str = "", limit: int = 30) -> list[dict]:
    if tag:
        url = f"{BASE}/t/{tag}.json"
    else:
        url = f"{BASE}/hottest.json"
    items = get_json(url)
    if not isinstance(items, list):
        return []
    return parse_hottest(items)[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="lobsters-fetch")
    p.add_argument("--tag", default="")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(tag=args.tag, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} lobsters signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
