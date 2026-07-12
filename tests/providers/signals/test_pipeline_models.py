import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.models import (
    Cluster,
    RunMeta,
    enrich_signal,
    validate_signal,
)


BASE = {
    "id": "hn:1",
    "provider": "hn",
    "url": "https://example.com/a?utm_source=x",
    "title": "  Agent Skills Packaging  ",
    "ts": "2026-07-12T12:00:00Z",
}


def test_validate_signal_ok():
    s = validate_signal(BASE)
    assert s["id"] == "hn:1"


def test_validate_signal_rejects_missing_title():
    bad = {**BASE}
    del bad["title"]
    try:
        validate_signal(bad)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "title" in str(e)


def test_enrich_signal_adds_canonical_and_norm_title():
    e = enrich_signal(BASE)
    assert e["canonical_url"].startswith("https://example.com/a")
    assert "utm_source" not in e["canonical_url"]
    assert e["norm_title"] == "agent skills packaging"
    assert e["enrich_meta"]["version"] == 1


def test_cluster_and_run_meta_roundtrip():
    c = Cluster(
        cluster_id="cl_001",
        title="Agent skills",
        signal_ids=["hn:1"],
        providers=["hn"],
        scores={"signal_consensus": 1},
        weak_signal=True,
    )
    d = c.to_dict()
    assert Cluster.from_dict(d).cluster_id == "cl_001"
    meta = RunMeta(
        date="2026-07-12",
        schema_version=1,
        providers_ok=["hn"],
        providers_degraded=[],
        counts={"signals": 1, "enriched": 1, "clusters": 1, "invalid": 0},
    )
    assert RunMeta.from_dict(meta.to_dict()).date == "2026-07-12"
