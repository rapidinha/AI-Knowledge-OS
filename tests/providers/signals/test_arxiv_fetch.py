import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.arxiv import fetch as arxiv_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "arxiv_atom.xml"


def test_arxiv_fetch_maps_entries(monkeypatch):
    fixture_bytes = FIXTURE.read_bytes()

    def fake_urlopen(req, timeout=30):
        return BytesIO(fixture_bytes)

    monkeypatch.setattr(arxiv_fetch, "urlopen", fake_urlopen)
    signals = arxiv_fetch.fetch(categories=["cs.AI", "cs.SE"], max_results=10)

    assert len(signals) == 2
    assert signals[0]["provider"] == "arxiv"
    assert signals[0]["id"] == "arxiv:2301.00001"
    assert signals[0]["url"] == "http://arxiv.org/abs/2301.00001"
    assert signals[0]["title"] == "Attention Is All You Need Again"
    assert signals[0]["ts"] == "2023-01-01T08:30:00Z"
    assert signals[0]["author"] == "Alice Researcher, Bob Scientist"
    assert signals[0]["text"] is None
    assert signals[0]["metrics"] == {}
    assert signals[0]["provenance"]["arxiv_id"] == "2301.00001"
    assert signals[0]["provenance"]["primary_category"] == "cs.AI"

    assert signals[1]["id"] == "arxiv:2302.00002"
    assert signals[1]["provider"] == "arxiv"
    assert signals[1]["url"] == "http://arxiv.org/abs/2302.00002"
