from __future__ import annotations

from typing import Any

from providers.signals.pipeline.correlate import correlate_enriched
from providers.signals.pipeline.models import Cluster


def _to_correlate_input(qualified: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for s in qualified:
        row = dict(s)
        row.setdefault("canonical_url", s.get("url", ""))
        row.setdefault("norm_title", (s.get("title") or "").lower())
        row["topics_hint"] = s.get("lexicon_hits") or []
        rows.append(row)
    return rows


def build_beachheads(qualified: list[dict[str, Any]], *, max_beachheads: int = 12) -> list[Cluster]:
    rows = _to_correlate_input(qualified)
    clusters = correlate_enriched(rows, max_clusters=max_beachheads, topics_index=None)
    by_id = {s["id"]: s for s in qualified}

    for c in clusters:
        members = [by_id[sid] for sid in c.signal_ids if sid in by_id]
        n = len(members) or 1
        intensity_avg = sum(m["pain_scores"]["intensity"] for m in members) / n
        workaround_avg = sum(m["pain_scores"]["workaround_evidence"] for m in members) / n
        wtp_avg = sum(m["pain_scores"]["willingness_to_pay_hint"] for m in members) / n
        composite = round((intensity_avg + workaround_avg + wtp_avg) / 3)
        c.scores.update(
            {
                "intensity_avg": round(intensity_avg),
                "workaround_avg": round(workaround_avg),
                "wtp_avg": round(wtp_avg),
                "composite_score": composite,
                "distinct_sources": len(set(c.providers)),
                "signal_count": len(c.signal_ids),
            }
        )
    return clusters
