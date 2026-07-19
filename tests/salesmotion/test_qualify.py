import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline.qualify import qualify_batch, qualify_signal

LEXICON = {
    "intensity_terms": ["hate", "so frustrating"],
    "workaround_terms": ["manually", "spreadsheet"],
    "willingness_to_pay_terms": ["would pay for", "shut up and take my money"],
}


def test_qualify_signal_scores_and_hits():
    signal = {
        "id": "hn:1",
        "provider": "hn",
        "title": "I hate doing this manually every week",
        "text": None,
    }
    out = qualify_signal(signal, pain_lexicon=LEXICON)
    assert out["pain_scores"]["intensity"] == 25
    assert out["pain_scores"]["workaround_evidence"] == 25
    assert out["pain_scores"]["willingness_to_pay_hint"] == 0
    assert out["lexicon_hits"] == ["hate", "manually"]
    # original fields preserved
    assert out["id"] == "hn:1"


def test_qualify_signal_scores_multiple_term_hits():
    signal = {
        "id": "hn:2",
        "provider": "hn",
        "title": "hate hate so frustrating manually spreadsheet",
        "text": None,
    }
    out = qualify_signal(signal, pain_lexicon=LEXICON)
    assert out["pain_scores"]["intensity"] == 50  # both intensity terms match; 2 hits * 25 = 50
    assert out["pain_scores"]["workaround_evidence"] == 50


def test_qualify_signal_no_hits_scores_zero():
    signal = {"id": "hn:3", "provider": "hn", "title": "unrelated title", "text": None}
    out = qualify_signal(signal, pain_lexicon=LEXICON)
    assert out["pain_scores"] == {
        "intensity": 0,
        "workaround_evidence": 0,
        "willingness_to_pay_hint": 0,
    }
    assert out["lexicon_hits"] == []


def test_qualify_batch_processes_all_signals():
    signals = [
        {"id": "hn:1", "provider": "hn", "title": "I would pay for this", "text": None},
        {"id": "hn:2", "provider": "hn", "title": "no pain here", "text": None},
    ]
    out = qualify_batch(signals, pain_lexicon=LEXICON)
    assert len(out) == 2
    assert out[0]["pain_scores"]["willingness_to_pay_hint"] == 25
    assert out[1]["pain_scores"]["willingness_to_pay_hint"] == 0
