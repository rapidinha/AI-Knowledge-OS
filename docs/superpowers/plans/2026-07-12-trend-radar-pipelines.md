# Trend Radar Pipelines Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an auditable ingest → enrich → correlate → score → synthesize pipeline (artifacts under `journals/radar/_pipeline/`), new providers (Product Hunt, RSS, YouTube Data API, GA4, Search Console), agent-assisted provider setup, and skill/docs updates — as a patch over Leverage Radar v2.

**Architecture:** Python-first stage functions write versioned JSON/JSONL artifacts; the session agent (supervisor skill) orchestrates stages with minimal context per stage. No Dagster. No vendor LLM SDKs. Personal providers only boost `personal_relevance`. Legacy `_raw/YYYY-MM-DD.jsonl` remains a copy of `signals.jsonl` for v2 compatibility.

**Tech Stack:** Python 3.11+ stdlib (`urllib`, `json`, `xml.etree`, `dataclasses`); optional PyYAML; pytest; Cursor/Claude skills. Dataclass models + JSON Schema mirrors (no Pydantic hard dependency — keeps labs stdlib-friendly; schemas stay versioned and auditable).

**Spec:** [`docs/superpowers/specs/2026-07-12-trend-radar-pipelines-design.md`](../specs/2026-07-12-trend-radar-pipelines-design.md)

**Hard rules:**

1. No `openai` / `anthropic` SDKs or HTTP LLM APIs from this repo.
2. No user-facing product CLI / daemon (agent-invoked Python entrypoints only).
3. No Dagster / Prefect / Temporal / LangGraph.
4. No GraphRAG / Neo4j / LlamaIndex in this plan.
5. Do not commit `journals/radar/config.yaml`, `_pipeline/`, `_raw/`, or personal API outputs to public upstream.
6. Clustering prose / daily narrative = **session model**; Python owns fetch, cheap enrich, hint-cluster, deterministic score fields, artifact I/O.

---

## File structure (lock this first)

```text
.gitignore                              # + journals/radar/_pipeline/

radar/
  schema/
    signal.schema.json                  # existing (keep)
    enriched_signal.schema.json         # new
    cluster.schema.json                 # new
    run_meta.schema.json                # new
  pipeline/
    __init__.py
    models.py                           # dataclasses + validate/to_dict
    paths.py                            # resolve _pipeline/YYYY-MM-DD/*
    artifacts.py                        # read/write jsonl + json
    run_meta.py                         # RunMeta builder
    enrich.py                           # cheap enrich + cache
    correlate.py                        # overlap clustering hints
    score.py                            # consensus, recurrence, personal boost
    provider_setup.py                   # missing-secret checks + setup hints
    run_stages.py                       # agent entrypoint: --stage ingest|enrich|…
  providers/
    product_hunt/{__init__.py,fetch.py}
    rss/{__init__.py,fetch.py}
    youtube_api/{__init__.py,fetch.py}
    ga4/{__init__.py,fetch.py}
    search_console/{__init__.py,fetch.py}
    fetch_enabled.py                    # register + credential gate
  fixtures/
    product_hunt_posts.json
    rss_feed.xml
    youtube_api_search.json
    ga4_report.json
    gsc_query.json

templates/radar/
  config.example.yaml                   # + new providers + pipeline caps
contracts/prompts/                      # stage prompt stubs for supervisor
  enrich.md
  correlate.md
  score.md
  synthesize.md
  configure-provider.md

skills/leverage-radar/SKILL.md          # pipeline + setup assist
.cursor/skills/leverage-radar/SKILL.md  # sync
.claude/skills/leverage-radar/SKILL.md  # sync

docs/radar/
  protocol.md, providers.md, scoring.md, using-agents.md

tests/radar/
  test_pipeline_models.py
  test_pipeline_paths.py
  test_pipeline_enrich.py
  test_pipeline_correlate.py
  test_pipeline_score.py
  test_provider_setup.py
  test_run_stages.py
  test_product_hunt_fetch.py
  test_rss_fetch.py
  test_youtube_api_fetch.py
  test_ga4_fetch.py
  test_search_console_fetch.py
  test_fetch_enabled.py                 # extend
  test_smoke_daily_render.py            # extend pipeline headings hints
```

---

### Task 1: Gitignore + pipeline package skeleton

**Files:**
- Modify: `.gitignore`
- Create: `radar/pipeline/__init__.py`
- Create: `radar/pipeline/paths.py`
- Test: `tests/radar/test_pipeline_paths.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/radar/test_pipeline_paths.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.paths import PipelinePaths


def test_pipeline_paths_layout(tmp_path: Path):
    p = PipelinePaths(radar_root=tmp_path, date="2026-07-12")
    assert p.dir == tmp_path / "_pipeline" / "2026-07-12"
    assert p.signals.name == "signals.jsonl"
    assert p.enriched.name == "enriched.jsonl"
    assert p.clusters.name == "clusters.json"
    assert p.run_meta.name == "run_meta.json"
    assert p.legacy_raw == tmp_path / "_raw" / "2026-07-12.jsonl"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/radar/test_pipeline_paths.py -v
```

Expected: FAIL with `ModuleNotFoundError` or import error for `radar.pipeline.paths`.

- [ ] **Step 3: Write minimal implementation**

Append to `.gitignore`:

```gitignore
journals/radar/_pipeline/
```

Create `radar/pipeline/__init__.py` (empty or docstring only).

Create `radar/pipeline/paths.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelinePaths:
    radar_root: Path
    date: str  # YYYY-MM-DD

    @property
    def dir(self) -> Path:
        return self.radar_root / "_pipeline" / self.date

    @property
    def signals(self) -> Path:
        return self.dir / "signals.jsonl"

    @property
    def enriched(self) -> Path:
        return self.dir / "enriched.jsonl"

    @property
    def clusters(self) -> Path:
        return self.dir / "clusters.json"

    @property
    def run_meta(self) -> Path:
        return self.dir / "run_meta.json"

    @property
    def legacy_raw(self) -> Path:
        return self.radar_root / "_raw" / f"{self.date}.jsonl"

    def ensure(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.legacy_raw.parent.mkdir(parents=True, exist_ok=True)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/radar/test_pipeline_paths.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .gitignore radar/pipeline/__init__.py radar/pipeline/paths.py tests/radar/test_pipeline_paths.py
git commit -m "feat(radar): add pipeline path layout and gitignore"
```

---

### Task 2: Artifact models + JSON schemas

**Files:**
- Create: `radar/pipeline/models.py`
- Create: `radar/pipeline/artifacts.py`
- Create: `radar/schema/enriched_signal.schema.json`
- Create: `radar/schema/cluster.schema.json`
- Create: `radar/schema/run_meta.schema.json`
- Test: `tests/radar/test_pipeline_models.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/radar/test_pipeline_models.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.models import (
    Cluster,
    EnrichedSignal,
    RunMeta,
    enrich_signal,
    validate_signal,
)


BASE = {
    "id": "hn:1",
    "provider": "hn",
    "url": "https://example.com/a?utm_source=x",
    "title": "  Agent Skills Packaging  ",
    "ts": "2026-07-12T12:00:00Z",
}


def test_validate_signal_ok():
    s = validate_signal(BASE)
    assert s["id"] == "hn:1"


def test_validate_signal_rejects_missing_title():
    bad = {**BASE}
    del bad["title"]
    try:
        validate_signal(bad)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "title" in str(e)


def test_enrich_signal_adds_canonical_and_norm_title():
    e = enrich_signal(BASE)
    assert e["canonical_url"].startswith("https://example.com/a")
    assert "utm_source" not in e["canonical_url"]
    assert e["norm_title"] == "agent skills packaging"
    assert e["enrich_meta"]["version"] == 1


def test_cluster_and_run_meta_roundtrip():
    c = Cluster(
        cluster_id="cl_001",
        title="Agent skills",
        signal_ids=["hn:1"],
        providers=["hn"],
        scores={"signal_consensus": 1},
        weak_signal=True,
    )
    d = c.to_dict()
    assert Cluster.from_dict(d).cluster_id == "cl_001"
    meta = RunMeta(
        date="2026-07-12",
        schema_version=1,
        providers_ok=["hn"],
        providers_degraded=[],
        counts={"signals": 1, "enriched": 1, "clusters": 1, "invalid": 0},
    )
    assert RunMeta.from_dict(meta.to_dict()).date == "2026-07-12"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/radar/test_pipeline_models.py -v
```

Expected: FAIL import / missing symbols.

- [ ] **Step 3: Write minimal implementation**

`radar/pipeline/models.py` — required surface:

```python
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from radar.lib.dedupe import canonicalize_url

REQUIRED_SIGNAL = ("id", "provider", "url", "title", "ts")
ENRICH_VERSION = 1


def validate_signal(raw: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED_SIGNAL if not raw.get(k)]
    if missing:
        raise ValueError(f"invalid signal missing: {', '.join(missing)}")
    return raw


def enrich_signal(raw: dict[str, Any], *, cache_hit: bool = False) -> dict[str, Any]:
    s = validate_signal(raw)
    out = dict(s)
    out["canonical_url"] = canonicalize_url(s["url"])
    out["norm_title"] = " ".join((s.get("title") or "").lower().split())
    # Cheap heuristics: tags from provenance, title tokens as topics_hint
    provenance = s.get("provenance") or {}
    tags = provenance.get("tag_list") or provenance.get("tags") or []
    topics_hint = [str(t) for t in tags][:8]
    if not topics_hint and out["norm_title"]:
        topics_hint = [w for w in out["norm_title"].split() if len(w) > 3][:5]
    out.setdefault("entities", [])
    out["topics_hint"] = topics_hint
    out.setdefault("language", None)
    out["enrich_meta"] = {
        "version": ENRICH_VERSION,
        "cache_hit": cache_hit,
    }
    return out


@dataclass
class Cluster:
    cluster_id: str
    title: str
    signal_ids: list[str]
    providers: list[str]
    scores: dict[str, Any] = field(default_factory=dict)
    slug: str | None = None
    rationale_hint: str | None = None
    weak_signal: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Cluster:
        return cls(
            cluster_id=d["cluster_id"],
            title=d["title"],
            signal_ids=list(d.get("signal_ids") or []),
            providers=list(d.get("providers") or []),
            scores=dict(d.get("scores") or {}),
            slug=d.get("slug"),
            rationale_hint=d.get("rationale_hint"),
            weak_signal=bool(d.get("weak_signal", False)),
        )


@dataclass
class RunMeta:
    date: str
    schema_version: int
    providers_ok: list[str]
    providers_degraded: list[str]
    counts: dict[str, int]
    notes: list[str] = field(default_factory=list)
    timings_ms: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RunMeta:
        return cls(
            date=d["date"],
            schema_version=int(d.get("schema_version") or 1),
            providers_ok=list(d.get("providers_ok") or []),
            providers_degraded=list(d.get("providers_degraded") or []),
            counts=dict(d.get("counts") or {}),
            notes=list(d.get("notes") or []),
            timings_ms=dict(d.get("timings_ms") or {}),
        )
```

`radar/pipeline/artifacts.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
```

Add JSON Schema files under `radar/schema/` mirroring `EnrichedSignal`, `Cluster`, `RunMeta` required fields (draft 2020-12, same style as `signal.schema.json`).

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/radar/test_pipeline_models.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add radar/pipeline/models.py radar/pipeline/artifacts.py radar/schema/*.json tests/radar/test_pipeline_models.py
git commit -m "feat(radar): add pipeline models and artifact I/O"
```

---

### Task 3: Enrich stage (cheap + cache)

**Files:**
- Create: `radar/pipeline/enrich.py`
- Test: `tests/radar/test_pipeline_enrich.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/radar/test_pipeline_enrich.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.enrich import enrich_batch


def test_enrich_batch_dedupes_by_canonical_and_caches(tmp_path: Path):
    signals = [
        {
            "id": "a",
            "provider": "hn",
            "url": "https://x.test/p?utm_source=1",
            "title": "Hello World Tools",
            "ts": "2026-07-12T00:00:00Z",
        },
        {
            "id": "b",
            "provider": "lobsters",
            "url": "https://x.test/p",
            "title": "Hello World Tools",
            "ts": "2026-07-12T01:00:00Z",
        },
    ]
    cache = tmp_path / "enrich_cache.json"
    first = enrich_batch(signals, cache_path=cache, max_batch=100)
    assert len(first) == 1
    assert first[0]["enrich_meta"]["cache_hit"] is False
    second = enrich_batch(first, cache_path=cache, max_batch=100)
    assert second[0]["enrich_meta"]["cache_hit"] is True
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/radar/test_pipeline_enrich.py -v
```

Expected: FAIL missing `enrich_batch`.

- [ ] **Step 3: Write minimal implementation**

```python
# radar/pipeline/enrich.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from radar.lib.dedupe import canonicalize_url
from radar.pipeline.models import enrich_signal, validate_signal


def _load_cache(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_cache(path: Path | None, cache: dict[str, dict[str, Any]]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def enrich_batch(
    signals: list[dict[str, Any]],
    *,
    cache_path: Path | None = None,
    max_batch: int = 200,
) -> list[dict[str, Any]]:
    cache = _load_cache(cache_path)
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    invalid = 0
    for raw in signals[: max(0, max_batch)]:
        try:
            validate_signal(raw)
        except ValueError:
            invalid += 1
            continue
        key = canonicalize_url(raw.get("url", "")) or raw["id"]
        if key in seen:
            continue
        seen.add(key)
        if key in cache:
            row = dict(cache[key])
            row["enrich_meta"] = {**(row.get("enrich_meta") or {}), "cache_hit": True}
            out.append(row)
            continue
        row = enrich_signal(raw, cache_hit=False)
        cache[key] = row
        out.append(row)
    _save_cache(cache_path, cache)
    return out
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/radar/test_pipeline_enrich.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add radar/pipeline/enrich.py tests/radar/test_pipeline_enrich.py
git commit -m "feat(radar): add cheap enrich stage with URL cache"
```

---

### Task 4: Correlate + score stages

**Files:**
- Create: `radar/pipeline/correlate.py`
- Create: `radar/pipeline/score.py`
- Test: `tests/radar/test_pipeline_correlate.py`
- Test: `tests/radar/test_pipeline_score.py`

- [ ] **Step 1: Write failing correlate test**

```python
# tests/radar/test_pipeline_correlate.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.correlate import correlate_enriched


def test_correlate_groups_shared_topic_hint():
    enriched = [
        {
            "id": "hn:1",
            "provider": "hn",
            "url": "https://a.test/1",
            "title": "Agent skills pack",
            "ts": "2026-07-12T00:00:00Z",
            "canonical_url": "https://a.test/1",
            "norm_title": "agent skills pack",
            "topics_hint": ["agent", "skills"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
        {
            "id": "lobsters:2",
            "provider": "lobsters",
            "url": "https://b.test/2",
            "title": "Skills for agents",
            "ts": "2026-07-12T01:00:00Z",
            "canonical_url": "https://b.test/2",
            "norm_title": "skills for agents",
            "topics_hint": ["skills", "agents"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
        {
            "id": "arxiv:3",
            "provider": "arxiv",
            "url": "https://c.test/3",
            "title": "Unrelated database paper",
            "ts": "2026-07-12T02:00:00Z",
            "canonical_url": "https://c.test/3",
            "norm_title": "unrelated database paper",
            "topics_hint": ["database"],
            "entities": [],
            "enrich_meta": {"version": 1, "cache_hit": False},
        },
    ]
    clusters = correlate_enriched(enriched, max_clusters=7, topics_index=None)
    assert 1 <= len(clusters) <= 7
    multi = [c for c in clusters if len(c.providers) >= 2]
    assert multi, "expected at least one multi-provider cluster from overlapping hints"
```

- [ ] **Step 2: Run correlate test — expect FAIL**

```bash
python3 -m pytest tests/radar/test_pipeline_correlate.py -v
```

- [ ] **Step 3: Implement `correlate.py`**

```python
# radar/pipeline/correlate.py
from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from radar.pipeline.models import Cluster


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def _hint_set(row: dict[str, Any]) -> set[str]:
    hints = {str(h).lower() for h in (row.get("topics_hint") or [])}
    for w in (row.get("norm_title") or "").split():
        if len(w) > 3:
            hints.add(w)
    return hints


def correlate_enriched(
    enriched: list[dict[str, Any]],
    *,
    max_clusters: int = 12,
    topics_index: dict[str, Any] | None = None,
) -> list[Cluster]:
    # topics_index reserved for agent merge hints; cheap path uses overlap only
    _ = topics_index
    groups: list[dict[str, Any]] = []
    for row in enriched:
        hints = _hint_set(row)
        domain = _domain(row.get("canonical_url") or row.get("url") or "")
        matched = None
        for g in groups:
            if _jaccard(hints, g["hints"]) >= 0.2 or (domain and domain == g["domain"]):
                matched = g
                break
        if matched is None:
            groups.append(
                {
                    "hints": set(hints),
                    "domain": domain,
                    "rows": [row],
                }
            )
        else:
            matched["hints"] |= hints
            matched["rows"].append(row)

    groups.sort(key=lambda g: (-len({r["provider"] for r in g["rows"]}), -len(g["rows"])))
    groups = groups[: max(1, max_clusters)]

    clusters: list[Cluster] = []
    for i, g in enumerate(groups, start=1):
        rows = g["rows"]
        providers = sorted({r["provider"] for r in rows})
        title = rows[0].get("title") or " ".join(sorted(g["hints"])[:4]) or f"cluster-{i}"
        clusters.append(
            Cluster(
                cluster_id=f"cl_{i:03d}",
                title=title,
                signal_ids=[r["id"] for r in rows],
                providers=providers,
                weak_signal=len(providers) == 1 and len(rows) == 1,
            )
        )
    return clusters
```

- [ ] **Step 4: Write failing score test**

```python
# tests/radar/test_pipeline_score.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.models import Cluster
from radar.pipeline.score import apply_deterministic_scores


def test_signal_consensus_and_personal_boost():
    c = Cluster(
        cluster_id="cl_001",
        title="Agent skills",
        signal_ids=["hn:1", "lobsters:2"],
        providers=["hn", "lobsters"],
        scores={},
    )
    topics = {
        "topics": [
            {
                "slug": "agent-skills",
                "aliases": ["agent skills"],
                "hit_count": 3,
                "provider_set": ["hn", "lobsters"],
            }
        ]
    }
    personal = {"agent", "skills"}  # tokens from GA4/GSC themes
    out = apply_deterministic_scores([c], topics_index=topics, personal_tokens=personal)
    assert out[0].scores["signal_consensus"] >= 2
    assert out[0].scores.get("personal_relevance", 0) >= 1
```

- [ ] **Step 5: Implement `score.py`**

```python
# radar/pipeline/score.py
from __future__ import annotations

from typing import Any

from radar.pipeline.models import Cluster


def apply_deterministic_scores(
    clusters: list[Cluster],
    *,
    topics_index: dict[str, Any] | None = None,
    personal_tokens: set[str] | None = None,
) -> list[Cluster]:
    personal_tokens = {t.lower() for t in (personal_tokens or set())}
    topics = (topics_index or {}).get("topics") or []
    for c in clusters:
        c.scores["signal_consensus"] = len(set(c.providers))
        # recurrence from topic overlap on title tokens
        title_tokens = set(c.title.lower().split())
        hit = 0
        for t in topics:
            aliases = {a.lower() for a in (t.get("aliases") or [])}
            aliases.add((t.get("slug") or "").replace("-", " "))
            if title_tokens & aliases or title_tokens & set((t.get("title") or "").lower().split()):
                hit = max(hit, int(t.get("hit_count") or 0))
        c.scores["growth_velocity"] = hit  # cheap stand-in until richer metrics
        if personal_tokens and (title_tokens & personal_tokens):
            c.scores["personal_relevance"] = len(title_tokens & personal_tokens)
        else:
            c.scores.setdefault("personal_relevance", 0)
    return clusters


def personal_tokens_from_signals(signals: list[dict[str, Any]]) -> set[str]:
    """Extract boost tokens from ga4/search_console signals only (never required in prose)."""
    tokens: set[str] = set()
    for s in signals:
        if s.get("provider") not in {"ga4", "search_console"}:
            continue
        for part in (s.get("title") or "").lower().replace(":", " ").split():
            if len(part) > 3:
                tokens.add(part)
    return tokens
```

- [ ] **Step 6: Run tests PASS + commit**

```bash
python3 -m pytest tests/radar/test_pipeline_correlate.py tests/radar/test_pipeline_score.py -v
git add radar/pipeline/correlate.py radar/pipeline/score.py tests/radar/test_pipeline_correlate.py tests/radar/test_pipeline_score.py
git commit -m "feat(radar): add correlate and deterministic score stages"
```

---

### Task 5: Provider setup gate

**Files:**
- Create: `radar/pipeline/provider_setup.py`
- Test: `tests/radar/test_provider_setup.py`

- [ ] **Step 1: Write failing test**

```python
# tests/radar/test_provider_setup.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar.pipeline.provider_setup import check_provider_ready


def test_product_hunt_requires_token(monkeypatch):
    monkeypatch.delenv("PRODUCTHUNT_TOKEN", raising=False)
    ok, hint = check_provider_ready("product_hunt", {"enabled": True})
    assert ok is False
    assert "PRODUCTHUNT_TOKEN" in hint


def test_rss_ready_with_feeds():
    ok, hint = check_provider_ready("rss", {"enabled": True, "feeds": ["https://example.com/feed.xml"]})
    assert ok is True
    assert hint == ""


def test_youtube_api_requires_key(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    ok, hint = check_provider_ready("youtube_api", {"enabled": True, "queries": ["ai agents"]})
    assert ok is False
    assert "YOUTUBE_API_KEY" in hint
```

- [ ] **Step 2: Run — expect FAIL**

```bash
python3 -m pytest tests/radar/test_provider_setup.py -v
```

- [ ] **Step 3: Implement**

```python
# radar/pipeline/provider_setup.py
from __future__ import annotations

import os
from typing import Any


def check_provider_ready(name: str, meta: dict[str, Any]) -> tuple[bool, str]:
    if not meta.get("enabled"):
        return True, ""
    if name == "product_hunt":
        if not os.environ.get("PRODUCTHUNT_TOKEN"):
            return False, (
                "Set env PRODUCTHUNT_TOKEN (Product Hunt developer token from "
                "https://api.producthunt.com/v2/oauth/applications). Never commit the token."
            )
        return True, ""
    if name == "rss":
        feeds = meta.get("feeds") or []
        if not feeds:
            return False, "Add providers.rss.feeds: [url, ...] in journals/radar/config.yaml"
        return True, ""
    if name == "youtube_api":
        if not os.environ.get("YOUTUBE_API_KEY"):
            return False, "Set env YOUTUBE_API_KEY (Google Cloud YouTube Data API key)."
        if not (meta.get("queries") or meta.get("channel_ids")):
            return False, "Set providers.youtube_api.queries or channel_ids in config.yaml"
        return True, ""
    if name == "ga4":
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not meta.get("credentials_file"):
            return False, (
                "Set GOOGLE_APPLICATION_CREDENTIALS or providers.ga4.credentials_file "
                "to a service-account JSON (lab only)."
            )
        if not meta.get("property_id"):
            return False, "Set providers.ga4.property_id in config.yaml"
        return True, ""
    if name == "search_console":
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not meta.get("credentials_file"):
            return False, (
                "Set GOOGLE_APPLICATION_CREDENTIALS or providers.search_console.credentials_file "
                "(lab only)."
            )
        if not meta.get("site_url"):
            return False, "Set providers.search_console.site_url (e.g. https://example.com/)"
        return True, ""
    return True, ""
```

- [ ] **Step 4: PASS + commit**

```bash
python3 -m pytest tests/radar/test_provider_setup.py -v
git add radar/pipeline/provider_setup.py tests/radar/test_provider_setup.py
git commit -m "feat(radar): add provider setup readiness checks"
```

---

### Task 6: RSS provider

**Files:**
- Create: `radar/providers/rss/__init__.py`
- Create: `radar/providers/rss/fetch.py`
- Create: `radar/fixtures/rss_feed.xml`
- Test: `tests/radar/test_rss_fetch.py`

- [ ] **Step 1: Fixture + failing test**

Minimal Atom fixture with one entry. Test `parse_feed(xml_bytes) -> list[Signal]` and monkeypatched `fetch`.

```python
def test_parse_rss_fixture():
    xml = (ROOT / "radar/fixtures/rss_feed.xml").read_bytes()
    signals = rss_fetch.parse_feed(xml, feed_url="https://example.com/feed.xml")
    assert len(signals) >= 1
    assert signals[0]["provider"] == "rss"
    assert signals[0]["id"].startswith("rss:")
```

- [ ] **Step 2: Implement `fetch.py`** using `xml.etree.ElementTree` (RSS 2.0 + Atom). `fetch(feeds: list[str], limit_per_feed: int = 10)`.

- [ ] **Step 3: PASS + commit**

```bash
python3 -m pytest tests/radar/test_rss_fetch.py -v
git add radar/providers/rss radar/fixtures/rss_feed.xml tests/radar/test_rss_fetch.py
git commit -m "feat(radar): add RSS blog provider"
```

---

### Task 7: Product Hunt provider

**Files:**
- Create: `radar/providers/product_hunt/__init__.py`
- Create: `radar/providers/product_hunt/fetch.py`
- Create: `radar/fixtures/product_hunt_posts.json`
- Test: `tests/radar/test_product_hunt_fetch.py`

- [ ] **Step 1: Failing test** — `parse_posts(payload)` from GraphQL-shaped fixture (`data.posts.edges[].node` with `id`, `name`, `tagline`, `url`, `votesCount`, `createdAt`).

- [ ] **Step 2: Implement** — `fetch(token: str | None = None, limit: int = 20)` reads `PRODUCTHUNT_TOKEN`, POSTs to `https://api.producthunt.com/v2/api/graphql` with a minimal posts query; `get_json`/`post_graphql` injectable for tests. Raise `RuntimeError` if token missing (caller treats as degrade).

- [ ] **Step 3: PASS + commit**

```bash
python3 -m pytest tests/radar/test_product_hunt_fetch.py -v
git commit -m "feat(radar): add Product Hunt GraphQL provider"
```

---

### Task 8: YouTube Data API provider

**Files:**
- Create: `radar/providers/youtube_api/__init__.py`
- Create: `radar/providers/youtube_api/fetch.py`
- Create: `radar/fixtures/youtube_api_search.json`
- Test: `tests/radar/test_youtube_api_fetch.py`

- [ ] **Step 1: Failing test** — parse search.list fixture → signals with `provider: youtube_api`, shallow fields only (no transcripts).

- [ ] **Step 2: Implement** — `fetch(api_key=None, queries=None, channel_ids=None, max_results=5)` using `https://www.googleapis.com/youtube/v3/search`. Missing key → raise. Quota errors → raise (degrade upstream).

- [ ] **Step 3: PASS + commit**

```bash
python3 -m pytest tests/radar/test_youtube_api_fetch.py -v
git commit -m "feat(radar): add YouTube Data API provider"
```

---

### Task 9: GA4 + Search Console providers (personal boost)

**Files:**
- Create: `radar/providers/ga4/...`
- Create: `radar/providers/search_console/...`
- Fixtures: `ga4_report.json`, `gsc_query.json`
- Tests: `test_ga4_fetch.py`, `test_search_console_fetch.py`

**Design constraint in tests and docs:** titles may look like `GA4 rising page theme: <token>` / `GSC rising query: <token>` for private lab ranking only; synthesize prompt must not paste raw traffic numbers into promotable text.

- [ ] **Step 1: GA4 failing test** — parse runReport-shaped fixture → ≤ N signals; `provider == "ga4"`; metrics may include `sessions` but synthesize rules ban leaking them.

- [ ] **Step 2: Implement GA4 fetch** — Prefer **file export path** for v1 of this patch to avoid shipping a full Google client:

```python
def fetch(property_id: str = "", credentials_file: str = "", export_path: str = "", limit: int = 20) -> list[dict]:
    """If export_path set, parse local JSON (lab). Else attempt Analytics Data API REST with access token from env GA4_ACCESS_TOKEN (optional)."""
```

For CI: only `export_path` / fixture parse is required. Live API path: if no token/export → raise with setup hint message.

- [ ] **Step 3: GSC same pattern** — `export_path` or Search Console API; fixture parse required in CI.

- [ ] **Step 4: PASS both + commit**

```bash
python3 -m pytest tests/radar/test_ga4_fetch.py tests/radar/test_search_console_fetch.py -v
git commit -m "feat(radar): add GA4 and Search Console providers for personal boost"
```

---

### Task 10: Wire fetch_enabled + config gate + config.example

**Files:**
- Modify: `radar/providers/fetch_enabled.py`
- Modify: `templates/radar/config.example.yaml`
- Modify: `tests/radar/test_fetch_enabled.py`

- [ ] **Step 1: Extend tests**

1. Enabled `rss` with feeds + monkeypatched fetch writes signals.
2. Enabled `product_hunt` without token → degraded (0 signals) and exit 0.
3. Unknown provider still skipped.

Update `fetch_all` to:

```python
from radar.pipeline.provider_setup import check_provider_ready

# before fetch:
ok, hint = check_provider_ready(name, meta)
if not ok:
    print(f"{name}: degraded (setup: {hint})", file=sys.stderr)
    counts[name] = 0
    continue
```

Register fetchers:

| name | kwargs from meta |
|------|------------------|
| `product_hunt` | `limit` |
| `rss` | `feeds`, `limit_per_feed` |
| `youtube_api` | `queries`, `channel_ids`, `max_results` |
| `ga4` | `property_id`, `credentials_file`, `export_path`, `limit` |
| `search_console` | `site_url`, `credentials_file`, `export_path`, `limit` |

- [ ] **Step 2: Extend `config.example.yaml`**

```yaml
defaults:
  watch_days: 7
  ignore_suppress_days: 3
  max_opportunities: 7
  max_signals_per_enrich_batch: 200
  max_clusters: 12

providers:
  # ... existing ...
  product_hunt:
    enabled: false
    limit: 20
  rss:
    enabled: false
    feeds: []
    limit_per_feed: 10
  youtube_api:
    enabled: false
    queries: []
    channel_ids: []
    max_results: 5
  ga4:
    enabled: false
    property_id: ""
    credentials_file: ""
    export_path: ""  # lab JSON export for offline/CI-friendly runs
    limit: 20
  search_console:
    enabled: false
    site_url: ""
    credentials_file: ""
    export_path: ""
    limit: 20
```

- [ ] **Step 3: PASS + commit**

```bash
python3 -m pytest tests/radar/test_fetch_enabled.py -v
git commit -m "feat(radar): register new providers with setup-aware degrade"
```

---

### Task 11: `run_stages` agent entrypoint

**Files:**
- Create: `radar/pipeline/run_stages.py`
- Test: `tests/radar/test_run_stages.py`

- [ ] **Step 1: Failing test** — with tmp radar root + monkeypatched `fetch_all`, running `--stage ingest` writes `signals.jsonl`, `run_meta.json`, and legacy `_raw` copy; `--stage enrich` reads signals → enriched; `--stage correlate` writes clusters with scores.

- [ ] **Step 2: Implement CLI**

```bash
python radar/pipeline/run_stages.py \
  --config journals/radar/config.yaml \
  --radar-root journals/radar \
  --date 2026-07-12 \
  --stage all
```

Stages: `ingest` | `enrich` | `correlate` | `score` | `all`  
(`synthesize` and Obsidian export remain agent-owned per skill; optional `--stage synthesize` may only print path to template + clusters for the agent.)

`ingest` must:

1. `fetch_all`
2. write `signals.jsonl` + copy to `legacy_raw`
3. write/update `run_meta.json` with providers_ok / providers_degraded from stderr-equivalent tracking — refactor `fetch_all` to return `(signals, counts, degraded: list[str])` if needed.

- [ ] **Step 3: PASS + commit**

```bash
python3 -m pytest tests/radar/test_run_stages.py -v
git commit -m "feat(radar): add run_stages pipeline entrypoint for agents"
```

---

### Task 12: Stage prompts + skill supervisor update

**Files:**
- Create: `contracts/prompts/enrich.md`, `correlate.md`, `score.md`, `synthesize.md`, `configure-provider.md`
- Modify: `skills/leverage-radar/SKILL.md`
- Sync: `.cursor/skills/leverage-radar/SKILL.md`, `.claude/skills/leverage-radar/SKILL.md`

- [ ] **Step 1: Write prompt stubs** (short, actionable)

Each file states: input artifact path, output expectations, token caps, bans (no vendor LLM APIs from repo tools).

`configure-provider.md`: one-provider-at-a-time checklist; call `check_provider_ready`; dry-run `run_stages --stage ingest` with only that provider enabled.

- [ ] **Step 2: Rewrite skill workflow**

Triggers add: `trend radar`, `configure radar providers`, `run radar stage`.

Workflow:

1. Config bootstrap (unchanged)
2. Topic bootstrap (unchanged)
3. **Ingest:** `python radar/pipeline/run_stages.py --stage ingest ...`
4. **Enrich:** `--stage enrich`
5. **Correlate+score:** `--stage correlate` (includes deterministic score)
6. **Session LLM:** read `clusters.json` + `topics.yaml` only (not full raw if avoidable); semantic merge/refine ≤ `max_opportunities`; write daily note answering leverage questions; dual-write topics
7. Note degraded from `run_meta.json` in Executive Summary
8. **Setup assist** subsection when providers degraded for missing setup

Keep HITL Decide table. Keep bans.

- [ ] **Step 3: Sync three skill copies** (content identical for workflow sections)

- [ ] **Step 4: Commit**

```bash
git add contracts/prompts skills/leverage-radar/SKILL.md .cursor/skills/leverage-radar/SKILL.md .claude/skills/leverage-radar/SKILL.md
git commit -m "docs(radar): supervisor skill for pipeline stages and setup assist"
```

---

### Task 13: Docs + smoke template checks

**Files:**
- Modify: `docs/radar/protocol.md`, `providers.md`, `scoring.md`, `using-agents.md`
- Modify: `tests/radar/test_smoke_daily_render.py` (optional assert for leverage questions listed in skill/docs — or keep template sections unchanged and assert protocol mentions `_pipeline/`)

- [ ] **Step 1: Update protocol data-flow diagram** to `_pipeline/` stages; link new providers; document personal boost rule; document setup assist.

- [ ] **Step 2: Update providers.md** connect steps for Product Hunt, RSS, YouTube API, GA4, GSC (secrets via env; never commit).

- [ ] **Step 3: Update scoring.md** — deterministic fields from Python vs session judgement; `personal_relevance` boost-only.

- [ ] **Step 4: Smoke / docs test** — add `tests/radar/test_pipeline_docs.py` that reads `docs/radar/protocol.md` and asserts `_pipeline/` and `run_stages` appear (lightweight regression).

- [ ] **Step 5: Run full radar test suite + commit**

```bash
python3 -m pytest tests/radar -q
git add docs/radar tests/radar/test_pipeline_docs.py tests/radar/test_smoke_daily_render.py
git commit -m "docs(radar): document Trend Radar pipeline stages and providers"
```

---

## Self-review (plan vs spec)

| Spec requirement | Task(s) |
|------------------|---------|
| Auditable `_pipeline/` artifacts | 1, 2, 11 |
| Stages invocable in isolation | 11, 12 |
| Enrich / correlate / score Python helpers | 3, 4 |
| Product Hunt, RSS, YouTube API, GA4, GSC | 6–10 |
| GA4/GSC personal_relevance boost only | 4, 9, 12, 13 |
| Agent-assisted provider setup | 5, 12 |
| Degrade without aborting daily | 5, 10, 11 |
| No Dagster / no LLM SDKs / no UI email | Hard rules + skill bans |
| Obsidian dual-write preserved | Skill task 12 (v2 behavior retained) |
| Legacy `_raw` compatibility | 1, 11 |
| Docs / skill updates | 12, 13 |

**Deferred (explicit):** LangGraph, multi-model routing, GraphRAG, transcripts, newsletter notify, Dagster.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-12-trend-radar-pipelines.md`. Two execution options:

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
