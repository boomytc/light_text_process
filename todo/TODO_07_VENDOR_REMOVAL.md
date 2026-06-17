# TODO 07: Vendor Removal

## Objective

Remove `third_party/fun_text_processing` only after every current vendor route
has an equivalent first-party implementation.

## Required Work

- [x] Prove every current vendor TN/ITN route is first-party or dependency-backed
      by an accepted non-vendor boundary.
- [x] Remove `light_text_process/runtime/fun_text_processing.py`.
- [x] Remove `third_party/fun_text_processing/` from the project tree.
- [x] Remove `third_party/` path insertion from `light_text_process/paths.py`.
- [x] Remove vendor package discovery and package-data entries from
      `pyproject.toml`.
- [x] Remove vendor-only dependencies such as `pynini`, `joblib`, `tqdm`,
      `PyYAML`, `regex`, and `inflect` when no first-party runtime needs them.
- [x] Remove or rewrite `scripts/cache_maintenance.py` so it no longer assumes
      FAR/FST grammar caches.
- [x] Update architecture tests to reject all `fun_text_processing` imports.
- [x] Update README, AGENTS, TODO, and release docs to describe the vendor-free
      state.

## Acceptance

- [x] `rg -n "fun_text_processing|FunTextProcessingEngine" light_text_process scripts tests pyproject.toml`
      returns no runtime dependency.
- [x] `find third_party -path '*fun_text_processing*' -print` returns no files.
- [x] Full validation passes after vendor files and dependencies are removed.
- [x] Generated caches and one-off validation artifacts are clean.

## Evidence

- `scripts/cache_maintenance.py status` reports `cache_policy: none`.
- `pyproject.toml` contains only first-party package discovery and active
  runtime dependencies.
- `tests/test_architecture_boundaries.py` rejects vendor imports anywhere under
  `light_text_process/`.
