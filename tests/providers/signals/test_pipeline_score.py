import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from providers.signals.pipeline.models import Cluster
from providers.signals.pipeline.score import apply_deterministic_scores


def test_signal_consensus_and_personal_boost():
    c = Cluster(
        cluster_id="cl_001",
        title="Agent skills",
        signal_ids=["hn:1", "lobsters:2"],
        providers=["hn", "lobsters"],
        scores={},
    )
    topics = {
        "topics": [
            {
                "slug": "agent-skills",
                "aliases": ["agent skills"],
                "hit_count": 3,
                "provider_set": ["hn", "lobsters"],
            }
        ]
    }
    personal = {"agent", "skills"}
    out = apply_deterministic_scores([c], topics_index=topics, personal_tokens=personal)
    assert out[0].scores["signal_consensus"] >= 2
    assert out[0].scores.get("personal_relevance", 0) >= 1
