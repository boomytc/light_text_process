# Vendor-Free Release Notes

## Runtime

- Removed the `fun_text_processing` runtime adapter and `third_party/` grammar tree.
- Public TN and ITN routes are served by first-party native rule modules.
- Public TN/ITN routes now have route/category golden coverage enforced by
  `scripts/validate_rules.py`.
- `num2words` remains the dependency-backed number-to-words surface.

## Dependencies And Packaging

- Removed vendor-only package discovery, package data, and build metadata.
- Removed vendor-only dependencies: `pynini`, `joblib`, `tqdm`, `PyYAML`,
  `regex`, and `inflect`.

## Cache Policy

- FAR/FST grammar caches are no longer used.
- `scripts/cache_maintenance.py status` reports `cache_policy: none`.

## Final Validation

- TOML parse passed for `pyproject.toml`.
- `compileall` passed for `light_text_process`, `scripts`, and `tests`.
- Unit tests passed: 52 tests.
- Rule validation passed: 538/538 cases with the route/category coverage gate.
- Oracle strict comparison passed against an external reference checkout:
  538 total, 50 matches, 488 accepted first-party improvements, 0 regressions,
  0 unsupported gaps.
- Vendor-removal searches found no runtime dependency or vendor tree.
- Public TN routes remain `de`, `en`, `es`, `ru`, and `zh`.
- Public ITN routes remain `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`,
  `ru`, `tl`, `vi`, and `zh`.
