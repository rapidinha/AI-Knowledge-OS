from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from providers.signals.lib.dedupe import canonicalize_url
from providers.signals.pipeline.models import enrich_signal, validate_signal


def _load_cache(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_cache(path: Path | None, cache: dict[str, dict[str, Any]]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def enrich_batch(
    signals: list[dict[str, Any]],
    *,
    cache_path: Path | None = None,
    max_batch: int = 200,
) -> tuple[list[dict[str, Any]], int]:
    cache = _load_cache(cache_path)
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    invalid = 0
    for raw in signals[: max(0, max_batch)]:
        try:
            validate_signal(raw)
        except ValueError:
            invalid += 1
            continue
        key = canonicalize_url(raw.get("url", "")) or raw["id"]
        if key in seen:
            continue
        seen.add(key)
        if key in cache:
            row = dict(cache[key])
            row["enrich_meta"] = {**(row.get("enrich_meta") or {}), "cache_hit": True}
            out.append(row)
            continue
        row = enrich_signal(raw, cache_hit=False)
        cache[key] = row
        out.append(row)
    _save_cache(cache_path, cache)
    return out, invalid
