from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = (ROOT / "agents" / "sales-motion" / "SKILL.md").read_text(encoding="utf-8")
CURSOR_COPY = (ROOT / ".cursor" / "skills" / "sales-motion" / "SKILL.md").read_text(encoding="utf-8")
CLAUDE_COPY = (ROOT / ".claude" / "skills" / "sales-motion" / "SKILL.md").read_text(encoding="utf-8")


def test_skill_documents_pipeline_entrypoint():
    assert "salesmotion/pipeline/run_stages.py" in SKILL
    assert "_pipeline/" in SKILL


def test_skill_documents_hard_gate_before_content():
    assert "decisions.yaml" in SKILL
    assert "cannot run without an explicit" in SKILL


def test_skill_bans_auto_send_and_vendor_sdks():
    assert "auto-send" in SKILL
    assert "openai" in SKILL and "anthropic" in SKILL


def test_skill_copies_are_identical_to_canonical():
    assert CURSOR_COPY == SKILL
    assert CLAUDE_COPY == SKILL
