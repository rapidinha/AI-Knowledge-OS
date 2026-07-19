import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline.beachheads import build_beachheads

QUALIFIED = [
    {
        "id": "hn:1",
        "provider": "hn",
        "url": "https://a.test/1",
        "title": "hate doing this manually",
        "text": None,
        "pain_scores": {"intensity": 100, "workaround_evidence": 50, "willingness_to_pay_hint": 0},
        "lexicon_hits": ["hate", "manually"],
    },
    {
        "id": "reddit:2",
        "provider": "reddit",
        "url": "https://b.test/2",
        "title": "manually doing this too, hate it",
        "text": None,
        "pain_scores": {"intensity": 100, "workaround_evidence": 50, "willingness_to_pay_hint": 0},
        "lexicon_hits": ["hate", "manually"],
    },
    {
        "id": "hn:3",
        "provider": "hn",
        "url": "https://c.test/3",
        "title": "totally unrelated database benchmark",
        "text": None,
        "pain_scores": {"intensity": 0, "workaround_evidence": 0, "willingness_to_pay_hint": 0},
        "lexicon_hits": [],
    },
]


def test_build_beachheads_groups_shared_lexicon_hits():
    beachheads = build_beachheads(QUALIFIED, max_beachheads=12)
    multi_source = [b for b in beachheads if b.scores.get("distinct_sources", 0) >= 2]
    assert multi_source, "expected a beachhead spanning hn + reddit"

    b = multi_source[0]
    assert b.scores["signal_count"] == 2
    assert b.scores["intensity_avg"] == 100
    assert b.scores["workaround_avg"] == 50
    assert b.scores["wtp_avg"] == 0
    assert b.scores["composite_score"] == 50  # round((100+50+0)/3)


def test_build_beachheads_respects_max_beachheads():
    beachheads = build_beachheads(QUALIFIED, max_beachheads=1)
    assert len(beachheads) == 1
