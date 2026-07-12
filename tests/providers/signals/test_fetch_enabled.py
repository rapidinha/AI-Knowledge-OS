import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals import fetch_enabled
from providers.signals.sources.arxiv import fetch as arxiv_fetch
from providers.signals.sources.devto import fetch as devto_fetch
from providers.signals.sources.github_trending import fetch as github_trending_fetch
from providers.signals.sources.hn import fetch as hn_fetch
from providers.signals.sources.lobsters import fetch as lobsters_fetch
from providers.signals.sources.product_hunt import fetch as product_hunt_fetch
from providers.signals.sources.reddit import fetch as reddit_fetch
from providers.signals.sources.rss import fetch as rss_fetch
from providers.signals.sources.youtube import fetch as youtube_fetch


HN_SIGNAL = {
    "id": "hn:1",
    "provider": "hn",
    "url": "https://a.test",
    "title": "A",
    "ts": "2026-07-11T00:00:00+00:00",
    "author": "alice",
    "text": None,
    "metrics": {"score": 10},
    "provenance": {"hn_id": 1},
}


def test_fetch_enabled_writes_only_enabled_providers(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: true
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
""",
        encoding="utf-8",
    )
    out = tmp_path / "raw" / "2026-07-11.jsonl"

    monkeypatch.setattr(hn_fetch, "fetch", lambda limit=30: [HN_SIGNAL])
    monkeypatch.setattr(arxiv_fetch, "fetch", lambda **kwargs: (_ for _ in ()).throw(AssertionError("arxiv")))
    monkeypatch.setattr(
        github_trending_fetch,
        "fetch",
        lambda since="daily": (_ for _ in ()).throw(AssertionError("github_trending")),
    )
    monkeypatch.setattr(
        reddit_fetch,
        "fetch",
        lambda subs, user_agent, limit=25: (_ for _ in ()).throw(AssertionError("reddit")),
    )

    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0

    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    signal = json.loads(lines[0])
    assert signal["provider"] == "hn"
    assert signal["id"] == "hn:1"


def test_fetch_enabled_includes_lobsters(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: false
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  lobsters:
    enabled: true
  devto:
    enabled: false
  youtube:
    enabled: false
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(
        lobsters_fetch,
        "fetch",
        lambda tag="", limit=30: [
            {
                "id": "lobsters:1",
                "provider": "lobsters",
                "url": "https://x.test",
                "title": "T",
                "ts": "2026-07-11T00:00:00Z",
            }
        ],
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    assert "lobsters:1" in out.read_text(encoding="utf-8")


def test_provider_error_degrades(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: true
  lobsters:
    enabled: true
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  devto:
    enabled: false
  youtube:
    enabled: false
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(hn_fetch, "fetch", lambda limit=30: [HN_SIGNAL])
    monkeypatch.setattr(
        lobsters_fetch,
        "fetch",
        lambda tag="", limit=30: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "hn:1" in text
    assert "lobsters:" not in text


def test_fetch_enabled_rss_with_feeds(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: false
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  lobsters:
    enabled: false
  devto:
    enabled: false
  youtube:
    enabled: false
  rss:
    enabled: true
    feeds:
      - https://example.com/feed.xml
    limit_per_feed: 5
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(
        rss_fetch,
        "fetch",
        lambda feeds, limit_per_feed=10: [
            {
                "id": "rss:1",
                "provider": "rss",
                "url": "https://example.com/post",
                "title": "RSS Post",
                "ts": "2026-07-11T00:00:00Z",
            }
        ],
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    assert "rss:1" in out.read_text(encoding="utf-8")


def test_product_hunt_degrades_without_token(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.delenv("PRODUCTHUNT_TOKEN", raising=False)
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: false
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  lobsters:
    enabled: false
  devto:
    enabled: false
  youtube:
    enabled: false
  product_hunt:
    enabled: true
    limit: 20
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(
        product_hunt_fetch,
        "fetch",
        lambda limit=20: (_ for _ in ()).throw(AssertionError("should not fetch")),
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    assert "product_hunt:" not in out.read_text(encoding="utf-8")
    captured = capsys.readouterr()
    assert "product_hunt: degraded (setup:" in captured.err
    assert "PRODUCTHUNT_TOKEN" in captured.err
