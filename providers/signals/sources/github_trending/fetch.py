from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://github.com/trending"
VALID_SINCE = frozenset({"daily", "weekly", "monthly"})
# ponytail: HTML layout drifts; agents may WebFetch https://github.com/trending?since=daily as fallback.


class _TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.repos: list[dict[str, str]] = []
        self._in_article = False
        self._in_h2 = False
        self._in_link = False
        self._in_desc = False
        self._href = ""
        self._title_parts: list[str] = []
        self._desc_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        cls = attrs_d.get("class", "")

        if tag == "article" and "Box-row" in cls:
            self._in_article = True
            self._href = ""
            self._title_parts = []
            self._desc_parts = []
            return

        if not self._in_article:
            return

        if tag == "h2":
            self._in_h2 = True
        elif tag == "a" and self._in_h2 and not self._href:
            href = attrs_d.get("href", "")
            if re.fullmatch(r"/[^/]+/[^/]+", href):
                self._in_link = True
                self._href = href
        elif tag == "p" and self._href and not self._desc_parts and not self._in_desc:
            self._in_desc = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_link:
            self._in_link = False
            self._in_h2 = False
        elif tag == "p" and self._in_desc:
            self._in_desc = False
        elif tag == "article" and self._in_article:
            if self._href:
                self.repos.append(
                    {
                        "href": self._href,
                        "title": " ".join(self._title_parts).strip(),
                        "text": " ".join(self._desc_parts).strip(),
                    }
                )
            self._in_article = False
            self._in_h2 = False
            self._in_link = False
            self._in_desc = False

    def handle_data(self, data: str) -> None:
        chunk = data.strip()
        if not chunk:
            return
        if self._in_link:
            self._title_parts.append(chunk)
        elif self._in_desc:
            self._desc_parts.append(chunk)


def parse_html(html: str) -> list[dict]:
    parser = _TrendingParser()
    parser.feed(html)
    ts = datetime.now(timezone.utc).isoformat()
    out: list[dict] = []
    for repo in parser.repos:
        href = repo["href"]
        slug = href.lstrip("/")
        owner = slug.split("/", 1)[0]
        out.append(
            {
                "id": f"github_trending:{slug}",
                "provider": "github_trending",
                "url": f"https://github.com/{slug}",
                "title": repo["title"] or slug.replace("/", " / "),
                "ts": ts,
                "author": owner,
                "text": repo["text"] or None,
                "metrics": {},
                "provenance": {"repo": slug, "since": None},
            }
        )
    return out


def get_page(url: str) -> str:
    req = Request(url, headers={"User-Agent": "ai-knowledge-os-radar/0.1"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def fetch(since: str = "daily") -> list[dict]:
    if since not in VALID_SINCE:
        raise ValueError(f"since must be one of {sorted(VALID_SINCE)}")
    url = f"{BASE}?since={since}"
    signals = parse_html(get_page(url))
    for signal in signals:
        signal["provenance"]["since"] = since
    return signals


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="github-trending-fetch")
    p.add_argument("--since", choices=sorted(VALID_SINCE), default="daily")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    signals = fetch(since=args.since)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for s in signals:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"wrote {len(signals)} github_trending signals → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
