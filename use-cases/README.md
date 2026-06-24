# Use Cases

OtchereJarvis is a **general-purpose base**. Specialized variants for specific domains live in **separate repos** that fork from OtchereJarvis. This folder is the starting point for scaffolding those specializations.

## Layout

```
use-cases/
├── _template/        # Copy this to scaffold a new specialization
│   ├── SPEC.md       # Fill in: goal, criteria, what stays/changes, sync strategy
│   └── README.md
└── <name>/           # (created per use case, after forking the repo)
    ├── SPEC.md
    ├── OVERLAY.md    # Every file the specialization changes on top of base
    └── tests/        # Use-case-specific tests
```

## Workflow

1. Fork `emmanuel-a-otchere/OtchereJarvis` to `emmanuel-a-otchere/OtchereJarvis-<usecase>`.
2. In the new repo, copy `_template/` → `<your-name>/` and fill it in.
3. Build your specialization as a focused layer on top of base.
4. Rebase (or merge) `base/main` weekly to pick up upstream fixes.
5. Promote generally-useful improvements back to OtchereJarvis via PR.

Full details: [`docs/SPECIALIZING.md`](../docs/SPECIALIZING.md).

## Active specializations

> None yet. When you create a specialized fork, link it here with a one-line summary.

- _add: `OtchereJarvis-<usecase>` — <what it does>_