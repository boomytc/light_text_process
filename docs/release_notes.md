# Vendor-Free Release Notes

## Runtime

- Removed the `fun_text_processing` runtime adapter and `third_party/` grammar tree.
- Public TN and ITN routes are served by first-party native rule modules.
- `num2words` remains the dependency-backed number-to-words surface.

## Dependencies And Packaging

- Removed vendor-only package discovery, package data, and build metadata.
- Removed vendor-only dependencies: `pynini`, `joblib`, `tqdm`, `PyYAML`,
  `regex`, and `inflect`.

## Cache Policy

- FAR/FST grammar caches are no longer used.
- `scripts/cache_maintenance.py status` reports `cache_policy: none`.
