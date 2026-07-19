# tests/salesmotion/test_contracts.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = ROOT / "contracts" / "prompts" / "sales"

EXPECTED_FILES = [
    "icp.md",
    "qualify.md",
    "verdict.md",
    "content-plan.md",
    "draft-lead.md",
    "draft-post.md",
    "state-resume.md",
]


def test_all_contract_files_exist():
    for name in EXPECTED_FILES:
        assert (CONTRACTS_DIR / name).exists(), f"missing contract: {name}"


def test_all_contracts_have_required_sections():
    for name in EXPECTED_FILES:
        text = (CONTRACTS_DIR / name).read_text(encoding="utf-8")
        assert "## Input" in text
        assert "## Output expectations" in text
        assert "## Bans" in text


def test_all_contracts_ban_vendor_llm_http():
    for name in EXPECTED_FILES:
        text = (CONTRACTS_DIR / name).read_text(encoding="utf-8")
        assert "vendor LLM" in text
