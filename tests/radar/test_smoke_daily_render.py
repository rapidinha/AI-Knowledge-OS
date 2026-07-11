from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = (ROOT / "templates" / "radar" / "daily.md").read_text(encoding="utf-8")


def test_daily_template_has_core_sections():
    for heading in ["## Executive Summary", "## Top Opportunities", "## Highest ROI", "## Worth Watching", "## Ignore", "## Signals"]:
        assert heading in TEMPLATE


def test_daily_template_has_recurrence_and_topic_link():
    assert "**Recurrence:**" in TEMPLATE
    assert "journals/radar/topics/" in TEMPLATE
    assert "## Topics" in TEMPLATE
