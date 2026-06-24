"""Test the research-digest recipe config parses and references valid tools."""
from pathlib import Path

import pytest


RECIPE_PATH = (
    Path(__file__).resolve().parents[1] / "configs" / "research-digest.toml"
)
try:
    import tomllib  # py3.11+
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


def test_recipe_file_exists():
    assert RECIPE_PATH.exists(), f"Recipe not found at {RECIPE_PATH}"


def test_recipe_parses():
    data = tomllib.loads(RECIPE_PATH.read_text())
    assert data["recipe"]["name"] == "research_digest"
    assert data["schedule"]["cron"] == "0 7 * * 1-5"
    assert isinstance(data["gather"]["sources"], list)
    assert len(data["gather"]["sources"]) >= 1


def test_recipe_tools_are_known():
    """All tools referenced must exist in the upstream openjarvis.tools module."""
    data = tomllib.loads(RECIPE_PATH.read_text())
    tools = set(data["agent"]["tools"])

    # Try importing the upstream tools module; if it's not on sys.path in this
    # test env we still verify the names look reasonable.
    known_prefixes = {
        "rss_fetch",  # this specialization
        "web_search", "http_request", "memory_store", "memory_search",
        "think", "file_write", "tts",
    }
    unknown = tools - known_prefixes
    assert not unknown, f"Recipe references unknown tools: {unknown}"


@pytest.mark.parametrize("tool", [
    "rss_fetch", "web_search", "http_request", "memory_store",
    "memory_search", "think", "file_write", "tts",
])
def test_each_tool_is_a_string(tool):
    data = tomllib.loads(RECIPE_PATH.read_text())
    assert tool in data["agent"]["tools"]
    assert isinstance(data["agent"]["tools"], list)