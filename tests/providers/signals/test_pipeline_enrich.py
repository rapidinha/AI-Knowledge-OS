import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.enrich import enrich_batch


def test_enrich_batch_dedupes_by_canonical_and_caches(tmp_path: Path):
    signals = [
        {
            "id": "a",
            "provider": "hn",
            "url": "https://x.test/p?utm_source=1",
            "title": "Hello World Tools",
            "ts": "2026-07-12T00:00:00Z",
        },
        {
            "id": "b",
            "provider": "lobsters",
            "url": "https://x.test/p",
            "title": "Hello World Tools",
            "ts": "2026-07-12T01:00:00Z",
        },
    ]
    cache = tmp_path / "enrich_cache.json"
    first, invalid_first = enrich_batch(signals, cache_path=cache, max_batch=100)
    assert len(first) == 1
    assert invalid_first == 0
    assert first[0]["enrich_meta"]["cache_hit"] is False
    second, invalid_second = enrich_batch(first, cache_path=cache, max_batch=100)
    assert invalid_second == 0
    assert second[0]["enrich_meta"]["cache_hit"] is True
