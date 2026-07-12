import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.search_console import fetch as gsc_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "gsc_query.json"


def test_parse_query():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = gsc_fetch.parse_query(payload)
    assert len(signals) == 2
    s = signals[0]
    assert s["provider"] == "search_console"
    assert s["id"].startswith("search_console:")
    assert s["title"] == "GSC rising query: context engineering patterns"
    assert s["metrics"]["clicks"] == 45
    assert s["metrics"]["impressions"] == 890
    assert s["provenance"]["query"] == "context engineering patterns"
    assert signals[1]["title"] == "GSC rising query: agent skills packaging"


def test_fetch_from_export_path():
    signals = gsc_fetch.fetch(export_path=str(FIXTURE), limit=10)
    assert len(signals) == 2
    assert all(s["provider"] == "search_console" for s in signals)


def test_fetch_export_path_respects_limit():
    signals = gsc_fetch.fetch(export_path=str(FIXTURE), limit=1)
    assert len(signals) == 1


def test_fetch_live_api_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    calls: list[tuple[str, str, int]] = []

    def fake_get_search_analytics(site_url: str, access_token: str, limit: int) -> dict:
        calls.append((site_url, access_token, limit))
        return payload

    monkeypatch.setenv("GSC_ACCESS_TOKEN", "test-token")
    monkeypatch.setattr(gsc_fetch, "get_search_analytics", fake_get_search_analytics)
    signals = gsc_fetch.fetch(site_url="https://example.com/", limit=5)
    assert len(calls) == 1
    assert calls[0] == ("https://example.com/", "test-token", 5)
    assert len(signals) == 2
    assert signals[0]["provider"] == "search_console"


def test_fetch_missing_setup_raises(monkeypatch):
    monkeypatch.delenv("GSC_ACCESS_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="export_path"):
        gsc_fetch.fetch()
