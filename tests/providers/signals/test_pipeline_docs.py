from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = (ROOT / "docs" / "radar" / "protocol.md").read_text(encoding="utf-8")


def test_protocol_documents_pipeline_artifacts():
    assert "_pipeline/" in PROTOCOL
    assert "run_stages" in PROTOCOL


def test_protocol_documents_run_stages_entrypoint():
    assert "providers/signals/pipeline/run_stages.py" in PROTOCOL
