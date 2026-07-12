import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.correlate import correlate_enriched


def test_correlate_groups_shared_topic_hint():
    enriched = [
        {
            "id": "hn:1",
            "provider": "hn",
            "url": "https://a.test/1",
            "title": "Agent skills pack",
            "ts": "2026-07-12T00:00:00Z",
            "canonical_url": "https://a.test/1",
            "norm_title": "agent skills pack",
            "topics_hint": ["agent", "skills"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
        {
            "id": "lobsters:2",
            "provider": "lobsters",
            "url": "https://b.test/2",
            "title": "Skills for agents",
            "ts": "2026-07-12T01:00:00Z",
            "canonical_url": "https://b.test/2",
            "norm_title": "skills for agents",
            "topics_hint": ["skills", "agents"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
        {
            "id": "arxiv:3",
            "provider": "arxiv",
            "url": "https://c.test/3",
            "title": "Unrelated database paper",
            "ts": "2026-07-12T02:00:00Z",
            "canonical_url": "https://c.test/3",
            "norm_title": "unrelated database paper",
            "topics_hint": ["database"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
    ]
    clusters = correlate_enriched(enriched, max_clusters=7, topics_index=None)
    assert 1 <= len(clusters) <= 7
    multi = [c for c in clusters if len(c.providers) >= 2]
    assert multi, "expected at least one multi-provider cluster from overlapping hints"
