"""Robustness tests for the RSS fetcher."""
import sys
from pathlib import Path

# Make the specialization's src/ package importable.
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC.parent) not in sys.path:
    sys.path.insert(0, str(_SRC.parent))

from src.tools import rss


SAMPLE_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Sample</title>
  <item>
    <title>First post</title>
    <link>https://example.com/first</link>
    <pubDate>Mon, 23 Jun 2026 10:00:00 +0000</pubDate>
    <description>Hello world</description>
  </item>
  <item>
    <title>No link post</title>
    <!-- missing link, must be skipped, not crash -->
    <pubDate>Mon, 23 Jun 2026 11:00:00 +0000</pubDate>
  </item>
  <item>
    <title>Garbage pubDate post</title>
    <link>https://example.com/garbage-date</link>
    <pubDate>not a date</pubDate>
  </item>
</channel></rss>"""


SAMPLE_ATOM = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Sample Atom</title>
  <entry>
    <title>Atom post</title>
    <link href="https://example.com/atom-1"/>
    <updated>2026-06-23T12:00:00Z</updated>
    <summary>An Atom entry.</summary>
  </entry>
</feed>"""


SAMPLE_MALFORMED = b"<?xml version='1.0'?><rss><channel><item><title>oops"


def test_parses_valid_rss(monkeypatch):
    monkeypatch.setattr(rss, "_fetch", lambda url: SAMPLE_RSS)
    items = rss.fetch_feed("https://example.com/feed")
    # Two items: the "no link" one is dropped, the "garbage date" survives.
    assert len(items) == 2
    assert items[0].title == "First post"
    assert items[0].link == "https://example.com/first"
    assert items[0].published is not None
    assert items[0].published.year == 2026
    assert items[1].link == "https://example.com/garbage-date"
    assert items[1].published is None  # unparseable date → None, not crash


def test_parses_atom(monkeypatch):
    monkeypatch.setattr(rss, "_fetch", lambda url: SAMPLE_ATOM)
    items = rss.fetch_feed("https://example.com/atom")
    assert len(items) == 1
    assert items[0].link == "https://example.com/atom-1"
    assert items[0].title == "Atom post"


def test_malformed_returns_empty(monkeypatch, caplog):
    monkeypatch.setattr(rss, "_fetch", lambda url: SAMPLE_MALFORMED)
    items = rss.fetch_feed("https://example.com/broken")
    assert items == []


def test_fetch_failure_returns_empty(monkeypatch, caplog):
    def boom(url):
        raise OSError("simulated")
    monkeypatch.setattr(rss, "_fetch", boom)
    items = rss.fetch_feed("https://example.com/down")
    assert items == []