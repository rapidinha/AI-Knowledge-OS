from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

ATOM_NS = "http://www.w3.org/2005/Atom"
DC_NS = "http://purl.org/dc/elements/1.1/"
UA = "ai-knowledge-os-radar/0.1"


def _ns(tag: str, ns: str = ATOM_NS) -> str:
    return f"{{{ns}}}{tag}"


def _signal_id(guid_or_key: str, url: str, title: str) -> str:
    key = (guid_or_key or "").strip()
    if key:
        return f"rss:{key}"
    raw = f"{url}|{title}".encode("utf-8")
    return f"rss:{hashlib.sha256(raw).hexdigest()[:16]}"


def _atom_link(entry: ET.Element) -> str:
    for link in entry.findall(_ns("link")):
        rel = link.get("rel")
        if rel in (None, "alternate"):
            href = link.get("href") or ""
            if href:
                return href
    return ""


def _parse_atom_entries(root: ET.Element, feed_url: str) -> list[dict]:
    out: list[dict] = []
    for entry in root.findall(_ns("entry")):
        entry_id = (entry.findtext(_ns("id"), default="") or "").strip()
        url = _atom_link(entry)
        title = (entry.findtext(_ns("title"), default="") or "").strip()
        ts = (
            entry.findtext(_ns("published"), default="")
            or entry.findtext(_ns("updated"), default="")
            or ""
        )
        author = entry.findtext(f"{_ns('author')}/{_ns('name')}") or None
        text = entry.findtext(_ns("summary"), default="") or entry.findtext(_ns("content"), default="")
        text = (text or "").strip() or None
        out.append(
            {
                "id": _signal_id(entry_id, url, title),
                "provider": "rss",
                "url": url,
                "title": title,
                "ts": ts,
                "author": author,
                "text": text,
                "metrics": {},
                "provenance": {"feed_url": feed_url},
            }
        )
    return out


def _parse_rss_items(root: ET.Element, feed_url: str) -> list[dict]:
    channel = root.find("channel")
    if channel is None:
        return []
    out: list[dict] = []
    for item in channel.findall("item"):
        guid_el = item.find("guid")
        guid = (guid_el.text if guid_el is not None and guid_el.text else "") or ""
        url = (item.findtext("link", default="") or "").strip()
        title = (item.findtext("title", default="") or "").strip()
        ts = item.findtext("pubDate", default="") or ""
        author = (
            item.findtext("author", default="")
            or item.findtext(f"{{{DC_NS}}}creator", default="")
            or None
        )
        text = item.findtext("description", default="")
        text = (text or "").strip() or None
        out.append(
            {
                "id": _signal_id(guid, url, title),
                "provider": "rss",
                "url": url,
                "title": title,
                "ts": ts,
                "author": author,
                "text": text,
                "metrics": {},
                "provenance": {"feed_url": feed_url},
            }
        )
    return out


def parse_feed(xml_bytes: bytes, feed_url: str = "") -> list[dict]:
    root = ET.fromstring(xml_bytes)
    tag = root.tag.rsplit("}", 1)[-1]
    if tag == "feed":
        return _parse_atom_entries(root, feed_url)
    if tag == "rss":
        return _parse_rss_items(root, feed_url)
    return []


def get_feed(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read()


def fetch(feeds: list[str], limit_per_feed: int = 10) -> list[dict]:
    out: list[dict] = []
    limit = max(0, limit_per_feed)
    for feed in feeds:
        if not feed:
            continue
        try:
            xml_bytes = get_feed(feed)
            signals = parse_feed(xml_bytes, feed_url=feed)
            out.extend(signals[:limit])
        except Exception:
            continue
    return out
