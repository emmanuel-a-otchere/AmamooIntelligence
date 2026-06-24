"""Sanity test: every URL in a sample briefing must return 2xx.

This is the test that catches LLM-hallucinated citations in real digests.
The 'sample briefing' here is a fixture; in production this test runs
against the most recent output of the orchestrator.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

import pytest


URL_RE = re.compile(r"https?://[^\s)\]<>\"']+")


def extract_urls(markdown: str) -> list[str]:
    # Strip trailing punctuation common in Markdown links.
    return [u.rstrip(".,;:!?") for u in URL_RE.findall(markdown)]


@pytest.fixture(scope="module")
def sample_briefing() -> str:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "sample_briefing.md"
    if not fixture.exists():
        pytest.skip(f"No fixture at {fixture}")
    return fixture.read_text()


@pytest.mark.network
def test_every_url_returns_2xx(sample_briefing: str) -> None:
    urls = extract_urls(sample_briefing)
    assert urls, "Sample briefing contains no URLs — fixture may be empty"

    failures: list[tuple[str, str]] = []
    for url in urls:
        try:
            req = Request(url, method="HEAD", headers={"User-Agent": "research-digest-tests/0.1"})
            with urlopen(req, timeout=10) as resp:  # noqa: S310
                code = resp.status
        except HTTPError as exc:
            code = exc.code
        except (URLError, TimeoutError) as exc:
            failures.append((url, f"network: {exc}"))
            continue
        if not (200 <= code < 300):
            failures.append((url, f"HTTP {code}"))

    assert not failures, "Broken URLs in briefing:\n" + "\n".join(f"  {u}  →  {why}" for u, why in failures)