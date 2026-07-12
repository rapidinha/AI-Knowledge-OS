from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

# Allow `python providers/signals/pipeline/run_stages.py` from repo root (agent entrypoint).
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from providers.signals.lib.io import load_config
from providers.signals.lib.topics_io import load_topics
from providers.signals.pipeline.artifacts import read_json, read_jsonl, write_json, write_jsonl
from providers.signals.pipeline.correlate import correlate_enriched
from providers.signals.pipeline.enrich import enrich_batch
from providers.signals.pipeline.models import Cluster, RunMeta
from providers.signals.pipeline.paths import PipelinePaths
from providers.signals.pipeline.score import apply_deterministic_scores, personal_tokens_from_signals
from providers.signals.fetch_enabled import fetch_all

STAGES = ("ingest", "enrich", "correlate", "score", "synthesize", "all")


def _defaults(config: dict[str, Any]) -> dict[str, Any]:
    defaults = config.get("defaults") or {}
    return defaults if isinstance(defaults, dict) else {}


def _load_or_init_meta(paths: PipelinePaths) -> RunMeta:
    if paths.run_meta.exists():
        return RunMeta.from_dict(read_json(paths.run_meta))
    return RunMeta(
        date=paths.date,
        schema_version=1,
        providers_ok=[],
        providers_degraded=[],
        counts={},
    )


def _topics_index(radar_root: Path) -> dict[str, Any] | None:
    topics_path = radar_root / "topics.yaml"
    if topics_path.exists():
        return load_topics(topics_path)
    return None


def stage_ingest(config: dict[str, Any], paths: PipelinePaths) -> None:
    signals, counts, degraded = fetch_all(config)
    paths.ensure()
    write_jsonl(paths.signals, signals)
    write_jsonl(paths.legacy_raw, signals)
    providers_ok = sorted(name for name, n in counts.items() if n > 0)
    meta = RunMeta(
        date=paths.date,
        schema_version=1,
        providers_ok=providers_ok,
        providers_degraded=sorted(degraded),
        counts=dict(counts),
    )
    write_json(paths.run_meta, meta.to_dict())


def stage_enrich(config: dict[str, Any], paths: PipelinePaths, radar_root: Path) -> None:
    signals = read_jsonl(paths.signals)
    defaults = _defaults(config)
    max_batch = int(defaults.get("max_signals_per_enrich_batch") or 200)
    cache_path = radar_root / "_pipeline" / "enrich_cache.json"
    enriched, invalid_count = enrich_batch(signals, cache_path=cache_path, max_batch=max_batch)
    write_jsonl(paths.enriched, enriched)
    meta = _load_or_init_meta(paths)
    meta.counts["enriched"] = len(enriched)
    meta.counts["invalid"] = invalid_count
    write_json(paths.run_meta, meta.to_dict())


def stage_correlate(config: dict[str, Any], paths: PipelinePaths, radar_root: Path) -> None:
    enriched = read_jsonl(paths.enriched)
    defaults = _defaults(config)
    max_clusters = int(defaults.get("max_clusters") or 12)
    topics = _topics_index(radar_root)
    clusters = correlate_enriched(enriched, max_clusters=max_clusters, topics_index=topics)
    all_signals = read_jsonl(paths.signals)
    personal = personal_tokens_from_signals(all_signals)
    apply_deterministic_scores(clusters, topics_index=topics, personal_tokens=personal)
    write_json(paths.clusters, {"clusters": [c.to_dict() for c in clusters]})
    meta = _load_or_init_meta(paths)
    meta.counts["clusters"] = len(clusters)
    write_json(paths.run_meta, meta.to_dict())


def stage_score(paths: PipelinePaths, radar_root: Path) -> None:
    data = read_json(paths.clusters)
    clusters = [Cluster.from_dict(c) for c in (data.get("clusters") or [])]
    topics = _topics_index(radar_root)
    all_signals = read_jsonl(paths.signals)
    personal = personal_tokens_from_signals(all_signals)
    apply_deterministic_scores(clusters, topics_index=topics, personal_tokens=personal)
    write_json(paths.clusters, {"clusters": [c.to_dict() for c in clusters]})


def stage_synthesize(paths: PipelinePaths) -> None:
    print(f"clusters: {paths.clusters}")
    print(f"daily template hint: journals/daily/{paths.date}.md (agent-owned synthesis)")


def run_pipeline(
    *,
    config: dict[str, Any],
    paths: PipelinePaths,
    radar_root: Path,
    stage: str,
) -> None:
    if stage == "ingest":
        stage_ingest(config, paths)
    elif stage == "enrich":
        stage_enrich(config, paths, radar_root)
    elif stage == "correlate":
        stage_correlate(config, paths, radar_root)
    elif stage == "score":
        stage_score(paths, radar_root)
    elif stage == "synthesize":
        stage_synthesize(paths)
    elif stage == "all":
        stage_ingest(config, paths)
        stage_enrich(config, paths, radar_root)
        stage_correlate(config, paths, radar_root)
    else:
        raise ValueError(f"unknown stage: {stage}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="run-stages")
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--radar-root", type=Path, required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--stage", choices=STAGES, required=True)
    args = p.parse_args(argv)

    config = load_config(args.config)
    paths = PipelinePaths(radar_root=args.radar_root, date=args.date)
    run_pipeline(config=config, paths=paths, radar_root=args.radar_root, stage=args.stage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
