from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from providers.signals.pipeline.models import Cluster


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def _hint_set(row: dict[str, Any]) -> set[str]:
    hints = {str(h).lower() for h in (row.get("topics_hint") or [])}
    for w in (row.get("norm_title") or "").split():
        if len(w) > 3:
            hints.add(w)
    return hints


def correlate_enriched(
    enriched: list[dict[str, Any]],
    *,
    max_clusters: int = 12,
    topics_index: dict[str, Any] | None = None,
) -> list[Cluster]:
    _ = topics_index
    groups: list[dict[str, Any]] = []
    for row in enriched:
        hints = _hint_set(row)
        domain = _domain(row.get("canonical_url") or row.get("url") or "")
        matched = None
        for g in groups:
            if _jaccard(hints, g["hints"]) >= 0.2 or (domain and domain == g["domain"]):
                matched = g
                break
        if matched is None:
            groups.append({"hints": set(hints), "domain": domain, "rows": [row]})
        else:
            matched["hints"] |= hints
            matched["rows"].append(row)

    groups.sort(key=lambda g: (-len({r["provider"] for r in g["rows"]}), -len(g["rows"])))
    groups = groups[: max(1, max_clusters)]

    clusters: list[Cluster] = []
    for i, g in enumerate(groups, start=1):
        rows = g["rows"]
        providers = sorted({r["provider"] for r in rows})
        title = rows[0].get("title") or " ".join(sorted(g["hints"])[:4]) or f"cluster-{i}"
        clusters.append(
            Cluster(
                cluster_id=f"cl_{i:03d}",
                title=title,
                signal_ids=[r["id"] for r in rows],
                providers=providers,
                weak_signal=len(providers) == 1 and len(rows) == 1,
            )
        )
    return clusters
