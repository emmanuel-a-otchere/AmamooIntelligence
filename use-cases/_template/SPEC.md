# Use Case: <NAME>

> One-line summary of what this specialization does and who it serves.

## Goal

What outcome does this specialization enable that the general OtchereJarvis does not?

## Success criteria

- [ ] Measurable outcome 1 (e.g., "processes 200 invoices/hour with <2% error rate")
- [ ] Measurable outcome 2
- [ ] User-facing behavior change

## What stays general

List which OtchereJarvis subsystems you deliberately do **not** modify. These are the "inherit from base" guarantees.

- e.g., `src/openjarvis/core/` — agent loop, untouched
- e.g., `src/openjarvis/tools/email.py` — generic IMAP, reused as-is

## What this specialization changes

| Path | Change | Rationale |
| --- | --- | --- |
| `configs/openjarvis/<file>.yaml` | New preset | <why> |
| `src/openjarvis/agents/<file>.py` | New agent | <why> |
| `docs/<file>.md` | New doc | <why> |

(Keep this table short — link to commits or PRs for full diff history.)

## Sync strategy

How does this specialization track OtchereJarvis `main`?

- [ ] Rebase weekly onto `base/main`
- [ ] Merge `base/main` weekly into a long-lived `integration` branch
- [ ] Cherry-pick only specific upstream commits (lowest coupling, highest maintenance)

## Tests

- Base suite must pass: `pytest tests/`
- Specialization tests: `pytest use-cases/<name>/tests/`
- E2E / acceptance: <how you verify success criteria above>

## Ownership

- Maintainer: <GitHub handle>
- Reviewers: <handles or "open to all">
- Escalation: <where to ask if base changes break this specialization>

## Out of scope

Explicitly list what this specialization does **not** attempt, so future contributors don't accidentally expand its charter.