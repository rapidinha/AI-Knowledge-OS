import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.paths import PipelinePaths


def test_pipeline_paths_layout(tmp_path: Path):
    p = PipelinePaths(radar_root=tmp_path, date="2026-07-12")
    assert p.dir == tmp_path / "_pipeline" / "2026-07-12"
    assert p.signals.name == "signals.jsonl"
    assert p.enriched.name == "enriched.jsonl"
    assert p.clusters.name == "clusters.json"
    assert p.run_meta.name == "run_meta.json"
    assert p.legacy_raw == tmp_path / "_raw" / "2026-07-12.jsonl"
