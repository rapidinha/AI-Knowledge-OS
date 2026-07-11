import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.sources.github_trending import fetch as github_trending_fetch

FIXTURE = ROOT / "providers" / "signals" / "fixtures" / "github_trending.html"


def test_github_trending_fetch_maps_repos(monkeypatch):
    fixture_bytes = FIXTURE.read_bytes()

    def fake_urlopen(req, timeout=30):
        return BytesIO(fixture_bytes)

    monkeypatch.setattr(github_trending_fetch, "urlopen", fake_urlopen)
    signals = github_trending_fetch.fetch(since="daily")

    assert len(signals) >= 1
    assert signals[0]["provider"] == "github_trending"
    assert signals[0]["id"] == "github_trending:torvalds/linux"
    assert signals[0]["url"] == "https://github.com/torvalds/linux"
    assert signals[0]["title"] == "torvalds / linux"
    assert signals[0]["text"] == "Linux kernel source tree"
    assert signals[0]["author"] == "torvalds"
    assert signals[0]["provenance"]["since"] == "daily"
    assert signals[0]["provenance"]["repo"] == "torvalds/linux"
