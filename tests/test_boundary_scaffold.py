from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ROOT = {"knowledge", "notes", "journals", "experiments", "obsidian", "vault"}
RESEARCH_ALLOWED = {".gitkeep", "README.md"}


def test_forbidden_personal_paths_absent():
    for name in FORBIDDEN_ROOT:
        assert not (ROOT / name).exists(), f"forbidden path present: {name}"


def test_research_is_scaffold_only_if_present():
    research = ROOT / "research"
    if not research.exists():
        return
    names = {p.name for p in research.iterdir() if p.name != ".DS_Store"}
    assert names <= RESEARCH_ALLOWED, f"research/ not scaffold-only: {names}"


def test_wiki_principles_has_no_markdown_corpus():
    principles = ROOT / "wiki" / "principles"
    if not principles.exists():
        return
    md = list(principles.glob("*.md"))
    assert md == [], f"public wiki/principles must be empty scaffold, found {md}"
