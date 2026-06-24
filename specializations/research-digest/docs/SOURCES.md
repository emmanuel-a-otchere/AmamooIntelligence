# Configuring sources

The `research-digest` specialization fetches items from a configurable list of RSS / Atom feeds and web URLs, defined in `configs/research-digest.toml` under `[gather].sources`.

## Default sources

```toml
[gather]
sources = [
  "https://news.ycombinator.com/rss",
  "https://arxiv.org/rss/cs.AI",
  "https://arxiv.org/rss/cs.CL",
  "https://www.technologyreview.com/feed/",
]
max_items_per_source = 25
```

These are sensible defaults for a tech / AI-leaning daily briefing.

## Customizing per deployment

Edit `configs/research-digest.toml` (or override via environment variables — see the upstream AmamooIntelligence config docs). For each source:

- Use **HTTPS** where available. The fetcher will refuse sources that redirect to plain HTTP if `require_https = true` (default in this specialization).
- Keep individual feeds under 2 MB. The fetcher hard-caps at 2 MB per feed; anything bigger is logged and skipped.
- Sources are fetched **in parallel**, capped at 8 concurrent by default.

## Suggested source bundles

| Bundle | Feeds |
| --- | --- |
| **AI / ML** | `https://arxiv.org/rss/cs.AI`, `https://arxiv.org/rss/cs.CL`, `https://arxiv.org/rss/cs.LG`, `https://huggingface.co/blog/feed.xml` |
| **Tech news** | `https://news.ycombinator.com/rss`, `https://www.technologyreview.com/feed/`, `https://feeds.arstechnica.com/arstechnica/index` |
| **Security** | `https://www.schneier.com/feed/atom/`, `https://krebsonsecurity.com/feed/`, `https://feeds.feedburner.com/TheHackersNews` |
| **Science** | `https://www.nature.com/nature.rss`, `https://www.sciencemag.org/rss/news_current.xml`, `https://arxiv.org/rss/` |

Mix and match. The orchestrator will cluster across whatever you give it — more sources means more themes to choose from, but slower runs.

## Failure handling

A source that returns 4xx/5xx, times out, or exceeds the 2 MB cap is logged at `WARN` and skipped. The digest continues with whatever succeeded. You can see per-source status in the daily `research_digest_state.json` next to the briefings directory.

## Promotion back to base

The `rss_fetch` tool shipped here is general-purpose. Once it has been validated in production for a few weeks, please open a PR against [AmamooIntelligence](https://github.com/emmanuel-a-otchere/AmamooIntelligence) to promote it to `src/openjarvis/tools/rss.py` in base.