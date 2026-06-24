"""Scheduled research-digest agent for AmamooIntelligence.

This module is part of the `research-digest` specialization. It is a thin
stateful wrapper around the upstream orchestrator agent, with persistence
of the last-run timestamp and idempotent re-runs.
"""
from __future__ import annotations

import datetime as _dt
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DigestRun:
    """A single execution of the digest workflow."""

    started_at: _dt.datetime
    finished_at: _dt.datetime | None = None
    themes: list[str] = field(default_factory=list)
    citations_total: int = 0
    output_markdown: Path | None = None
    output_audio: Path | None = None
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "themes": self.themes,
            "citations_total": self.citations_total,
            "output_markdown": str(self.output_markdown) if self.output_markdown else None,
            "output_audio": str(self.output_audio) if self.output_audio else None,
            "errors": self.errors,
        }


class ResearchDigestAgent:
    """Orchestrates the gather → cluster → deep-research → synthesize workflow.

    State (last run, run history) is persisted to a JSON sidecar next to the
    briefing output directory. This makes re-runs idempotent and gives operators
    an audit trail without needing a database.
    """

    def __init__(self, recipe_path: Path, state_dir: Path) -> None:
        self.recipe_path = recipe_path
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = state_dir / "research_digest_state.json"
        self.last_run = self._load_state()

    def _load_state(self) -> DigestRun | None:
        if not self.state_file.exists():
            return None
        try:
            data = json.loads(self.state_file.read_text())
            return DigestRun(
                started_at=_dt.datetime.fromisoformat(data["started_at"]),
                finished_at=(
                    _dt.datetime.fromisoformat(data["finished_at"])
                    if data.get("finished_at")
                    else None
                ),
                themes=data.get("themes", []),
                citations_total=data.get("citations_total", 0),
            )
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.warning("Could not parse state file %s: %s — starting fresh",
                           self.state_file, exc)
            return None

    def _save_state(self, run: DigestRun) -> None:
        self.state_file.write_text(json.dumps(run.to_dict(), indent=2))

    def should_run(self, now: _dt.datetime) -> bool:
        """Idempotency guard: only run if the last run was on a different day
        (or has never happened)."""
        if self.last_run is None or self.last_run.finished_at is None:
            return True
        return self.last_run.finished_at.date() < now.date()

    def run(self, now: _dt.datetime | None = None) -> DigestRun:
        """Execute the digest workflow. Returns the run record.

        The actual gather / cluster / synthesize steps are delegated to the
        upstream orchestrator agent (configured via `agent_template` in the
        recipe). This class owns the lifecycle, state, and idempotency.
        """
        now = now or _dt.datetime.now()
        run = DigestRun(started_at=now)
        logger.info("Starting research-digest run at %s", now.isoformat())

        # The real implementation invokes the orchestrator here. Stubbed so
        # this module imports cleanly before the upstream agent is fully wired.
        # See the recipe's [agent] section and the upstream `orchestrator` agent.
        try:
            self._invoke_orchestrator(run)
        except Exception as exc:  # noqa: BLE001 — surface any error in state
            logger.exception("Orchestrator failed")
            run.errors.append(str(exc))

        run.finished_at = _dt.datetime.now()
        self._save_state(run)
        return run

    def _invoke_orchestrator(self, run: DigestRun) -> None:
        """Hook for the upstream orchestrator. Implemented by the deployer.

        This stub records the intent without performing the call. A real
        deployment wires this to `openjarvis.agents.orchestrator.OrchestratorAgent`.
        """
        logger.info("Orchestrator invocation is a no-op in this specialization stub.")
        run.themes = []
        run.citations_total = 0