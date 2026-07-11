from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://dev.to/api/articles"
UA = "ai-knowledge-os-radar/0.1"


def get_json(url: str) -> Any:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_articles(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    for item in items:
        aid = item.get("id")
        if aid is None:
            continue
        user = item.get("user") or {}
        out.append(
            {
                "id": f"devto:{aid}",
                "provider": "devto",
                "url": item.get("url") or "",
                "title": item.get("title") or "",
                "ts": item.get("published_timestamp") or "",
                "author": user.get("username"),
                "text": None,
                "metrics": {
                    "public_reactions_count": item.get("public_reactions_count"),
                    "comments_count": item.get("comments_count"),
                },
                "provenance": {"devto_id": aid, "tag_list": item.get("tag_list") or []},
            }
        )
    return out


def fetch(tag: str = "", limit: int = 30) -> list[dict]:
    params: dict[str, Any] = {"per_page": max(1, min(limit, 100))}
    if tag:
        params["tag"] = tag
    url = f"{BASE}?{urlencode(params)}"
    items = get_json(url)
    if not isinstance(items, list):
        return []
    return parse_articles(items)[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="devto-fetch")
    p.add_argument("--tag", default="")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(tag=args.tag, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} devto signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
