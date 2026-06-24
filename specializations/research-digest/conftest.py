# Rootdir conftest for the research-digest specialization.
# Ensures `src.tools.rss`, `src.agents.research_digest`, etc. are importable
# from any test under tests/ without needing the package to be installed.
import sys
from pathlib import Path

_SPEC_ROOT = Path(__file__).resolve().parent
_SRC_PARENT = _SPEC_ROOT / "src"
if str(_SPEC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SPEC_ROOT))