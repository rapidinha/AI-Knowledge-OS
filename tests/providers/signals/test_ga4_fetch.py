import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.ga4 import fetch as ga4_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "ga4_report.json"


def test_parse_report():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = ga4_fetch.parse_report(payload)
    assert len(signals) == 2
    s = signals[0]
    assert s["provider"] == "ga4"
    assert s["id"].startswith("ga4:")
    assert s["title"] == "GA4 rising page theme: agent skills guide"
    assert s["url"] == "/blog/agent-skills-guide"
    assert s["metrics"]["sessions"] == 128
    assert s["metrics"]["screenPageViews"] == 340
    assert s["provenance"]["page_path"] == "/blog/agent-skills-guide"
    assert signals[1]["title"] == "GA4 rising page theme: context engineering"


def test_fetch_from_export_path():
    signals = ga4_fetch.fetch(export_path=str(FIXTURE), limit=10)
    assert len(signals) == 2
    assert all(s["provider"] == "ga4" for s in signals)


def test_fetch_export_path_respects_limit():
    signals = ga4_fetch.fetch(export_path=str(FIXTURE), limit=1)
    assert len(signals) == 1


def test_fetch_live_api_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    calls: list[tuple[str, str, int]] = []

    def fake_post_run_report(property_id: str, access_token: str, limit: int) -> dict:
        calls.append((property_id, access_token, limit))
        return payload

    monkeypatch.setenv("GA4_ACCESS_TOKEN", "test-token")
    monkeypatch.setattr(ga4_fetch, "post_run_report", fake_post_run_report)
    signals = ga4_fetch.fetch(property_id="123456789", limit=5)
    assert len(calls) == 1
    assert calls[0] == ("123456789", "test-token", 5)
    assert len(signals) == 2
    assert signals[0]["provider"] == "ga4"


def test_fetch_missing_setup_raises(monkeypatch):
    monkeypatch.delenv("GA4_ACCESS_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="export_path"):
        ga4_fetch.fetch()
