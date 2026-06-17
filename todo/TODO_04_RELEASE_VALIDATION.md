# TODO 04: Release Validation

## Objective

Validate that the package is releasable with the vendor backend preserved.

## Required Work

- [ ] Run the full basic validation command set from `AGENTS.md`.
- [ ] Run `scripts/cache_maintenance.py status` and any needed warmup checks.
- [ ] Confirm `pyproject.toml` includes vendor package data and dependency
      requirements.
- [ ] Confirm generated cache files stay under ignored `runtime/`.
- [ ] Update release notes whenever public language coverage or dependency
      expectations change.

## Acceptance

- [ ] Unit tests, rule validation, cache status, and num2words smoke test pass.
- [ ] `git status --short` shows no accidental generated runtime artifacts.
