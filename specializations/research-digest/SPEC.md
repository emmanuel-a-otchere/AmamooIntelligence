# Use Case: research-digest

> A scheduled, multi-source research digest that combines daily news intake with deeper topical research runs, delivered as a written briefing plus optional audio.

## Goal

Produce a daily morning briefing that:

1. Pulls fresh items from configured RSS / web sources (news, blogs, arXiv).
2. Identifies 2-4 themes worth deeper research for the day.
3. Runs short deep-research passes on each theme using the upstream `deep-researcher` template as the agent backbone.
4. Synthesizes everything into a single written briefing (Markdown) and optionally speaks it via TTS.

The general AmamooIntelligence ships the *primitives* for each step (scheduled agents, deep researcher template, TTS). This specialization is the **layered recipe** that ties them into a workflow the general framework doesn't ship out-of-the-box.

## Success criteria

- [ ] Briefing delivered every weekday morning at 07:00 local time (configured per-deployment).
- [ ] Cites ≥3 sources per theme (real URLs, not placeholders).
- [ ] Cites at least one arXiv paper per science-themed briefing.
- [ ] Total runtime ≤ 10 minutes on a single Ollama + 8B-qwen3 box.
- [ ] Audio version (TTS) under 8 minutes long.
- [ ] Markdown briefing passes basic factual sanity: no fabricated URLs (test asserts every cited URL returns 2xx).

## What stays general

Inherited unmodified from AmamooIntelligence base:

- `src/openjarvis/core/` — agent loop
- `src/openjarvis/templates/data/deep-researcher.toml` — used as a building block, not modified
- `src/openjarvis/templates/data/morning-digest-*.toml` — used as inspiration, not modified
- `src/openjarvis/tools/web_search.py`, `src/openjarvis/tools/http_request.py`, `src/openjarvis/tools/tts.py` — reused as-is
- All 8 built-in agents — this specialization does not add new agent types

## What this specialization changes

| Path | Change | Rationale |
| --- | --- | --- |
| `configs/openjarvis/recipes/research-digest.toml` | New recipe | Defines the orchestrated workflow: gather → cluster → deep-research → synthesize → speak |
| `src/openjarvis/agents/research_digest.py` | New agent | Stateful scheduled agent that owns the workflow |
| `src/openjarvis/tools/rss.py` | New tool | RSS/Atom feed fetch (general-purpose, will be promoted back to base) |
| `use-cases/research-digest/` | This folder | Scaffold + tests + samples |
| `docs/SOURCES.md` | New doc | How to configure the source list per-deployment |

## Sync strategy

- **Rebase weekly** onto `base/main` (AmamooIntelligence). Linear history keeps `OVERLAY.md` diffs trivial.
- After each rebase, run `pytest use-cases/research-digest/tests/` to confirm nothing upstream broke the recipe.

## Tests

- Base suite must pass: `uv run pytest tests/`
- Specialization tests: `uv run pytest use-cases/research-digest/tests/`
  - `test_rss_fetch.py` — feed parser handles malformed entries without crashing
  - `test_url_sanity.py` — every URL in a sample briefing returns 2xx (catches LLM hallucination)
  - `test_recipe_loads.py` — the `research-digest.toml` recipe parses and references only available tools/agents
- Acceptance test (manual, weekly): produce a briefing on a known topic and verify all four success criteria above.

## Ownership

- Maintainer: [@emmanuel-a-otchere](https://github.com/emmanuel-a-otchere)
- Reviewers: open to all
- Escalation: file an issue against [AmamooIntelligence](https://github.com/emmanuel-a-otchere/AmamooIntelligence) if a base refactor breaks the recipe.

## Out of scope

- Real-time streaming / push notifications (only scheduled digests).
- Personal email/calendar integration (that's the general `morning_digest` preset — use that instead).
- Multi-language briefings — English only for v1.
- Mobile app delivery — Markdown + audio are the v1 surfaces.