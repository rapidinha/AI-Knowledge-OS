# tests/salesmotion/test_templates.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates" / "sales"

CONFIG = (TEMPLATES / "config.example.yaml").read_text(encoding="utf-8")
DECISIONS = (TEMPLATES / "decisions.example.yaml").read_text(encoding="utf-8")
VERDICT = (TEMPLATES / "verdict.md").read_text(encoding="utf-8")
CONTENT_PLAN = (TEMPLATES / "content-plan.md").read_text(encoding="utf-8")
LEAD = (TEMPLATES / "lead.md").read_text(encoding="utf-8")
STATE = (TEMPLATES / "state.md").read_text(encoding="utf-8")
LEDGER = (TEMPLATES / "ledger.md").read_text(encoding="utf-8")


def test_config_template_has_core_fields():
    for field in [
        "product:", "goal:", "icp:", "pain_lexicon:", "channels:", "verdict:", "kill_check_weeks:",
    ]:
        assert field in CONFIG


def test_decisions_template_documents_stages():
    assert "decisions:" in DECISIONS
    assert "decided_by: human_chat" in DECISIONS


def test_verdict_template_has_decision_gate():
    assert "**Decide:**" in VERDICT
    assert "go | watch | no-go | pivot" in VERDICT


def test_content_plan_template_has_status_gate():
    assert "**Status:**" in CONTENT_PLAN
    assert "accepted | skipped | held" in CONTENT_PLAN


def test_lead_template_has_state_lifecycle():
    assert "drafted | approved | sent | replied | qualified" in LEAD


def test_state_template_has_pending_actions_and_weeks_since_go():
    assert "## Pending human actions" in STATE
    assert "Weeks since Go" in STATE


def test_ledger_template_has_core_metrics():
    for metric in ["Signals seen", "Verdict", "Leads sent", "Qualified conversations"]:
        assert metric in LEDGER
