import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.hn import fetch as hn_fetch


def test_hn_fetch_maps_items(monkeypatch):
    top = [1, 2]
    items = {
        1: {"id": 1, "title": "A", "url": "https://a.test", "by": "alice", "score": 10, "time": 1700000000, "type": "story"},
        2: {"id": 2, "title": "B", "url": "https://b.test", "by": "bob", "score": 3, "time": 1700000100, "type": "story"},
    }

    def fake_get_json(url: str):
        if url.endswith("topstories.json"):
            return top
        if "/item/1.json" in url:
            return items[1]
        if "/item/2.json" in url:
            return items[2]
        raise AssertionError(url)

    monkeypatch.setattr(hn_fetch, "get_json", fake_get_json)
    signals = hn_fetch.fetch(limit=2)
    assert len(signals) == 2
    assert signals[0]["provider"] == "hn"
    assert signals[0]["id"] == "hn:1"
    assert signals[0]["url"] == "https://a.test"
