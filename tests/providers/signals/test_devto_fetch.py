import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.devto import fetch as devto_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "devto_articles.json"


def test_parse_articles():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = devto_fetch.parse_articles(payload)
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "devto:999001"
    assert s["provider"] == "devto"
    assert "agent skills" in s["title"].lower()
    assert s["metrics"]["public_reactions_count"] == 12


def test_fetch_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(devto_fetch, "get_json", lambda url: payload)
    assert len(devto_fetch.fetch(tag="ai", limit=10)) == 1
