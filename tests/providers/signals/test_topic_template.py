from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOPIC = (ROOT / "templates" / "radar" / "topic.md").read_text(encoding="utf-8")
INDEX = (ROOT / "templates" / "radar" / "topics-index.md").read_text(encoding="utf-8")


def test_topic_template_has_summary_surface():
    assert "radar_topic: true" in TOPIC
    assert "## Rolling summary" in TOPIC
    assert "## Timeline" in TOPIC
    assert "## Sources" in TOPIC


def test_topics_index_template():
    assert "radar_topics_index: true" in INDEX
    assert "## Active topics" in INDEX
