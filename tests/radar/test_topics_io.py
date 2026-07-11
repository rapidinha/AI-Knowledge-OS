import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.lib import topics_io


def test_round_trip_topics_yaml(tmp_path: Path):
    path = tmp_path / "topics.yaml"
    data = {
        "version": 1,
        "updated_at": "2026-07-11T12:00:00Z",
        "topics": [
            {
                "slug": "agent-skills",
                "title": "Agent skills packaging",
                "aliases": ["claude skills"],
                "first_seen": "2026-07-11",
                "last_seen": "2026-07-11",
                "hit_count": 1,
                "provider_set": ["hn", "lobsters"],
                "recent_urls": ["https://example.com/a"],
                "status": "emerging",
            }
        ],
    }
    topics_io.save_topics(path, data)
    loaded = topics_io.load_topics(path)
    assert loaded["version"] == 1
    assert loaded["topics"][0]["slug"] == "agent-skills"
    assert loaded["topics"][0]["provider_set"] == ["hn", "lobsters"]


def test_load_missing_returns_empty_graph(tmp_path: Path):
    path = tmp_path / "missing.yaml"
    loaded = topics_io.load_topics(path)
    assert loaded["version"] == 1
    assert loaded["topics"] == []
