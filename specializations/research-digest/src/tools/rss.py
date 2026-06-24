"""Minimal RSS / Atom feed fetcher for the research-digest specialization.

This is intentionally narrow: it parses the common subset of RSS 2.0 and
Atom 1.0 that real-world feeds use, returns a flat list of items, and
fails soft (logs + returns empty) on malformed entries so a single bad
source doesn't kill the whole digest.

If this tool proves generally useful it should be promoted back to
`src/openjarvis/tools/rss.py` in AmamooIntelligence base.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)

_TIMEOUT_SECONDS = 15
_MAX_BYTES = 2_000_000  # 2 MB hard cap per feed


@dataclass
class FeedItem:
    title: str
    link: str
    published: datetime | None
    summary: str
    source: str  # feed URL, for traceability

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "published": self.published.isoformat() if self.published else None,
            "summary": self.summary,
            "source": self.source,
        }


def _fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "research-digest/0.1 (+amamoo)"})
    with urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:  # noqa: S310 — URL is operator-configured
        data = resp.read(_MAX_BYTES + 1)
        if len(data) > _MAX_BYTES:
            raise ValueError(f"Feed {url!r} exceeded {_MAX_BYTES} bytes")
        return data


def _parse_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    # RSS uses RFC 822, Atom uses ISO 8601. Try both, give up gracefully.
    for parser in (
        lambda s: datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %z"),
        lambda s: datetime.strptime(s, "%a, %d %b %Y %H:%M:%S GMT"),
        datetime.fromisoformat,
    ):
        try:
            return parser(text)
        except (ValueError, TypeError):
            continue
    return None


def _text(el: ET.Element | None) -> str:
    return (el.text or "").strip() if el is not None else ""


def fetch_feed(url: str) -> list[FeedItem]:
    """Fetch and parse one feed. Returns [] on any failure (logged)."""
    try:
        raw = _fetch(url)
    except (URLError, HTTPError, TimeoutError, OSError, ValueError) as exc:
        logger.warning("Feed fetch failed for %s: %s", url, exc)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        logger.warning("Feed parse failed for %s: %s", url, exc)
        return []

    items: list[FeedItem] = []

    # RSS 2.0: <rss><channel><item>
    for item in root.iter("item"):
        try:
            link = _text(item.find("link"))
            if not link:
                continue
            items.append(
                FeedItem(
                    title=_text(item.find("title")) or "(untitled)",
                    link=link,
                    published=_parse_dt(_text(item.find("pubDate"))),
                    summary=_text(item.find("description")),
                    source=url,
                )
            )
        except Exception as exc:  # noqa: BLE001 — one bad item must not kill the feed
            logger.warning("Bad RSS item in %s: %s", url, exc)

    # Atom 1.0: <feed xmlns="..."><entry>. The default namespace means
    # tag names carry a Clark notation prefix; ET strips it on .iter()
    # when the root declares it. Look for {ns}entry with a plain fallback.
    atom_entries = list(root.iter("{http://www.w3.org/2005/Atom}entry")) or list(
        root.iter("entry")
    )
    NS = "{http://www.w3.org/2005/Atom}"
    for entry in atom_entries:
        try:
            # NB: don't use `or` to merge the two find() calls — Element's
            # __bool__ reports child count, so an empty <link/> is falsy
            # and `or` would silently drop a real element.
            link_el = entry.find(f"{NS}link")
            if link_el is None:
                link_el = entry.find("link")
            href = link_el.get("href") if link_el is not None else ""
            if not href:
                continue
            title_el = entry.find(f"{NS}title")
            if title_el is None:
                title_el = entry.find("title")
            updated_el = entry.find(f"{NS}updated")
            if updated_el is None:
                updated_el = entry.find("updated")
            published_el = entry.find(f"{NS}published")
            if published_el is None:
                published_el = entry.find("published")
            summary_el = entry.find(f"{NS}summary")
            if summary_el is None:
                summary_el = entry.find("summary")
            content_el = entry.find(f"{NS}content")
            if content_el is None:
                content_el = entry.find("content")
            items.append(
                FeedItem(
                    title=_text(title_el) or "(untitled)",
                    link=href,
                    published=_parse_dt(_text(updated_el) or _text(published_el)),
                    summary=_text(summary_el) or _text(content_el),
                    source=url,
                )
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Bad Atom entry in %s: %s", url, exc)

    return items