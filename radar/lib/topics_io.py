from __future__ import annotations

from pathlib import Path
from typing import Any

EMPTY: dict[str, Any] = {"version": 1, "updated_at": None, "topics": []}


def load_topics(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "updated_at": None, "topics": []}
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
    except Exception:
        return {"version": 1, "updated_at": None, "topics": []}
    if not isinstance(data, dict):
        return {"version": 1, "updated_at": None, "topics": []}
    topics = data.get("topics") or []
    if not isinstance(topics, list):
        topics = []
    return {
        "version": int(data.get("version") or 1),
        "updated_at": data.get("updated_at"),
        "topics": topics,
    }


def save_topics(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore

        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except Exception:
        # ponytail: minimal fallback without PyYAML — enough for empty bootstrap
        path.write_text("version: 1\nupdated_at: null\ntopics: []\n", encoding="utf-8")
