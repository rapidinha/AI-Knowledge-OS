from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://hacker-news.firebaseio.com/v0"


def get_json(url: str):
    req = Request(url, headers={"User-Agent": "ai-knowledge-os-radar/0.1"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch(limit: int = 30) -> list[dict]:
    ids = get_json(f"{BASE}/topstories.json")[:limit]
    out: list[dict] = []
    for i in ids:
        item = get_json(f"{BASE}/item/{i}.json")
        if not item or item.get("type") != "story":
            continue
        url = item.get("url") or f"https://news.ycombinator.com/item?id={i}"
        ts = datetime.fromtimestamp(item.get("time", 0), tz=timezone.utc).isoformat()
        out.append(
            {
                "id": f"hn:{i}",
                "provider": "hn",
                "url": url,
                "title": item.get("title") or "",
                "ts": ts,
                "author": item.get("by"),
                "text": None,
                "metrics": {"score": item.get("score"), "descendants": item.get("descendants")},
                "provenance": {"hn_id": i, "hn_url": f"https://news.ycombinator.com/item?id={i}"},
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hn-fetch")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} hn signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
