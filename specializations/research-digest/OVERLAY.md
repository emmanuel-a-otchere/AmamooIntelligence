# Overlay — research-digest

> Every file this specialization adds or modifies on top of AmamooIntelligence base.

## Added files

| Path | Purpose | Base reference |
| --- | --- | --- |
| `use-cases/research-digest/SPEC.md` | Use-case spec | (no equivalent) |
| `use-cases/research-digest/OVERLAY.md` | This file | (no equivalent) |
| `use-cases/research-digest/README.md` | Quick start for this specialization | (no equivalent) |
| `use-cases/research-digest/tests/test_recipe_loads.py` | Recipe parse smoke test | `tests/` |
| `use-cases/research-digest/tests/test_rss_fetch.py` | RSS parser robustness | `tests/tools/` |
| `use-cases/research-digest/tests/test_url_sanity.py` | Catches fabricated URLs in briefings | (no equivalent — research-digest specific) |
| `use-cases/research-digest/configs/research-digest.toml` | Recipe config | `configs/openjarvis/recipes/` |
| `use-cases/research-digest/src/agents/research_digest.py` | Stateful scheduled agent | `src/openjarvis/agents/` |
| `use-cases/research-digest/src/tools/rss.py` | RSS/Atom fetcher | `src/openjarvis/tools/` |
| `use-cases/research-digest/docs/SOURCES.md` | Per-deployment source list docs | `docs/` |

## Modified files

| Path | Change | Reason |
| --- | --- | --- |
| `use-cases/README.md` | Added link to this specialization | Discovery |

## Reused unchanged from base

- `src/openjarvis/templates/data/deep-researcher.toml` — used as the deep-research agent template inside the recipe
- `src/openjarvis/tools/tts.py` — used for the optional audio briefing
- `src/openjarvis/tools/web_search.py`, `http_request.py` — used by the gather and citation steps
- All of `src/openjarvis/core/` — the agent loop is reused as-is

## Files this overlay deliberately does **not** touch

- Anything in `src/openjarvis/core/` — base is the source of truth for the loop
- Other use-cases in `use-cases/` — each specialization is independent
- `desktop/`, `frontend/`, `rust/` — UI is base-owned

## Rebase expectations

When base `main` advances, the most likely conflict surfaces are:

1. `use-cases/README.md` — both base and this overlay add a line. Resolve by keeping both (base's scaffold + this specialization's entry).
2. `src/openjarvis/agents/` — only if base adds an agent with a conflicting filename. Current agent files use `morning_digest.py` and friends; `research_digest.py` should remain unique.

Run `pytest use-cases/research-digest/tests/` after every rebase.