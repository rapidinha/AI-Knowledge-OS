from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.lib.io import load_config, enabled_providers


def test_enabled_providers_respects_flags(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: true
  arxiv:
    enabled: false
    categories: ["cs.AI"]
  github_trending:
    enabled: true
  reddit:
    enabled: false
""",
        encoding="utf-8",
    )
    data = load_config(cfg)
    assert enabled_providers(data) == ["github_trending", "hn"]
