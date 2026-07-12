import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.youtube_api import fetch as youtube_api_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "youtube_api_search.json"


def test_parse_search():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = youtube_api_fetch.parse_search(payload)
    assert len(signals) == 2
    s = signals[0]
    assert s["id"] == "youtube_api:dQw4w9WgXcQ"
    assert s["provider"] == "youtube_api"
    assert s["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert s["title"] == "Building AI Agents in Production"
    assert s["ts"] == "2026-07-10T12:00:00Z"
    assert s["author"] == "Example Channel"
    assert s["text"] == "A short overview of agent patterns for shipping."
    assert s["metrics"] == {}
    assert s["provenance"] == {
        "video_id": "dQw4w9WgXcQ",
        "channel_title": "Example Channel",
    }
    assert signals[1]["text"] is None
    assert signals[1]["provenance"]["video_id"] == "abc123xyz"


def test_fetch_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    calls: list[str] = []

    def fake_get_json(url: str) -> dict:
        calls.append(url)
        return payload

    monkeypatch.setattr(youtube_api_fetch, "get_json", fake_get_json)
    signals = youtube_api_fetch.fetch(
        api_key="test-key",
        queries=["ai agents", "context engineering"],
        max_results=5,
    )
    assert len(calls) == 2
    assert "q=ai+agents" in calls[0] or "q=ai%20agents" in calls[0]
    assert "key=test-key" in calls[0]
    assert len(signals) == 2
    assert signals[0]["provider"] == "youtube_api"


def test_fetch_dedupes_across_queries(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def fake_get_json(url: str) -> dict:
        return payload

    monkeypatch.setattr(youtube_api_fetch, "get_json", fake_get_json)
    signals = youtube_api_fetch.fetch(
        api_key="test-key",
        queries=["query-a", "query-b"],
        max_results=5,
    )
    assert len(signals) == 2
    ids = {s["provenance"]["video_id"] for s in signals}
    assert len(ids) == 2


def test_fetch_channel_ids(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    calls: list[str] = []

    def fake_get_json(url: str) -> dict:
        calls.append(url)
        return payload

    monkeypatch.setattr(youtube_api_fetch, "get_json", fake_get_json)
    signals = youtube_api_fetch.fetch(
        api_key="test-key",
        channel_ids=["UCxxxx"],
        max_results=3,
    )
    assert len(calls) == 1
    assert "channelId=UCxxxx" in calls[0]
    assert len(signals) == 2


def test_fetch_missing_key_raises(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="YOUTUBE_API_KEY"):
        youtube_api_fetch.fetch(queries=["ai agents"])
