# research-digest

Scheduled multi-source research digest built on AmamooIntelligence.

See [`SPEC.md`](SPEC.md) for the full design and success criteria, and [`OVERLAY.md`](OVERLAY.md) for the file-by-file delta over base AmamooIntelligence.

## Quick start

```bash
# In the specialization repo
uv sync
uv run jarvis run --recipe configs/research-digest.toml --once
```

For scheduled runs, see the upstream AmamooIntelligence scheduling docs.

## Layout

```
research-digest/
├── SPEC.md                          # Use-case design + success criteria
├── OVERLAY.md                       # Files this specialization adds/modifies
├── README.md                        # This file
├── configs/research-digest.toml     # Recipe definition
├── src/
│   ├── agents/research_digest.py    # Scheduled agent
│   └── tools/rss.py                 # RSS/Atom fetcher
├── tests/
│   ├── test_recipe_loads.py
│   ├── test_rss_fetch.py
│   └── test_url_sanity.py
└── docs/SOURCES.md                  # How to configure the source list
```

## Syncing with base

```bash
git fetch base
git rebase base/main
pytest use-cases/research-digest/tests/
git push origin usecase/research-digest --force-with-lease
```

See [AmamooIntelligence — Specializing](../docs/SPECIALIZING.md) for the full workflow.