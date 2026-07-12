from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen

UA = "ai-knowledge-os-radar/0.1"
SETUP_HINT = (
    "Set export_path to a local GA4 runReport JSON export, or set GA4_ACCESS_TOKEN "
    "and property_id for live Analytics Data API access (lab only)."
)


def _row_key(page_path: str) -> str:
    return hashlib.sha256(page_path.encode("utf-8")).hexdigest()[:16]


def _theme_token(page_path: str) -> str:
    path = (page_path or "").strip().strip("/")
    if not path:
        return "unknown"
    segment = path.split("/")[-1]
    return segment.replace("-", " ").replace("_", " ") or path


def parse_report(payload: dict) -> list[dict]:
    out: list[dict] = []
    metric_headers = [h.get("name") for h in payload.get("metricHeaders") or []]
    for row in payload.get("rows") or []:
        dim_values = row.get("dimensionValues") or []
        page_path = (dim_values[0].get("value") if dim_values else "") or ""
        if not page_path:
            continue
        metrics: dict[str, int | float] = {}
        for idx, metric_value in enumerate(row.get("metricValues") or []):
            name = metric_headers[idx] if idx < len(metric_headers) else f"metric_{idx}"
            raw = metric_value.get("value")
            if raw is None:
                continue
            try:
                metrics[name] = int(raw) if str(raw).isdigit() else float(raw)
            except (TypeError, ValueError):
                continue
        theme = _theme_token(page_path)
        row_key = _row_key(page_path)
        out.append(
            {
                "id": f"ga4:{row_key}",
                "provider": "ga4",
                "url": page_path,
                "title": f"GA4 rising page theme: {theme}",
                "ts": "",
                "text": None,
                "metrics": metrics,
                "provenance": {"page_path": page_path, "theme": theme},
            }
        )
    return out


def _load_export(export_path: str) -> dict:
    path = Path(export_path)
    return json.loads(path.read_text(encoding="utf-8"))


def post_run_report(property_id: str, access_token: str, limit: int) -> dict:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    body = json.dumps(
        {
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "sessions"}, {"name": "screenPageViews"}],
            "limit": max(1, limit),
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
    property_id: str = "",
    credentials_file: str = "",
    export_path: str = "",
    limit: int = 20,
) -> list[dict]:
    _ = credentials_file  # reserved for service-account flows in lab configs
    if export_path:
        payload = _load_export(export_path)
        return parse_report(payload)[: max(0, limit)]

    token = os.environ.get("GA4_ACCESS_TOKEN")
    if token and property_id:
        payload = post_run_report(property_id, token, limit)
        return parse_report(payload)[: max(0, limit)]

    raise RuntimeError(SETUP_HINT)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ga4-fetch")
    p.add_argument("--property-id", default="")
    p.add_argument("--credentials-file", default="")
    p.add_argument("--export-path", default="")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(
        property_id=args.property_id,
        credentials_file=args.credentials_file,
        export_path=args.export_path,
        limit=args.limit,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} ga4 signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
