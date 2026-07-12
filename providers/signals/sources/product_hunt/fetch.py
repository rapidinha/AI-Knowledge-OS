from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"
UA = "ai-knowledge-os-radar/0.1"


def _posts_query(first: int) -> str:
    return f"""
query {{
  posts(first: {first}) {{
    edges {{
      node {{
        id
        name
        tagline
        url
        votesCount
        createdAt
      }}
    }}
  }}
}}
"""


def post_graphql(query: str, token: str) -> Any:
    body = json.dumps({"query": query}).encode("utf-8")
    req = Request(
        GRAPHQL_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_posts(payload: dict) -> list[dict]:
    out: list[dict] = []
    edges = payload.get("data", {}).get("posts", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node") or {}
        pid = node.get("id")
        if pid is None:
            continue
        out.append(
            {
                "id": f"product_hunt:{pid}",
                "provider": "product_hunt",
                "url": node.get("url") or "",
                "title": node.get("name") or "",
                "ts": node.get("createdAt") or "",
                "text": node.get("tagline"),
                "metrics": {"votesCount": node.get("votesCount")},
                "provenance": {"product_hunt_id": pid},
            }
        )
    return out


def fetch(token: str | None = None, limit: int = 20) -> list[dict]:
    resolved = token or os.environ.get("PRODUCTHUNT_TOKEN")
    if not resolved:
        raise RuntimeError("PRODUCTHUNT_TOKEN is required")
    first = max(1, limit)
    payload = post_graphql(_posts_query(first), resolved)
    return parse_posts(payload)[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="product-hunt-fetch")
    p.add_argument("--token", default=None, help="Product Hunt API token (or PRODUCTHUNT_TOKEN env)")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(token=args.token, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} product_hunt signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
