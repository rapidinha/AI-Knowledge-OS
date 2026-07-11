import json
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.reddit import fetch as reddit_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "reddit_hot.json"


def test_reddit_fetch_maps_posts(monkeypatch):
    fixture_bytes = FIXTURE.read_bytes()

    def fake_urlopen(req, timeout=30):
        return BytesIO(fixture_bytes)

    monkeypatch.setattr(reddit_fetch, "urlopen", fake_urlopen)
    signals = reddit_fetch.fetch(subs=["programming"], user_agent="test-agent/1.0", limit=2)

    assert len(signals) == 2
    assert signals[0]["provider"] == "reddit"
    assert signals[0]["id"] == "reddit:t3_abc123"
    assert signals[0]["url"] == "https://example.com/article"
    assert signals[0]["title"] == "A useful thread"
    assert signals[0]["author"] == "alice"
    assert signals[0]["metrics"]["score"] == 42
    assert signals[0]["provenance"]["permalink"] == (
        "https://www.reddit.com/r/programming/comments/abc123/a_useful_thread/"
    )
    assert signals[0]["provenance"]["subreddit"] == "programming"

    assert signals[1]["id"] == "reddit:t3_def456"
    assert signals[1]["provenance"]["subreddit"] == "MachineLearning"


def test_reddit_fetch_sends_user_agent(monkeypatch):
    fixture_bytes = FIXTURE.read_bytes()
    seen_headers: list[str] = []

    def fake_urlopen(req, timeout=30):
        seen_headers.append(req.headers.get("User-agent") or req.headers.get("User-Agent"))
        return BytesIO(fixture_bytes)

    monkeypatch.setattr(reddit_fetch, "urlopen", fake_urlopen)
    reddit_fetch.fetch(subs=["programming"], user_agent="custom-ua/2.0", limit=1)

    assert seen_headers == ["custom-ua/2.0"]
