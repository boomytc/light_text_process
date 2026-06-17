# TODO 00: Vendor Baseline

## Objective

Preserve the full `fun_text_processing` backend as the temporary baseline
grammar runtime while first-party replacement coverage is built.

## Required Work

- [x] Restore `third_party/fun_text_processing/` in this project tree.
- [x] Add `third_party/` to runtime import paths from `light_text_process/paths.py`.
- [x] Restore project-local grammar cache directory handling under
      `runtime/cache/fun_text_processing/`.
- [x] Restore vendor package discovery, package data, and runtime dependencies
      in `pyproject.toml`.
- [x] Restore `scripts/cache_maintenance.py` for project-local FAR cache
      inspection, warmup, rebuild, and cleanup.

## Acceptance

- [x] `fun_text_processing` can be imported through the project runtime path.
- [x] Missing vendor dependencies still fail visibly.
- [x] Runtime caches remain ignored and are not tracked source.
- [x] This phase does not declare vendor to be permanent.
