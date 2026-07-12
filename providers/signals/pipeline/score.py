from __future__ import annotations

from typing import Any

from providers.signals.pipeline.models import Cluster


def apply_deterministic_scores(
    clusters: list[Cluster],
    *,
    topics_index: dict[str, Any] | None = None,
    personal_tokens: set[str] | None = None,
) -> list[Cluster]:
    personal_tokens = {t.lower() for t in (personal_tokens or set())}
    topics = (topics_index or {}).get("topics") or []
    for c in clusters:
        c.scores["signal_consensus"] = len(set(c.providers))
        title_tokens = set(c.title.lower().split())
        hit = 0
        for t in topics:
            aliases = {a.lower() for a in (t.get("aliases") or [])}
            aliases.add((t.get("slug") or "").replace("-", " "))
            if title_tokens & aliases or title_tokens & set((t.get("title") or "").lower().split()):
                hit = max(hit, int(t.get("hit_count") or 0))
        c.scores["growth_velocity"] = hit
        if personal_tokens and (title_tokens & personal_tokens):
            c.scores["personal_relevance"] = len(title_tokens & personal_tokens)
        else:
            c.scores.setdefault("personal_relevance", 0)
    return clusters


def personal_tokens_from_signals(signals: list[dict[str, Any]]) -> set[str]:
    tokens: set[str] = set()
    for s in signals:
        if s.get("provider") not in {"ga4", "search_console"}:
            continue
        for part in (s.get("title") or "").lower().replace(":", " ").split():
            if len(part) > 3:
                tokens.add(part)
    return tokens
