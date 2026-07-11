from pathlib import Path


def test_daily_template_has_required_sections():
    text = Path("templates/radar/daily.md").read_text(encoding="utf-8")
    for heading in ["Executive Summary", "Top Opportunities", "Highest ROI", "Worth Watching", "Ignore", "Signals"]:
        assert heading in text
