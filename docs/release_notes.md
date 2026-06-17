# Release Notes

## Vendor-Free Release

Date: 2026-06-17

### Runtime Changes

- `TextProcessor` now uses the first-party native TN/ITN engine by default.
- Public TN routes are limited to `en` and `zh`.
- Public ITN routes are limited to `en` and `zh`.
- `num2words` remains a separate dependency-backed surface and continues to
  report languages, modes, and currencies from the installed `num2words`
  package.

### Removed Routes

- Retired TN languages: `de`, `es`, and `ru`.
- Retired ITN languages: `de`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`,
  `tl`, and `vi`.
- Removed vendor-era ITN options for Japanese standalone number handling.
- Removed vendor-era TN option passthrough fields. TN/ITN option models now
  reject unknown fields visibly instead of accepting removed behavior.

### Dependency And Packaging Changes

- Removed the vendored `third_party/fun_text_processing` grammar tree.
- Removed the runtime vendor adapter.
- Removed vendor-only package discovery and package-data metadata.
- Removed vendor-only dependencies: `inflect`, `joblib`, `pynini`, `PyYAML`,
  `regex`, and `tqdm`.
- Runtime path setup is project-local and no longer inserts vendor paths.

### Cache Policy

- Vendor grammar FAR/FST cache generation is no longer part of this package.
- `scripts/cache_maintenance.py status` reports the vendor-free cache policy
  and does not create runtime grammar artifacts.

### Customer-Visible Behavior

- Calls to TN/ITN with retired non-zh/en languages now fail as unsupported
  language requests.
- Calls using removed TN/ITN option fields now fail validation instead of being
  passed through to a removed vendor backend.
- zh/en TN/ITN behavior is covered by the golden regression suite in
  `data/rule_cases/`.
