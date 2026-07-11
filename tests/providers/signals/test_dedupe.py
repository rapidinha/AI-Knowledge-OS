import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.lib.dedupe import canonicalize_url, dedupe_signals


def test_canonicalize_strips_tracking():
    u = "https://Example.com/a?utm_source=x&id=1"
    assert canonicalize_url(u) == "https://example.com/a?id=1"


def test_dedupe_keeps_first_by_url():
    signals = [
        {"id": "1", "provider": "hn", "url": "https://a.com/x", "title": "Hello", "ts": "2026-07-11T00:00:00Z"},
        {"id": "2", "provider": "reddit", "url": "https://a.com/x/", "title": "Hello!", "ts": "2026-07-11T01:00:00Z"},
    ]
    out = dedupe_signals(signals)
    assert len(out) == 1
    assert out[0]["id"] == "1"
