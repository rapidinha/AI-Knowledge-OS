"""Manual X-paste intake for sales-motion.

Connect path: founder (or agent, on the founder's instruction) pastes one JSON
object per line into raw/ops/sales/inbox/x-manual.jsonl — {url, text, ts, author?}.
No HTTP call to X, no scraping, no automation against X's ToS.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED = ("url", "text", "ts")


def _signal_id(url: str, ts: str) -> str:
    raw = f"{url}|{ts}".encode("utf-8")
    return f"x_manual:{hashlib.sha256(raw).hexdigest()[:16]}"


def _title_from_text(text: str) -> str:
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    return first_line[:120]


def parse_entry(entry: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED if not entry.get(k)]
    if missing:
        raise ValueError(f"invalid x_manual entry missing: {', '.join(missing)}")
    return {
        "id": _signal_id(entry["url"], entry["ts"]),
        "provider": "x_manual",
        "url": entry["url"],
        "title": _title_from_text(entry["text"]),
        "ts": entry["ts"],
        "author": entry.get("author"),
        "text": entry["text"],
        "metrics": {},
        "provenance": {"manual": True},
    }


def fetch(inbox_path: Path) -> list[dict[str, Any]]:
    if not inbox_path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in inbox_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            out.append(parse_entry(entry))
        except (ValueError, json.JSONDecodeError):
            continue
    return out
