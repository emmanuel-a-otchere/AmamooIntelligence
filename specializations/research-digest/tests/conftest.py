# conftest for the research-digest specialization.
# Adds the specialization's src/ tree to sys.path so test files can
# `import rss`, `import agents.research_digest`, etc.
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))