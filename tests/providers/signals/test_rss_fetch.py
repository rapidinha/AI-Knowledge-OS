import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.rss import fetch as rss_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "rss_feed.xml"


def test_parse_rss_fixture():
    xml = FIXTURE.read_bytes()
    signals = rss_fetch.parse_feed(xml, feed_url="https://example.com/feed.xml")
    assert len(signals) >= 1
    assert signals[0]["provider"] == "rss"
    assert signals[0]["id"].startswith("rss:")
    assert signals[0]["provenance"]["feed_url"] == "https://example.com/feed.xml"


def test_parse_rss20_items():
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example RSS</title>
    <item>
      <guid>post-42</guid>
      <title>RSS Item Title</title>
      <link>https://example.com/rss-item</link>
      <pubDate>Sat, 10 Jul 2026 10:00:00 GMT</pubDate>
      <description>Short summary.</description>
    </item>
  </channel>
</rss>"""
    signals = rss_fetch.parse_feed(xml, feed_url="https://example.com/rss.xml")
    assert len(signals) == 1
    assert signals[0]["id"] == "rss:post-42"
    assert signals[0]["provider"] == "rss"
    assert signals[0]["title"] == "RSS Item Title"


def test_fetch_monkeypatched(monkeypatch):
    xml = FIXTURE.read_bytes()
    monkeypatch.setattr(rss_fetch, "get_feed", lambda url: xml)
    signals = rss_fetch.fetch(feeds=["https://example.com/feed.xml"], limit_per_feed=10)
    assert len(signals) >= 1
    assert signals[0]["provider"] == "rss"
    assert signals[0]["id"].startswith("rss:")
