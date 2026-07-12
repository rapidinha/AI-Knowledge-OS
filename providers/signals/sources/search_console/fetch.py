from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

UA = "ai-knowledge-os-radar/0.1"
SETUP_HINT = (
    "Set export_path to a local Search Console query export JSON, or set "
    "GSC_ACCESS_TOKEN and site_url for live API access (lab only)."
)


def _row_key(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]


def parse_query(payload: dict) -> list[dict]:
    out: list[dict] = []
    for row in payload.get("rows") or []:
        keys = row.get("keys") or []
        query = (keys[0] if keys else "") or ""
        if not query:
            continue
        metrics = {
            k: row[k]
            for k in ("clicks", "impressions", "ctr", "position")
            if k in row
        }
        row_key = _row_key(query)
        out.append(
            {
                "id": f"search_console:{row_key}",
                "provider": "search_console",
                "url": "",
                "title": f"GSC rising query: {query}",
                "ts": "",
                "text": None,
                "metrics": metrics,
                "provenance": {"query": query},
            }
        )
    return out


def _load_export(export_path: str) -> dict:
    path = Path(export_path)
    return json.loads(path.read_text(encoding="utf-8"))


def get_search_analytics(site_url: str, access_token: str, limit: int) -> dict:
    params = urlencode({"siteUrl": site_url})
    url = f"https://www.googleapis.com/webmasters/v3/sites/{site_url}/searchAnalytics/query?{params}"
    body = json.dumps(
        {
            "startDate": "2026-07-01",
            "endDate": "2026-07-12",
            "dimensions": ["query"],
            "rowLimit": max(1, limit),
        }
    ).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
        method="POST",
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch(
    site_url: str = "",
    credentials_file: str = "",
    export_path: str = "",
    limit: int = 20,
) -> list[dict]:
    _ = credentials_file  # reserved for service-account flows in lab configs
    if export_path:
        payload = _load_export(export_path)
        return parse_query(payload)[: max(0, limit)]

    token = os.environ.get("GSC_ACCESS_TOKEN")
    if token and site_url:
        payload = get_search_analytics(site_url, token, limit)
        return parse_query(payload)[: max(0, limit)]

    raise RuntimeError(SETUP_HINT)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="search-console-fetch")
    p.add_argument("--site-url", default="")
    p.add_argument("--credentials-file", default="")
    p.add_argument("--export-path", default="")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(
        site_url=args.site_url,
        credentials_file=args.credentials_file,
        export_path=args.export_path,
        limit=args.limit,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} search_console signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
