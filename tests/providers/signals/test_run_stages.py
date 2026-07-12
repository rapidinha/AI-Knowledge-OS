import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.paths import PipelinePaths
from providers.signals.pipeline import run_stages

SAMPLE_SIGNALS = [
    {
        "id": "hn:1",
        "provider": "hn",
        "url": "https://a.test/1",
        "title": "Agent skills pack",
        "ts": "2026-07-12T00:00:00Z",
    },
    {
        "id": "lobsters:2",
        "provider": "lobsters",
        "url": "https://b.test/2",
        "title": "Skills for agents",
        "ts": "2026-07-12T01:00:00Z",
    },
]


def _write_config(radar_root: Path) -> Path:
    config_path = radar_root / "config.yaml"
    config_path.write_text(
        """
defaults:
  max_signals_per_enrich_batch: 200
  max_clusters: 12
providers:
  hn:
    enabled: true
  lobsters:
    enabled: true
""",
        encoding="utf-8",
    )
    return config_path


def _base_args(radar_root: Path, config_path: Path, stage: str) -> list[str]:
    return [
        "--config",
        str(config_path),
        "--radar-root",
        str(radar_root),
        "--date",
        "2026-07-12",
        "--stage",
        stage,
    ]


def test_stage_ingest_writes_artifacts(tmp_path: Path, monkeypatch):
    radar_root = tmp_path / "radar"
    radar_root.mkdir()
    config_path = _write_config(radar_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_all",
        lambda _config: (list(SAMPLE_SIGNALS), {"hn": 1, "lobsters": 1}, []),
    )

    assert run_stages.main(_base_args(radar_root, config_path, "ingest")) == 0

    paths = PipelinePaths(radar_root=radar_root, date="2026-07-12")
    assert paths.signals.exists()
    assert paths.legacy_raw.exists()
    assert paths.run_meta.exists()

    signals = paths.signals.read_text(encoding="utf-8")
    assert "hn:1" in signals
    assert paths.legacy_raw.read_text(encoding="utf-8") == signals

    meta = json.loads(paths.run_meta.read_text(encoding="utf-8"))
    assert set(meta["providers_ok"]) == {"hn", "lobsters"}
    assert meta["providers_degraded"] == []
    assert meta["counts"]["hn"] == 1
    assert meta["counts"]["lobsters"] == 1


def test_stage_enrich_after_ingest(tmp_path: Path, monkeypatch):
    radar_root = tmp_path / "radar"
    radar_root.mkdir()
    config_path = _write_config(radar_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_all",
        lambda _config: (list(SAMPLE_SIGNALS), {"hn": 1, "lobsters": 1}, []),
    )
    base = _base_args(radar_root, config_path, "ingest")
    assert run_stages.main(base) == 0
    assert run_stages.main(_base_args(radar_root, config_path, "enrich")) == 0

    paths = PipelinePaths(radar_root=radar_root, date="2026-07-12")
    assert paths.enriched.exists()
    lines = paths.enriched.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    meta = json.loads(paths.run_meta.read_text(encoding="utf-8"))
    assert meta["counts"]["enriched"] == 2


def test_stage_correlate_writes_scored_clusters(tmp_path: Path, monkeypatch):
    radar_root = tmp_path / "radar"
    radar_root.mkdir()
    config_path = _write_config(radar_root)

    monkeypatch.setattr(
        run_stages,
        "fetch_all",
        lambda _config: (list(SAMPLE_SIGNALS), {"hn": 1, "lobsters": 1}, []),
    )
    for stage in ("ingest", "enrich", "correlate"):
        assert run_stages.main(_base_args(radar_root, config_path, stage)) == 0

    paths = PipelinePaths(radar_root=radar_root, date="2026-07-12")
    assert paths.clusters.exists()
    data = json.loads(paths.clusters.read_text(encoding="utf-8"))
    clusters = data["clusters"]
    assert clusters
    assert all("scores" in c for c in clusters)
    assert any(c["scores"].get("signal_consensus", 0) >= 1 for c in clusters)
