import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.pipeline.paths import SalesPipelinePaths


def test_pipeline_paths_layout(tmp_path: Path):
    p = SalesPipelinePaths(sales_root=tmp_path, date="2026-07-18")
    assert p.dir == tmp_path / "_pipeline" / "2026-07-18"
    assert p.signals.name == "signals.jsonl"
    assert p.qualified.name == "qualified.jsonl"
    assert p.beachheads.name == "beachheads.json"
    assert p.run_meta.name == "run_meta.json"
    assert p.verdict.name == "verdict.md"
    assert p.inbox_x_manual == tmp_path / "inbox" / "x-manual.jsonl"


def test_ensure_creates_directories(tmp_path: Path):
    p = SalesPipelinePaths(sales_root=tmp_path, date="2026-07-18")
    p.ensure()
    assert p.dir.exists()
    assert p.inbox_x_manual.parent.exists()
