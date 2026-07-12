# tests/radar/test_provider_setup.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.provider_setup import check_provider_ready


def test_product_hunt_requires_token(monkeypatch):
    monkeypatch.delenv("PRODUCTHUNT_TOKEN", raising=False)
    ok, hint = check_provider_ready("product_hunt", {"enabled": True})
    assert ok is False
    assert "PRODUCTHUNT_TOKEN" in hint


def test_rss_ready_with_feeds():
    ok, hint = check_provider_ready("rss", {"enabled": True, "feeds": ["https://example.com/feed.xml"]})
    assert ok is True
    assert hint == ""


def test_youtube_api_requires_key(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    ok, hint = check_provider_ready("youtube_api", {"enabled": True, "queries": ["ai agents"]})
    assert ok is False
    assert "YOUTUBE_API_KEY" in hint


def test_ga4_ready_with_export_path_only(monkeypatch):
    monkeypatch.delenv("GA4_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    ok, hint = check_provider_ready("ga4", {"enabled": True, "export_path": "/tmp/ga4.json"})
    assert ok is True
    assert hint == ""


def test_ga4_requires_property_without_export(monkeypatch):
    monkeypatch.delenv("GA4_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    ok, hint = check_provider_ready("ga4", {"enabled": True})
    assert ok is False
    assert "property" in hint.lower() or "token" in hint.lower()


def test_gsc_ready_with_export_path_only(monkeypatch):
    monkeypatch.delenv("GSC_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    ok, hint = check_provider_ready(
        "search_console", {"enabled": True, "export_path": "/tmp/gsc.json"}
    )
    assert ok is True
    assert hint == ""
