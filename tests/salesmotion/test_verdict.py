import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline.verdict import DEFAULT_THRESHOLDS, evaluate_beachhead


def test_go_eligible_when_score_and_floor_both_met():
    scores = {"composite_score": 70, "signal_count": 6, "distinct_sources": 2}
    out = evaluate_beachhead(scores)
    assert out["recommendation"] == "go_eligible"
    assert out["evidence_floor_met"] is True
    assert out["composite_score"] == 70


def test_high_score_capped_at_watch_when_floor_unmet():
    scores = {"composite_score": 90, "signal_count": 2, "distinct_sources": 1}
    out = evaluate_beachhead(scores)
    assert out["evidence_floor_met"] is False
    assert out["recommendation"] == "watch"


def test_low_score_is_no_go():
    scores = {"composite_score": 10, "signal_count": 10, "distinct_sources": 3}
    out = evaluate_beachhead(scores)
    assert out["recommendation"] == "no_go"


def test_thresholds_are_overridable():
    scores = {"composite_score": 50, "signal_count": 5, "distinct_sources": 2}
    out = evaluate_beachhead(scores, thresholds={"go_threshold": 40})
    assert out["recommendation"] == "go_eligible"
    assert out["thresholds_used"]["go_threshold"] == 40
    assert out["thresholds_used"]["watch_threshold"] == DEFAULT_THRESHOLDS["watch_threshold"]
