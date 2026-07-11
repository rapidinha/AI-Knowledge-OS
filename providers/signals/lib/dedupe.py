from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


_TRACKING = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid"}


def canonicalize_url(url: str) -> str:
    p = urlparse(url.strip())
    query = [
        (k, v)
        for k, v in parse_qsl(p.query, keep_blank_values=True)
        if k.lower() not in _TRACKING
    ]
    path = p.path.rstrip("/") or "/"
    clean = p._replace(
        scheme=p.scheme.lower(),
        netloc=p.netloc.lower(),
        path=path,
        query=urlencode(query),
        fragment="",
    )
    return urlunparse(clean)


def dedupe_signals(signals: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for s in signals:
        key = canonicalize_url(s.get("url", ""))
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out
