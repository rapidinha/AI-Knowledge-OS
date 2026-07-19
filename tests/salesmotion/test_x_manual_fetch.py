import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from salesmotion.providers.x_manual import fetch as x_manual_fetch


def test_parse_entry_normalizes_to_signal():
    entry = {
        "url": "https://x.com/someone/status/123",
        "text": "I hate doing this by hand every week.\nSecond line.",
        "author": "someone",
        "ts": "2026-07-18T09:00:00Z",
    }
    s = x_manual_fetch.parse_entry(entry)
    assert s["provider"] == "x_manual"
    assert s["url"] == entry["url"]
    assert s["title"] == "I hate doing this by hand every week."
    assert s["text"] == entry["text"]
    assert s["author"] == "someone"
    assert s["provenance"] == {"manual": True}
    assert s["id"].startswith("x_manual:")


def test_parse_entry_rejects_missing_fields():
    try:
        x_manual_fetch.parse_entry({"url": "https://x.com/1"})
        assert False, "expected ValueError"
    except ValueError as e:
        assert "text" in str(e) and "ts" in str(e)


def test_fetch_reads_inbox_and_skips_invalid_lines(tmp_path: Path):
    inbox = tmp_path / "x-manual.jsonl"
    valid_1 = {"url": "https://x.com/a", "text": "pain post one", "ts": "2026-07-18T09:00:00Z"}
    valid_2 = {"url": "https://x.com/b", "text": "pain post two", "ts": "2026-07-18T10:00:00Z"}
    invalid = {"url": "https://x.com/c"}  # missing text/ts
    inbox.write_text(
        "\n".join(json.dumps(e) for e in (valid_1, invalid, valid_2)) + "\n",
        encoding="utf-8",
    )
    signals = x_manual_fetch.fetch(inbox)
    assert len(signals) == 2
    assert {s["url"] for s in signals} == {"https://x.com/a", "https://x.com/b"}


def test_fetch_missing_inbox_returns_empty(tmp_path: Path):
    assert x_manual_fetch.fetch(tmp_path / "missing.jsonl") == []
