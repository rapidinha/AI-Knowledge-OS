import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.product_hunt import fetch as product_hunt_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "product_hunt_posts.json"


def test_parse_posts():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = product_hunt_fetch.parse_posts(payload)
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "product_hunt:123"
    assert s["provider"] == "product_hunt"
    assert s["title"] == "Example AI Tool"
    assert s["text"] == "Ship agents faster"
    assert s["url"] == "https://www.producthunt.com/posts/example-ai-tool"
    assert s["ts"] == "2026-07-12T10:00:00Z"
    assert s["metrics"]["votesCount"] == 42
    assert s["provenance"]["product_hunt_id"] == "123"


def test_fetch_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(product_hunt_fetch, "post_graphql", lambda query, token: payload)
    signals = product_hunt_fetch.fetch(token="test-token", limit=10)
    assert len(signals) == 1
    assert signals[0]["id"] == "product_hunt:123"


def test_fetch_missing_token_raises(monkeypatch):
    monkeypatch.delenv("PRODUCTHUNT_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="PRODUCTHUNT_TOKEN"):
        product_hunt_fetch.fetch()
