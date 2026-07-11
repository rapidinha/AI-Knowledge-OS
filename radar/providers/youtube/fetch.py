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
