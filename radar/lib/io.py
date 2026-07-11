from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """Minimal subset parser used only if PyYAML is absent — prefer PyYAML in labs."""
    # ponytail: ceiling = nested maps one level under providers.*; upgrade = require PyYAML
    import re

    data: dict[str, Any] = {"providers": {}}
    current: str | None = None
    for line in text.splitlines():
        if re.match(r"^providers:\s*$", line):
            continue
        m = re.match(r"^  ([a-z0-9_]+):\s*$", line)
        if m:
            current = m.group(1)
            data["providers"][current] = {}
            continue
        m = re.match(r"^    enabled:\s*(true|false)\s*$", line)
        if m and current:
            data["providers"][current]["enabled"] = m.group(1) == "true"
    return data


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    return _parse_simple_yaml(text)


def enabled_providers(config: dict[str, Any]) -> list[str]:
    providers = config.get("providers") or {}
    return sorted(
        name
        for name, meta in providers.items()
        if isinstance(meta, dict) and meta.get("enabled") is True
    )
