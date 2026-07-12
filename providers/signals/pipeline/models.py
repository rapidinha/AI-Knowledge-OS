from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from providers.signals.lib.dedupe import canonicalize_url

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
