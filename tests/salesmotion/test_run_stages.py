import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline import run_stages
from salesmotion.pipeline.paths import SalesPipelinePaths

SAMPLE_SIGNALS = [
    {
        "id": "hn:1",
        "provider": "hn",
        "url": "https://a.test/1",
        "title": "I hate doing this manually every week",
        "ts": "2026-07-18T00:00:00Z",
        "text": None,
    },
    {
        "id": "reddit:2",
        "provider": "reddit",
        "url": "https://b.test/2",
        "title": "manually doing this too, hate it so much",
        "ts": "2026-07-18T01:00:00Z",
        "text": None,
    },
]


def _write_config(sales_root: Path) -> Path:
    config_path = sales_root / "config.yaml"
    config_path.write_text(
        """
pain_lexicon:
  intensity_terms: ["hate"]
  workaround_terms: ["manually"]
  willingness_to_pay_terms: []
defaults:
  max_beachheads: 12
verdict:
  go_threshold: 40
  watch_threshold: 20
  min_signals_for_go: 2
  min_sources_for_go: 2
""",
        encoding="utf-8",
    )
    return config_path


def _base_args(sales_root: Path, config_path: Path, stage: str) -> list[str]:
    return [
        "--config", str(config_path),
        "--sales-root", str(sales_root),
        "--date", "2026-07-18",
        "--stage", stage,
    ]


def test_stage_ingest_writes_artifacts(tmp_path: Path, monkeypatch):
    sales_root = tmp_path / "sales"
    sales_root.mkdir()
    config_path = _write_config(sales_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_channels",
        lambda _config, inbox_path: (list(SAMPLE_SIGNALS), {"hn": 1, "reddit": 1}, []),
    )

    assert run_stages.main(_base_args(sales_root, config_path, "ingest")) == 0

    paths = SalesPipelinePaths(sales_root=sales_root, date="2026-07-18")
    assert paths.signals.exists()
    assert paths.run_meta.exists()
    meta = json.loads(paths.run_meta.read_text(encoding="utf-8"))
    assert set(meta["providers_ok"]) == {"hn", "reddit"}
    assert meta["providers_degraded"] == []


def test_full_pipeline_ingest_to_verdict_prep(tmp_path: Path, monkeypatch):
    sales_root = tmp_path / "sales"
    sales_root.mkdir()
    config_path = _write_config(sales_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_channels",
        lambda _config, inbox_path: (list(SAMPLE_SIGNALS), {"hn": 1, "reddit": 1}, []),
    )

    for stage in ("ingest", "qualify", "beachheads", "verdict-prep"):
        assert run_stages.main(_base_args(sales_root, config_path, stage)) == 0

    paths = SalesPipelinePaths(sales_root=sales_root, date="2026-07-18")
    assert paths.qualified.exists()
    assert paths.beachheads.exists()

    verdict_prep_path = paths.dir / "verdict_prep.json"
    assert verdict_prep_path.exists()
    data = json.loads(verdict_prep_path.read_text(encoding="utf-8"))
    assert data["beachheads"]
    b = data["beachheads"][0]
    assert b["recommendation"] in {"go_eligible", "watch", "no_go"}
    assert b["thresholds_used"]["go_threshold"] == 40


def test_stage_all_runs_every_stage(tmp_path: Path, monkeypatch):
    sales_root = tmp_path / "sales"
    sales_root.mkdir()
    config_path = _write_config(sales_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_channels",
        lambda _config, inbox_path: (list(SAMPLE_SIGNALS), {"hn": 1, "reddit": 1}, []),
    )

    assert run_stages.main(_base_args(sales_root, config_path, "all")) == 0

    paths = SalesPipelinePaths(sales_root=sales_root, date="2026-07-18")
    assert paths.signals.exists()
    assert paths.qualified.exists()
    assert paths.beachheads.exists()
    assert (paths.dir / "verdict_prep.json").exists()
