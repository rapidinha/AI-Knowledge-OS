import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.lobsters import fetch as lobsters_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "lobsters_hottest.json"


def test_parse_hottest_json():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = lobsters_fetch.parse_hottest(payload)
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "lobsters:abc123"
    assert s["provider"] == "lobsters"
    assert s["title"].startswith("Agent skills")
    assert s["url"] == "https://example.com/skills"
    assert s["metrics"]["score"] == 42
    assert s["provenance"]["tags"] == ["ai", "practices"]


def test_fetch_uses_get_json(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(lobsters_fetch, "get_json", lambda url: payload)
    signals = lobsters_fetch.fetch(limit=10)
    assert len(signals) == 1


def test_parse_hottest_string_submitter():
    payload = [
        {
            "short_id": "xyz99",
            "created_at": "2026-07-11T12:00:00.000-05:00",
            "title": "Live API shape",
            "url": "https://example.com/live",
            "score": 10,
            "comment_count": 2,
            "submitter_user": "fanf",
            "tags": ["security"],
        }
    ]
    signals = lobsters_fetch.parse_hottest(payload)
    assert len(signals) == 1
    assert signals[0]["author"] == "fanf"
