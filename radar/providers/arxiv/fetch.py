from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "http://export.arxiv.org/api/query"
ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"
DEFAULT_CATEGORIES = ["cs.AI", "cs.SE"]


def _ns(tag: str, ns: str = ATOM_NS) -> str:
    return f"{{{ns}}}{tag}"


def build_query_url(categories: list[str], max_results: int, start: int = 0) -> str:
    search_query = "+OR+".join(f"cat:{cat}" for cat in categories)
    params = urlencode({"search_query": search_query, "start": start, "max_results": max_results})
    return f"{BASE}?{params}"


def _arxiv_id_from_entry(entry: ET.Element) -> str:
    for link in entry.findall(_ns("link")):
        if link.get("rel") == "alternate" and link.get("type") == "text/html":
            href = link.get("href", "")
            m = re.search(r"arxiv\.org/abs/([^/]+)", href)
            if m:
                return re.sub(r"v\d+$", "", m.group(1))
    entry_id = entry.findtext(_ns("id"), default="")
    m = re.search(r"arxiv\.org/abs/([^/]+)", entry_id)
    if m:
        return re.sub(r"v\d+$", "", m.group(1))
    return entry_id.rsplit("/", 1)[-1]


def _entry_url(arxiv_id: str) -> str:
    return f"http://arxiv.org/abs/{arxiv_id}"


def parse_atom(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out: list[dict] = []
    for entry in root.findall(_ns("entry")):
        arxiv_id = _arxiv_id_from_entry(entry)
        authors = [a.findtext(_ns("name"), default="") for a in entry.findall(_ns("author"))]
        author = ", ".join(a for a in authors if a) or None
        primary = entry.find(f"{{{ARXIV_NS}}}primary_category")
        category = primary.get("term") if primary is not None else None
        out.append(
            {
                "id": f"arxiv:{arxiv_id}",
                "provider": "arxiv",
                "url": _entry_url(arxiv_id),
                "title": (entry.findtext(_ns("title"), default="") or "").strip(),
                "ts": entry.findtext(_ns("published"), default=""),
                "author": author,
                "text": None,
                "metrics": {},
                "provenance": {"arxiv_id": arxiv_id, "primary_category": category},
            }
        )
    return out


def get_feed(url: str) -> str:
    req = Request(url, headers={"User-Agent": "ai-knowledge-os-radar/0.1"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def fetch(categories: list[str] | None = None, max_results: int = 10) -> list[dict]:
    cats = categories or DEFAULT_CATEGORIES
    url = build_query_url(cats, max_results)
    return parse_atom(get_feed(url))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="arxiv-fetch")
    p.add_argument("--categories", default=",".join(DEFAULT_CATEGORIES), help="Comma-separated arXiv categories")
    p.add_argument("--max-results", type=int, default=10)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    signals = fetch(categories=categories, max_results=args.max_results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} arxiv signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
