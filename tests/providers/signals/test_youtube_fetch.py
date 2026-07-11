import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.youtube import fetch as youtube_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "youtube_atom.xml"


def test_parse_atom():
    xml = FIXTURE.read_text(encoding="utf-8")
    signals = youtube_fetch.parse_atom(xml, channel_label="Example Eng")
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "youtube:VIDEO123"
    assert s["provider"] == "youtube"
    assert s["url"].endswith("VIDEO123")
    assert s["author"] == "Example Eng"


def test_fetch_channels_monkeypatched(monkeypatch):
    xml = FIXTURE.read_text(encoding="utf-8")
    monkeypatch.setattr(youtube_fetch, "get_feed", lambda url: xml)
    signals = youtube_fetch.fetch(
        channels=[{"id": "UCxxxx", "label": "Example Eng"}],
        max_videos_per_channel=5,
    )
    assert len(signals) == 1


def test_invalid_channel_skipped(monkeypatch):
    def boom(url: str) -> str:
        raise OSError("fail")

    monkeypatch.setattr(youtube_fetch, "get_feed", boom)
    signals = youtube_fetch.fetch(channels=[{"id": "bad", "label": "x"}], max_videos_per_channel=5)
    assert signals == []
