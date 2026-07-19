# tests/salesmotion/test_using_agents_doc.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = (ROOT / "docs" / "sales" / "using-agents.md").read_text(encoding="utf-8")


def test_using_agents_documents_pipeline_stages():
    assert "salesmotion/pipeline/run_stages.py" in DOC
    for stage in ["ingest", "qualify", "beachheads", "verdict-prep"]:
        assert stage in DOC


def test_using_agents_bans_daemon_and_vendor_sdks():
    assert "daemon" in DOC
    assert "openai" in DOC and "anthropic" in DOC


def test_using_agents_documents_resume_pattern():
    assert "STATE.md" in DOC
    assert "resume" in DOC.lower()
