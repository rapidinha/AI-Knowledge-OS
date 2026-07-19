from __future__ import annotations

from typing import Any

_POINTS_PER_HIT = 25
_MAX_SCORE = 100


def _score_terms(haystack: str, terms: list[str]) -> tuple[int, list[str]]:
    hits = [t for t in terms if t.lower() in haystack]
    score = min(_MAX_SCORE, len(hits) * _POINTS_PER_HIT)
    return score, hits


def qualify_signal(signal: dict[str, Any], *, pain_lexicon: dict[str, list[str]]) -> dict[str, Any]:
    haystack = f"{signal.get('title', '')} {signal.get('text') or ''}".lower()
    intensity_score, intensity_hits = _score_terms(haystack, pain_lexicon.get("intensity_terms") or [])
    workaround_score, workaround_hits = _score_terms(haystack, pain_lexicon.get("workaround_terms") or [])
    wtp_score, wtp_hits = _score_terms(haystack, pain_lexicon.get("willingness_to_pay_terms") or [])

    out = dict(signal)
    out["pain_scores"] = {
        "intensity": intensity_score,
        "workaround_evidence": workaround_score,
        "willingness_to_pay_hint": wtp_score,
    }
    out["lexicon_hits"] = sorted(set(intensity_hits + workaround_hits + wtp_hits))
    return out


def qualify_batch(
    signals: list[dict[str, Any]], *, pain_lexicon: dict[str, list[str]]
) -> list[dict[str, Any]]:
    return [qualify_signal(s, pain_lexicon=pain_lexicon) for s in signals]
