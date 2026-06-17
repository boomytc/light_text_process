# TODO 07: Vendor Removal

## Objective

Remove `third_party/fun_text_processing` only after every current vendor route
has an equivalent first-party implementation.

## Required Work

- [ ] Prove every current vendor TN/ITN route is first-party or dependency-backed
      by an accepted non-vendor boundary.
- [ ] Remove `light_text_process/runtime/fun_text_processing.py`.
- [ ] Remove `third_party/fun_text_processing/` from the project tree.
- [ ] Remove `third_party/` path insertion from `light_text_process/paths.py`.
- [ ] Remove vendor package discovery and package-data entries from
      `pyproject.toml`.
- [ ] Remove vendor-only dependencies such as `pynini`, `joblib`, `tqdm`,
      `PyYAML`, `regex`, and `inflect` when no first-party runtime needs them.
- [ ] Remove or rewrite `scripts/cache_maintenance.py` so it no longer assumes
      FAR/FST grammar caches.
- [ ] Update architecture tests to reject all `fun_text_processing` imports.
- [ ] Update README, AGENTS, TODO, and release docs to describe the vendor-free
      state.

## Acceptance

- [ ] `rg -n "fun_text_processing|FunTextProcessingEngine" light_text_process scripts tests pyproject.toml`
      returns no runtime dependency.
- [ ] `find third_party -path '*fun_text_processing*' -print` returns no files.
- [ ] Full validation passes after vendor files and dependencies are removed.
- [ ] Generated caches and one-off validation artifacts are clean.
