# Leverage Radar v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend Leverage Radar with a durable cross-day topic graph (Obsidian-readable), Lobsters + DEV.to providers, and YouTube channel-RSS “light” signals for Influence/Content — still skill-first, no vendor LLM APIs, no user CLI.

**Architecture:** Keep v1 vault protocol. Python adapters fetch Lobsters/DEV/YouTube RSS into `_raw/*.jsonl`. The agent clusters signals, updates `journals/radar/topics.yaml` (machine index) **and** per-topic Markdown notes under `journals/radar/topics/<slug>.md` (Obsidian + future AI summary surface), then writes the daily note with Recurrence + wikilinks. Provider failures degrade per-provider; the run continues.

**Tech Stack:** Python 3.11+ stdlib (`urllib`, `json`, `xml.etree`); optional PyYAML (already used in lab); pytest; Cursor/Claude skills; Obsidian Markdown.

**Spec:** [`docs/specs/2026-07-11-leverage-radar-v2-design.md`](../specs/2026-07-11-leverage-radar-v2-design.md)

**Hard rules:**

1. No `openai` / `anthropic` SDKs or HTTP LLM APIs from this repo.
2. No user-facing `radar` CLI / daemon.
3. No X/Twitter fetcher in this plan.
4. No YouTube transcripts — channel RSS only.
5. Clustering / topic merge / rolling summaries = **session model only**; Python only fetch + topics I/O helpers.
6. Topic Markdown notes are **durable vault memory** for Obsidian/AI — do not delete on retire (mark `status: retired` instead).

---

## File structure (lock this first)

```text
.gitignore                              # + journals/radar/topics.yaml

templates/radar/
  config.example.yaml                   # + lobsters, devto, youtube
  daily.md                              # + Recurrence + topic wikilink
  topics.example.yaml                   # empty machine index template
  topic.md                              # per-topic Obsidian note template
  topics-index.md                       # MOC / _index.md template

radar/
  fixtures/
    lobsters_hottest.json
    devto_articles.json
    youtube_atom.xml
  lib/
    topics_io.py                        # load/save topics.yaml only
  providers/
    lobsters/__init__.py
    lobsters/fetch.py
    devto/__init__.py
    devto/fetch.py
    youtube/__init__.py
    youtube/fetch.py
    fetch_enabled.py                    # register + try/except degrade

tests/radar/
  test_topics_io.py
  test_lobsters_fetch.py
  test_devto_fetch.py
  test_youtube_fetch.py
  test_fetch_enabled.py                 # extend
  test_smoke_daily_render.py            # extend Recurrence / topic link
  test_topic_template.py                # required sections for Obsidian AI

docs/radar/
  protocol.md, providers.md, scoring.md, using-agents.md, obsidian.md

skills/leverage-radar/SKILL.md          # + topic graph + note projection
.cursor/skills/leverage-radar/SKILL.md  # sync
.claude/skills/leverage-radar/SKILL.md  # sync

journals/radar/                         # PRIVATE lab only
  topics.yaml                           # gitignored machine index
  topics/                               # KEEP — Obsidian notes (commit in private SoT OK)
    _index.md
    <slug>.md
```

### Topic memory dual-write (required)

| Artifact | Audience | Git |
|----------|----------|-----|
| `journals/radar/topics.yaml` | Agent / scripts (compact graph) | **gitignore** |
| `journals/radar/topics/<slug>.md` | Obsidian + future AI summarization | **keep in vault**; private SoT may commit |
| `journals/radar/topics/_index.md` | MOC / Dataview entry | keep |

Each topic note must remain stable enough that a later Obsidian AI pass can open `topics/<slug>.md` and produce a richer summary from `## Rolling summary`, `## Timeline`, and `## Sources` without needing `_raw/` history.

---

### Task 1: Gitignore + topic templates (Obsidian-ready)

**Files:**
- Modify: `.gitignore`
- Create: `templates/radar/topics.example.yaml`
- Create: `templates/radar/topic.md`
- Create: `templates/radar/topics-index.md`

- [ ] **Step 1: Add gitignore entry**

Append to `.gitignore` (keep existing radar lines):

```gitignore
journals/radar/topics.yaml
```

Do **not** gitignore `journals/radar/topics/` — those Markdown notes are the durable Obsidian surface.

- [ ] **Step 2: Write `templates/radar/topics.example.yaml`**

```yaml
# Copy to journals/radar/topics.yaml on first radar run (private — gitignored).
# Machine index for the topic graph. Obsidian notes live in journals/radar/topics/*.md
version: 1
updated_at: null
topics: []
```

- [ ] **Step 3: Write `templates/radar/topic.md`**

```markdown
---
slug: {{slug}}
title: "{{title}}"
status: {{status}}
first_seen: {{first_seen}}
last_seen: {{last_seen}}
hit_count: {{hit_count}}
providers: {{providers_csv}}
aliases: {{aliases_csv}}
radar_topic: true
---

# {{title}}

## Rolling summary

{{rolling_summary}}

<!-- Agent updates this section each day the topic appears.
     Future Obsidian / AI tools should treat this as the primary abstract. -->

## Timeline

{{timeline}}

<!-- Bullet list: `- YYYY-MM-DD — short note / link to daily [[journals/radar/YYYY-MM-DD]]` -->

## Sources

{{sources_md}}

## Related

{{related_md}}
```

- [ ] **Step 4: Write `templates/radar/topics-index.md`**

```markdown
---
radar_topics_index: true
---

# Radar topics

Durable theme memory for Leverage Radar. Each note under this folder is one topic.

## How to use

- Morning: open today's `[[journals/radar/YYYY-MM-DD]]`
- Deep dive: open a topic note; read **Rolling summary**
- Later AI: ask the vault agent to summarize `journals/radar/topics/` or a single `slug`

## Active topics

{{active_list}}

<!-- Agent maintains a bullet list: `- [[journals/radar/topics/<slug>|<title>]] — status · hits:N · last:YYYY-MM-DD` -->

## Retired

{{retired_list}}
```

- [ ] **Step 5: Commit**

```bash
git add .gitignore templates/radar/topics.example.yaml templates/radar/topic.md templates/radar/topics-index.md
git commit -m "feat(radar): topic templates for Obsidian-durable memory"
```

---

### Task 2: `topics_io` load/save helper

**Files:**
- Create: `radar/lib/topics_io.py`
- Test: `tests/radar/test_topics_io.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/radar/test_topics_io.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.lib import topics_io


def test_round_trip_topics_yaml(tmp_path: Path):
    path = tmp_path / "topics.yaml"
    data = {
        "version": 1,
        "updated_at": "2026-07-11T12:00:00Z",
        "topics": [
            {
                "slug": "agent-skills",
                "title": "Agent skills packaging",
                "aliases": ["claude skills"],
                "first_seen": "2026-07-11",
                "last_seen": "2026-07-11",
                "hit_count": 1,
                "provider_set": ["hn", "lobsters"],
                "recent_urls": ["https://example.com/a"],
                "status": "emerging",
            }
        ],
    }
    topics_io.save_topics(path, data)
    loaded = topics_io.load_topics(path)
    assert loaded["version"] == 1
    assert loaded["topics"][0]["slug"] == "agent-skills"
    assert loaded["topics"][0]["provider_set"] == ["hn", "lobsters"]


def test_load_missing_returns_empty_graph(tmp_path: Path):
    path = tmp_path / "missing.yaml"
    loaded = topics_io.load_topics(path)
    assert loaded["version"] == 1
    assert loaded["topics"] == []
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/radar/test_topics_io.py -v
```

Expected: FAIL (`ModuleNotFoundError` or import error for `topics_io`).

- [ ] **Step 3: Write minimal implementation**

```python
# radar/lib/topics_io.py
from __future__ import annotations

from pathlib import Path
from typing import Any

EMPTY: dict[str, Any] = {"version": 1, "updated_at": None, "topics": []}


def load_topics(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "updated_at": None, "topics": []}
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
    except Exception:
        return {"version": 1, "updated_at": None, "topics": []}
    if not isinstance(data, dict):
        return {"version": 1, "updated_at": None, "topics": []}
    topics = data.get("topics") or []
    if not isinstance(topics, list):
        topics = []
    return {
        "version": int(data.get("version") or 1),
        "updated_at": data.get("updated_at"),
        "topics": topics,
    }


def save_topics(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore

        path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except Exception:
        # ponytail: minimal fallback without PyYAML — enough for empty bootstrap
        path.write_text("version: 1\nupdated_at: null\ntopics: []\n", encoding="utf-8")
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/radar/test_topics_io.py -v
```

Expected: PASS (requires PyYAML in the environment; if missing, `pip install pyyaml`).

- [ ] **Step 5: Commit**

```bash
git add radar/lib/topics_io.py tests/radar/test_topics_io.py
git commit -m "feat(radar): topics.yaml load/save helper"
```

---

### Task 3: Lobsters provider (TDD)

**Files:**
- Create: `radar/providers/lobsters/__init__.py` (empty)
- Create: `radar/providers/lobsters/fetch.py`
- Create: `radar/fixtures/lobsters_hottest.json`
- Test: `tests/radar/test_lobsters_fetch.py`

- [ ] **Step 1: Write fixture**

```json
[
  {
    "short_id": "abc123",
    "created_at": "2026-07-11T10:00:00.000-05:00",
    "title": "Agent skills are the new packaging",
    "url": "https://example.com/skills",
    "score": 42,
    "comment_count": 7,
    "submitter_user": {"username": "dev"},
    "tags": ["ai", "practices"]
  }
]
```

- [ ] **Step 2: Write the failing test**

```python
# tests/radar/test_lobsters_fetch.py
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.providers.lobsters import fetch as lobsters_fetch

FIXTURE = ROOT / "radar" / "fixtures" / "lobsters_hottest.json"


def test_parse_hottest_json():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = lobsters_fetch.parse_hottest(payload)
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "lobsters:abc123"
    assert s["provider"] == "lobsters"
    assert s["title"].startswith("Agent skills")
    assert s["url"] == "https://example.com/skills"
    assert s["metrics"]["score"] == 42
    assert s["provenance"]["tags"] == ["ai", "practices"]


def test_fetch_uses_get_json(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(lobsters_fetch, "get_json", lambda url: payload)
    signals = lobsters_fetch.fetch(limit=10)
    assert len(signals) == 1
```

- [ ] **Step 3: Run test to verify it fails**

```bash
python3 -m pytest tests/radar/test_lobsters_fetch.py -v
```

Expected: FAIL (module missing).

- [ ] **Step 4: Implement fetcher**

```python
# radar/providers/lobsters/fetch.py
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://lobste.rs"
UA = "ai-knowledge-os-radar/0.1"


def get_json(url: str) -> Any:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_hottest(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    for item in items:
        sid = item.get("short_id") or ""
        if not sid:
            continue
        submitter = item.get("submitter_user") or {}
        story_url = item.get("url") or f"{BASE}/s/{sid}"
        out.append(
            {
                "id": f"lobsters:{sid}",
                "provider": "lobsters",
                "url": story_url,
                "title": item.get("title") or "",
                "ts": item.get("created_at") or "",
                "author": submitter.get("username"),
                "text": None,
                "metrics": {
                    "score": item.get("score"),
                    "comment_count": item.get("comment_count"),
                },
                "provenance": {
                    "short_id": sid,
                    "lobsters_url": f"{BASE}/s/{sid}",
                    "tags": item.get("tags") or [],
                },
            }
        )
    return out


def fetch(tag: str = "", limit: int = 30) -> list[dict]:
    if tag:
        url = f"{BASE}/t/{tag}.json"
    else:
        url = f"{BASE}/hottest.json"
    items = get_json(url)
    if not isinstance(items, list):
        return []
    return parse_hottest(items)[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="lobsters-fetch")
    p.add_argument("--tag", default="")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(tag=args.tag, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} lobsters signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run tests**

```bash
python3 -m pytest tests/radar/test_lobsters_fetch.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add radar/providers/lobsters radar/fixtures/lobsters_hottest.json tests/radar/test_lobsters_fetch.py
git commit -m "feat(radar): Lobsters provider"
```

---

### Task 4: DEV.to provider (TDD)

**Files:**
- Create: `radar/providers/devto/__init__.py`
- Create: `radar/providers/devto/fetch.py`
- Create: `radar/fixtures/devto_articles.json`
- Test: `tests/radar/test_devto_fetch.py`

- [ ] **Step 1: Write fixture**

```json
[
  {
    "id": 999001,
    "title": "Shipping agent skills in production",
    "url": "https://dev.to/example/shipping-agent-skills",
    "published_timestamp": "2026-07-11T12:00:00Z",
    "user": {"username": "example"},
    "public_reactions_count": 12,
    "comments_count": 3,
    "tag_list": ["ai", "productivity"]
  }
]
```

- [ ] **Step 2: Write the failing test**

```python
# tests/radar/test_devto_fetch.py
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.providers.devto import fetch as devto_fetch

FIXTURE = ROOT / "radar" / "fixtures" / "devto_articles.json"


def test_parse_articles():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    signals = devto_fetch.parse_articles(payload)
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "devto:999001"
    assert s["provider"] == "devto"
    assert "agent skills" in s["title"].lower()
    assert s["metrics"]["public_reactions_count"] == 12


def test_fetch_monkeypatched(monkeypatch):
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr(devto_fetch, "get_json", lambda url: payload)
    assert len(devto_fetch.fetch(tag="ai", limit=10)) == 1
```

- [ ] **Step 3: Run test — expect FAIL**

```bash
python3 -m pytest tests/radar/test_devto_fetch.py -v
```

- [ ] **Step 4: Implement**

```python
# radar/providers/devto/fetch.py
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://dev.to/api/articles"
UA = "ai-knowledge-os-radar/0.1"


def get_json(url: str) -> Any:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_articles(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    for item in items:
        aid = item.get("id")
        if aid is None:
            continue
        user = item.get("user") or {}
        out.append(
            {
                "id": f"devto:{aid}",
                "provider": "devto",
                "url": item.get("url") or "",
                "title": item.get("title") or "",
                "ts": item.get("published_timestamp") or "",
                "author": user.get("username"),
                "text": None,
                "metrics": {
                    "public_reactions_count": item.get("public_reactions_count"),
                    "comments_count": item.get("comments_count"),
                },
                "provenance": {"devto_id": aid, "tag_list": item.get("tag_list") or []},
            }
        )
    return out


def fetch(tag: str = "", limit: int = 30) -> list[dict]:
    params: dict[str, Any] = {"per_page": max(1, min(limit, 100))}
    if tag:
        params["tag"] = tag
    url = f"{BASE}?{urlencode(params)}"
    items = get_json(url)
    if not isinstance(items, list):
        return []
    return parse_articles(items)[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="devto-fetch")
    p.add_argument("--tag", default="")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(tag=args.tag, limit=args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} devto signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run tests — expect PASS; commit**

```bash
python3 -m pytest tests/radar/test_devto_fetch.py -v
git add radar/providers/devto radar/fixtures/devto_articles.json tests/radar/test_devto_fetch.py
git commit -m "feat(radar): DEV.to provider"
```

---

### Task 5: YouTube light (channel RSS)

**Files:**
- Create: `radar/providers/youtube/__init__.py`
- Create: `radar/providers/youtube/fetch.py`
- Create: `radar/fixtures/youtube_atom.xml`
- Test: `tests/radar/test_youtube_fetch.py`

- [ ] **Step 1: Write Atom fixture** (minimal YouTube-shaped feed)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015"
      xmlns:media="http://search.yahoo.com/mrss/"
      xmlns="http://www.w3.org/2005/Atom">
  <title>Example Eng</title>
  <entry>
    <id>yt:video:VIDEO123</id>
    <yt:videoId>VIDEO123</yt:videoId>
    <yt:channelId>UCxxxx</yt:channelId>
    <title>How agent skills change workflows</title>
    <published>2026-07-10T15:00:00+00:00</published>
    <author><name>Example Eng</name></author>
    <link rel="alternate" href="https://www.youtube.com/watch?v=VIDEO123"/>
  </entry>
</feed>
```

- [ ] **Step 2: Write failing tests**

```python
# tests/radar/test_youtube_fetch.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.providers.youtube import fetch as youtube_fetch

FIXTURE = ROOT / "radar" / "fixtures" / "youtube_atom.xml"


def test_parse_atom():
    xml = FIXTURE.read_text(encoding="utf-8")
    signals = youtube_fetch.parse_atom(xml, channel_label="Example Eng")
    assert len(signals) == 1
    s = signals[0]
    assert s["id"] == "youtube:VIDEO123"
    assert s["provider"] == "youtube"
    assert s["url"].endswith("VIDEO123")
    assert s["author"] == "Example Eng"


def test_fetch_channels_monkeypatched(monkeypatch):
    xml = FIXTURE.read_text(encoding="utf-8")
    monkeypatch.setattr(youtube_fetch, "get_feed", lambda url: xml)
    signals = youtube_fetch.fetch(
        channels=[{"id": "UCxxxx", "label": "Example Eng"}],
        max_videos_per_channel=5,
    )
    assert len(signals) == 1


def test_invalid_channel_skipped(monkeypatch):
    def boom(url: str) -> str:
        raise OSError("fail")

    monkeypatch.setattr(youtube_fetch, "get_feed", boom)
    signals = youtube_fetch.fetch(channels=[{"id": "bad", "label": "x"}], max_videos_per_channel=5)
    assert signals == []
```

- [ ] **Step 3: Run — expect FAIL; then implement**

```python
# radar/providers/youtube/fetch.py
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

ATOM_NS = "http://www.w3.org/2005/Atom"
YT_NS = "http://www.youtube.com/xml/schemas/2015"
UA = "ai-knowledge-os-radar/0.1"


def _ns(tag: str, ns: str = ATOM_NS) -> str:
    return f"{{{ns}}}{tag}"


def feed_url(channel_id: str) -> str:
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def get_feed(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_atom(xml_text: str, channel_label: str | None = None) -> list[dict]:
    root = ET.fromstring(xml_text)
    out: list[dict] = []
    for entry in root.findall(_ns("entry")):
        video_el = entry.find(f"{{{YT_NS}}}videoId")
        video_id = (video_el.text if video_el is not None else "") or ""
        if not video_id:
            entry_id = entry.findtext(_ns("id"), default="")
            if "yt:video:" in entry_id:
                video_id = entry_id.rsplit(":", 1)[-1]
        if not video_id:
            continue
        author = entry.findtext(f"{_ns('author')}/{_ns('name')}") or channel_label
        link = ""
        for ln in entry.findall(_ns("link")):
            if ln.get("rel") == "alternate":
                link = ln.get("href") or ""
                break
        if not link:
            link = f"https://www.youtube.com/watch?v={video_id}"
        out.append(
            {
                "id": f"youtube:{video_id}",
                "provider": "youtube",
                "url": link,
                "title": (entry.findtext(_ns("title"), default="") or "").strip(),
                "ts": entry.findtext(_ns("published"), default="") or "",
                "author": author,
                "text": None,
                "metrics": {},
                "provenance": {"video_id": video_id, "channel_label": channel_label},
            }
        )
    return out


def fetch(
    channels: list[dict[str, Any]] | None = None,
    max_videos_per_channel: int = 5,
) -> list[dict]:
    channels = channels or []
    out: list[dict] = []
    for ch in channels:
        cid = (ch or {}).get("id") or ""
        if not cid:
            continue
        label = (ch or {}).get("label")
        try:
            xml = get_feed(feed_url(cid))
            out.extend(parse_atom(xml, channel_label=label)[: max(0, max_videos_per_channel)])
        except Exception:
            continue
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="youtube-fetch")
    p.add_argument("--channel-id", action="append", default=[])
    p.add_argument("--max-per-channel", type=int, default=5)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    channels = [{"id": c, "label": None} for c in args.channel_id]
    signals = fetch(channels=channels, max_videos_per_channel=args.max_per_channel)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} youtube signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Tests PASS + commit**

```bash
python3 -m pytest tests/radar/test_youtube_fetch.py -v
git add radar/providers/youtube radar/fixtures/youtube_atom.xml tests/radar/test_youtube_fetch.py
git commit -m "feat(radar): YouTube channel RSS provider (light)"
```

---

### Task 6: Wire `fetch_enabled` + per-provider degrade

**Files:**
- Modify: `radar/providers/fetch_enabled.py`
- Modify: `tests/radar/test_fetch_enabled.py`

- [ ] **Step 1: Extend tests**

Add to `tests/radar/test_fetch_enabled.py`:

```python
from radar.providers.lobsters import fetch as lobsters_fetch
from radar.providers.devto import fetch as devto_fetch
from radar.providers.youtube import fetch as youtube_fetch


def test_fetch_enabled_includes_lobsters(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: false
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  lobsters:
    enabled: true
  devto:
    enabled: false
  youtube:
    enabled: false
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(
        lobsters_fetch,
        "fetch",
        lambda tag="", limit=30: [
            {
                "id": "lobsters:1",
                "provider": "lobsters",
                "url": "https://x.test",
                "title": "T",
                "ts": "2026-07-11T00:00:00Z",
            }
        ],
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    assert "lobsters:1" in out.read_text(encoding="utf-8")


def test_provider_error_degrades(tmp_path: Path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
providers:
  hn:
    enabled: true
  lobsters:
    enabled: true
  arxiv:
    enabled: false
  github_trending:
    enabled: false
  reddit:
    enabled: false
  devto:
    enabled: false
  youtube:
    enabled: false
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    monkeypatch.setattr(hn_fetch, "fetch", lambda limit=30: [HN_SIGNAL])
    monkeypatch.setattr(
        lobsters_fetch,
        "fetch",
        lambda tag="", limit=30: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    assert fetch_enabled.main(["--config", str(cfg), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "hn:1" in text
    assert "lobsters:" not in text
```

- [ ] **Step 2: Run — expect FAIL on degrade / missing providers**

```bash
python3 -m pytest tests/radar/test_fetch_enabled.py -v
```

- [ ] **Step 3: Update `fetch_enabled.py`**

Replace imports and `PROVIDER_FETCHERS` / `fetch_all` with:

```python
from radar.providers.lobsters import fetch as lobsters_fetch
from radar.providers.devto import fetch as devto_fetch
from radar.providers.youtube import fetch as youtube_fetch


def _fetch_lobsters(meta: dict[str, Any]) -> list[dict]:
    return lobsters_fetch.fetch(tag=meta.get("tag") or "", limit=int(meta.get("limit") or 30))


def _fetch_devto(meta: dict[str, Any]) -> list[dict]:
    return devto_fetch.fetch(tag=meta.get("tag") or "", limit=int(meta.get("limit") or 30))


def _fetch_youtube(meta: dict[str, Any]) -> list[dict]:
    return youtube_fetch.fetch(
        channels=meta.get("channels") or [],
        max_videos_per_channel=int(meta.get("max_videos_per_channel") or 5),
    )


PROVIDER_FETCHERS: dict[str, Callable[[dict[str, Any]], list[dict]]] = {
    "hn": _fetch_hn,
    "github_trending": _fetch_github_trending,
    "arxiv": _fetch_arxiv,
    "reddit": _fetch_reddit,
    "lobsters": _fetch_lobsters,
    "devto": _fetch_devto,
    "youtube": _fetch_youtube,
}


def fetch_all(config: dict[str, Any]) -> tuple[list[dict], dict[str, int]]:
    providers = config.get("providers") or {}
    raw: list[dict] = []
    counts: dict[str, int] = {}

    for name in enabled_providers(config):
        fetcher = PROVIDER_FETCHERS.get(name)
        if fetcher is None:
            print(f"skip unknown provider: {name}", file=sys.stderr)
            continue
        meta = providers.get(name) or {}
        if not isinstance(meta, dict):
            meta = {}
        try:
            signals = fetcher(meta)
        except Exception as exc:
            print(f"{name}: degraded ({exc})", file=sys.stderr)
            counts[name] = 0
            continue
        counts[name] = len(signals)
        raw.extend(signals)

    return dedupe_signals(raw), counts
```

Keep existing `_fetch_hn` / github / arxiv / reddit helpers unchanged.

- [ ] **Step 4: Tests PASS + commit**

```bash
python3 -m pytest tests/radar/test_fetch_enabled.py -v
git add radar/providers/fetch_enabled.py tests/radar/test_fetch_enabled.py
git commit -m "feat(radar): wire lobsters/devto/youtube with degrade"
```

---

### Task 7: Config example

**Files:**
- Modify: `templates/radar/config.example.yaml`

- [ ] **Step 1: Append provider blocks** (after `reddit:`)

```yaml
  lobsters:
    enabled: true
    tag: ""
    limit: 30

  devto:
    enabled: true
    tag: "ai"
    limit: 30

  youtube:
    enabled: false
    channels:
      - id: UCxxxx
        label: "Example Eng"
    search_queries: []
    max_videos_per_channel: 5
```

- [ ] **Step 2: Commit**

```bash
git add templates/radar/config.example.yaml
git commit -m "docs(radar): config example for v2 providers"
```

---

### Task 8: Daily template + smoke tests (Recurrence + topic link)

**Files:**
- Modify: `templates/radar/daily.md`
- Modify: `tests/radar/test_smoke_daily_render.py`
- Create: `tests/radar/test_topic_template.py`

- [ ] **Step 1: Update opportunity block in `templates/radar/daily.md`**

```markdown
### {{rank}}. {{title}}

- **Topic:** [[journals/radar/topics/{{topic_slug}}|{{topic_title}}]]
- **Category:** {{category}}
- **Recurrence:** hits {{hit_count}} · first {{first_seen}} · providers {{provider_set}}
- **Scores:** {{scores_inline}}
- **Why:** {{rationale}}
- **Sources:** {{sources_md}}
- **Decide:** `pending` <!-- agent sets: ignore | watch | research | known | merge -->
```

Also add under Signals:

```markdown
## Topics

Index: `journals/radar/topics/_index.md` · Graph: `journals/radar/topics.yaml` (private)
```

- [ ] **Step 2: Extend smoke test**

```python
# tests/radar/test_smoke_daily_render.py
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
```

- [ ] **Step 3: Topic template smoke test**

```python
# tests/radar/test_topic_template.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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
```

- [ ] **Step 4: Run + commit**

```bash
python3 -m pytest tests/radar/test_smoke_daily_render.py tests/radar/test_topic_template.py -v
git add templates/radar/daily.md tests/radar/test_smoke_daily_render.py tests/radar/test_topic_template.py
git commit -m "feat(radar): daily Recurrence + topic wikilinks for Obsidian"
```

---

### Task 9: Skill — topic graph dual-write + clustering rules

**Files:**
- Modify: `skills/leverage-radar/SKILL.md`
- Sync identical copies to `.cursor/skills/leverage-radar/SKILL.md` and `.claude/skills/leverage-radar/SKILL.md`

- [ ] **Step 1: Replace Workflow section** with:

```markdown
## Workflow

1. **Config** — Read `journals/radar/config.yaml`. If missing, copy from `templates/radar/config.example.yaml` and ask the user to enable providers before continuing.

2. **Topic store bootstrap**
   - If `journals/radar/topics.yaml` missing → copy `templates/radar/topics.example.yaml`.
   - Ensure `journals/radar/topics/` exists. If `_index.md` missing → copy `templates/radar/topics-index.md`.

3. **Fetch** — Run (today's date as `YYYY-MM-DD`):

   ```bash
   python radar/providers/fetch_enabled.py \
     --config journals/radar/config.yaml \
     --out journals/radar/_raw/YYYY-MM-DD.jsonl
   ```

   Note any `degraded` lines from stderr for the Executive Summary.

4. **Load** — Read jsonl + `topics.yaml` via reading files (optional: `radar.lib.topics_io`). Dedupe URLs/titles if needed.

5. **Cluster and score (session model only)** — never OpenAI/Anthropic HTTP APIs or SDKs:
   - Cluster into ≤ `defaults.max_opportunities` Opportunities (ecosystem themes, not per-feed lists).
   - Prefer multi-provider Opportunities when evidence exists.
   - Bias YouTube-heavy themes toward **Influence** (content leverage).
   - Assign/create topic `slug` per Opportunity; merge with existing topics on alias/title/url overlap.
   - Update topic fields: `hit_count` (+1 once per distinct day), `last_seen`, `provider_set` union, `recent_urls` (cap 8), `status` hint (`emerging` / `validated` when hits≥3 and ≥2 providers).
   - Cap ~200 topics; set `status: retired` on oldest low-hit — **do not delete** Markdown notes.

6. **Persist topic memory (dual-write — required)**
   - Write `journals/radar/topics.yaml` (machine index).
   - For each touched topic, create/update `journals/radar/topics/<slug>.md` from `templates/radar/topic.md`:
     - Refresh **Rolling summary** (2–4 sentences; cumulative, not only today).
     - Append today's bullet under **Timeline** with wikilink to `[[journals/radar/YYYY-MM-DD]]`.
     - Merge **Sources** URLs.
   - Update `journals/radar/topics/_index.md` active/retired lists.
   - These notes are for **Obsidian and future AI summarization** — keep them readable without `_raw/`.

7. **Write daily note** — `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md`, including Topic wikilink + Recurrence from the topic graph.

8. **Stop** — No Stage 2 / wiki edits unless the user Decide's.
```

Keep existing HITL + Bans sections. Add under References: v2 design spec path.

- [ ] **Step 2: Sync three skill files** (`cp` or identical write) and verify:

```bash
diff -q skills/leverage-radar/SKILL.md .cursor/skills/leverage-radar/SKILL.md
diff -q skills/leverage-radar/SKILL.md .claude/skills/leverage-radar/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add skills/leverage-radar/SKILL.md .cursor/skills/leverage-radar/SKILL.md .claude/skills/leverage-radar/SKILL.md
git commit -m "feat(radar): skill dual-writes topic graph + Obsidian notes"
```

---

### Task 10: Docs suite

**Files:**
- Modify: `docs/radar/protocol.md`
- Modify: `docs/radar/providers.md`
- Modify: `docs/radar/scoring.md`
- Modify: `docs/radar/obsidian.md`
- Modify: `docs/radar/using-agents.md`

- [ ] **Step 1: protocol.md** — document paths:

```markdown
| `journals/radar/topics.yaml` | Machine topic graph (gitignored) |
| `journals/radar/topics/<slug>.md` | Obsidian topic notes + rolling summary (durable) |
| `journals/radar/topics/_index.md` | Topic MOC |
```

State dual-write explicitly; note future AI should prefer topic notes for summarization.

- [ ] **Step 2: providers.md** — add Lobsters, DEV.to, YouTube light connect steps; YouTube = channel RSS only; `search_queries` optional agent browse; no X.

- [ ] **Step 3: scoring.md** — recurrence fields; YouTube → Influence bias.

- [ ] **Step 4: obsidian.md** — how to browse topics folder; Dataview hint optional:

```markdown
```dataview
TABLE status, hit_count, last_seen FROM "journals/radar/topics" WHERE radar_topic = true SORT hit_count DESC
```
```

- [ ] **Step 5: using-agents.md** — mention topic dual-write step; PyYAML for topics_io.

- [ ] **Step 6: Commit**

```bash
git add docs/radar/
git commit -m "docs(radar): v2 protocol, providers, Obsidian topic memory"
```

---

### Task 11: Manual E2E checklist (private lab)

**Files:** none required (checklist in commit message / lab only)

- [ ] **Step 1: Merge config** — update local `journals/radar/config.yaml` with lobsters/devto enabled; optionally one real YouTube `channel_id`.

- [ ] **Step 2: Run skill** — “Run today's Leverage Radar”.

- [ ] **Step 3: Verify artifacts**
  - `_raw/YYYY-MM-DD.jsonl` includes `lobsters` / `devto` (and `youtube` if enabled)
  - `topics.yaml` exists and has ≥1 topic after a run with opportunities
  - `topics/<slug>.md` has Rolling summary + Timeline
  - `_index.md` lists the topic
  - Daily note has Recurrence + wikilink to topic note

- [ ] **Step 4: Second-day smoke** (same or next calendar day simulation)
  - Re-run with overlapping theme → `hit_count` increments; Timeline gains a line; summary updates; **note file not replaced blank**

- [ ] **Step 5: Commit only OSS-safe files** — never `config.yaml`, `_raw/`, or private `topics.yaml`. Topic Markdown may be committed on **private** SoT if the user wants vault history; omit from public PRs (`journals/` forbidden on upstream).

---

## Self-review (plan vs spec)

| Spec requirement | Task |
|------------------|------|
| Topic graph `topics.yaml` | 1, 2, 9 |
| Obsidian/AI-durable summaries | 1, 8, 9, 10 (dual-write Markdown) |
| Lobsters + DEV.to | 3, 4, 6, 7 |
| YouTube light RSS | 5, 6, 7 |
| Multi-provider Opportunities + recurrence | 8, 9 |
| Provider degrade | 6 |
| No X / no transcripts / no daemon / no LLM SDKs | Hard rules + Task 9 bans |
| Docs + skill sync | 9, 10 |
| Tests/fixtures | 2–6, 8 |
| Governance gitignore | 1 |

**Placeholder scan:** none intentional.  
**Type consistency:** providers `lobsters` | `devto` | `youtube`; topic fields match spec + `rolling_summary` on Markdown only.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-11-leverage-radar-v2.md` (mirrored under `docs/plans/`).

**Two execution options:**

**1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — execute tasks in this session with executing-plans and checkpoints

**Which approach?**
