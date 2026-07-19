import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline import ingest

CONFIG = {
    "channels": {
        "hn": {"enabled": True, "limit": 10},
        "reddit": {"enabled": False},
        "rss": {"enabled": False},
        "x_manual": {"enabled": True},
    }
}


def test_fetch_channels_calls_enabled_hn_and_x_manual(tmp_path: Path, monkeypatch):
    inbox = tmp_path / "x-manual.jsonl"
    inbox.write_text(
        '{"url": "https://x.com/a", "text": "pain post", "ts": "2026-07-18T09:00:00Z"}\n',
        encoding="utf-8",
    )

    def fake_hn_fetch(limit: int = 30):
        assert limit == 10
        return [
            {
                "id": "hn:1",
                "provider": "hn",
                "url": "https://a.test/1",
                "title": "hn story",
                "ts": "2026-07-18T00:00:00Z",
            }
        ]

    monkeypatch.setattr(ingest.hn_fetch, "fetch", fake_hn_fetch)

    signals, counts, degraded = ingest.fetch_channels(CONFIG, inbox_path=inbox)

    assert counts["hn"] == 1
    assert counts["x_manual"] == 1
    assert "reddit" not in counts
    assert "rss" not in counts
    assert degraded == []
    assert {s["provider"] for s in signals} == {"hn", "x_manual"}


def test_fetch_channels_marks_failing_channel_degraded(tmp_path: Path, monkeypatch):
    inbox = tmp_path / "x-manual.jsonl"

    def broken_hn_fetch(limit: int = 30):
        raise RuntimeError("network down")

    monkeypatch.setattr(ingest.hn_fetch, "fetch", broken_hn_fetch)

    signals, counts, degraded = ingest.fetch_channels(CONFIG, inbox_path=inbox)

    assert counts["hn"] == 0
    assert degraded == ["hn"]
    assert signals == []
