from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

# Allow `python salesmotion/pipeline/run_stages.py` from repo root (agent entrypoint).
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from providers.signals.lib.io import load_config
from providers.signals.pipeline.artifacts import read_json, read_jsonl, write_json, write_jsonl

from salesmotion.pipeline.beachheads import build_beachheads
from salesmotion.pipeline.ingest import fetch_channels
from salesmotion.pipeline.paths import SalesPipelinePaths
from salesmotion.pipeline.qualify import qualify_batch
from salesmotion.pipeline.verdict import evaluate_beachhead

STAGES = ("ingest", "qualify", "beachheads", "verdict-prep", "all")


def _load_or_init_meta(paths: SalesPipelinePaths) -> dict[str, Any]:
    if paths.run_meta.exists():
        return read_json(paths.run_meta)
    return {"date": paths.date, "providers_ok": [], "providers_degraded": [], "counts": {}}


def stage_ingest(config: dict[str, Any], paths: SalesPipelinePaths) -> None:
    paths.ensure()
    signals, counts, degraded = fetch_channels(config, inbox_path=paths.inbox_x_manual)
    write_jsonl(paths.signals, signals)
    meta = {
        "date": paths.date,
        "providers_ok": sorted(name for name, n in counts.items() if n > 0),
        "providers_degraded": sorted(degraded),
        "counts": dict(counts),
    }
    write_json(paths.run_meta, meta)


def stage_qualify(config: dict[str, Any], paths: SalesPipelinePaths) -> None:
    signals = read_jsonl(paths.signals)
    pain_lexicon = config.get("pain_lexicon") or {}
    qualified = qualify_batch(signals, pain_lexicon=pain_lexicon)
    write_jsonl(paths.qualified, qualified)
    meta = _load_or_init_meta(paths)
    meta["counts"]["qualified"] = len(qualified)
    write_json(paths.run_meta, meta)


def stage_beachheads(config: dict[str, Any], paths: SalesPipelinePaths) -> None:
    qualified = read_jsonl(paths.qualified)
    defaults = config.get("defaults") or {}
    max_beachheads = int(defaults.get("max_beachheads") or 12)
    clusters = build_beachheads(qualified, max_beachheads=max_beachheads)
    write_json(paths.beachheads, {"beachheads": [c.to_dict() for c in clusters]})
    meta = _load_or_init_meta(paths)
    meta["counts"]["beachheads"] = len(clusters)
    write_json(paths.run_meta, meta)


def stage_verdict_prep(config: dict[str, Any], paths: SalesPipelinePaths) -> None:
    data = read_json(paths.beachheads)
    thresholds = config.get("verdict") or {}
    out = []
    for b in data.get("beachheads") or []:
        evaluation = evaluate_beachhead(b.get("scores") or {}, thresholds=thresholds)
        out.append(
            {
                "beachhead_slug": b.get("slug") or b.get("cluster_id"),
                "title": b.get("title"),
                **evaluation,
            }
        )
    write_json(paths.dir / "verdict_prep.json", {"beachheads": out})


def run_pipeline(*, config: dict[str, Any], paths: SalesPipelinePaths, stage: str) -> None:
    if stage == "ingest":
        stage_ingest(config, paths)
    elif stage == "qualify":
        stage_qualify(config, paths)
    elif stage == "beachheads":
        stage_beachheads(config, paths)
    elif stage == "verdict-prep":
        stage_verdict_prep(config, paths)
    elif stage == "all":
        stage_ingest(config, paths)
        stage_qualify(config, paths)
        stage_beachheads(config, paths)
        stage_verdict_prep(config, paths)
    else:
        raise ValueError(f"unknown stage: {stage}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sales-run-stages")
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--sales-root", type=Path, required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--stage", choices=STAGES, required=True)
    args = p.parse_args(argv)

    config = load_config(args.config)
    paths = SalesPipelinePaths(sales_root=args.sales_root, date=args.date)
    run_pipeline(config=config, paths=paths, stage=args.stage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
