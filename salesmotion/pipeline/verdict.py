from __future__ import annotations

from typing import Any

DEFAULT_THRESHOLDS: dict[str, int] = {
    "go_threshold": 65,
    "watch_threshold": 40,
    "min_signals_for_go": 5,
    "min_sources_for_go": 2,
}


def evaluate_beachhead(
    beachhead_scores: dict[str, Any], *, thresholds: dict[str, Any] | None = None
) -> dict[str, Any]:
    t = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    composite = beachhead_scores.get("composite_score", 0)
    signal_count = beachhead_scores.get("signal_count", 0)
    distinct_sources = beachhead_scores.get("distinct_sources", 0)

    evidence_floor_met = (
        signal_count >= t["min_signals_for_go"] and distinct_sources >= t["min_sources_for_go"]
    )

    if composite >= t["go_threshold"] and evidence_floor_met:
        recommendation = "go_eligible"
    elif composite >= t["watch_threshold"]:
        recommendation = "watch"
    else:
        recommendation = "no_go"

    return {
        "composite_score": composite,
        "evidence_floor_met": evidence_floor_met,
        "recommendation": recommendation,
        "thresholds_used": t,
    }
