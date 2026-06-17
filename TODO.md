# Light Text Process Vendor Replacement TODO

This file is the root progress index for the completed replacement direction:
`light_text_process` has replaced `third_party/fun_text_processing` for retained
public TN/ITN routes and no longer depends on the third-party grammar tree.

The final vendor-free state keeps only public TN/ITN routes that are either
covered by owned code or explicitly backed by an accepted package dependency.
Vendor-only routes have been removed from the public capability surface.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

All stages are complete. The repository is in the vendor-free release state:
TN/ITN keep first-party `en` and `zh` routes, `num2words` remains
dependency-backed, and removed vendor-only routes fail visibly as unsupported.

## Phase Index

| Status | Stage | File | Purpose |
| --- | --- | --- | --- |
| [x] | A0 | [TODO_00_VENDOR_BASELINE.md](todo/TODO_00_VENDOR_BASELINE.md) | Restore vendor as the temporary ability baseline. |
| [x] | A1 | [TODO_01_PUBLIC_CAPABILITIES.md](todo/TODO_01_PUBLIC_CAPABILITIES.md) | Expose current vendor TN/ITN coverage and visible unsupported failures. |
| [x] | A2 | [TODO_02_ZH_EN_ENHANCEMENT.md](todo/TODO_02_ZH_EN_ENHANCEMENT.md) | Add zh/en first-party enhancement hooks without dropping vendor routes. |
| [x] | B0 | [TODO_03_REPLACEMENT_INVENTORY.md](todo/TODO_03_REPLACEMENT_INVENTORY.md) | Build a route-by-route vendor capability and replacement matrix. |
| [x] | B1 | [TODO_04_ZH_EN_NATIVE_PARITY.md](todo/TODO_04_ZH_EN_NATIVE_PARITY.md) | Harden zh/en native parity before making those routes vendor-free. |
| [x] | B2 | [TODO_05_LANGUAGE_SUPPORT_DECISIONS.md](todo/TODO_05_LANGUAGE_SUPPORT_DECISIONS.md) | Decide which non-zh/en vendor routes remain public and which are retired. |
| [x] | B3 | [TODO_06_ROUTE_MIGRATION.md](todo/TODO_06_ROUTE_MIGRATION.md) | Migrate approved routes one language/operation pair at a time. |
| [x] | C0 | [TODO_07_VENDOR_REMOVAL.md](todo/TODO_07_VENDOR_REMOVAL.md) | Remove `third_party/fun_text_processing` after all gates pass. |
| [x] | C1 | [TODO_08_RELEASE_VALIDATION.md](todo/TODO_08_RELEASE_VALIDATION.md) | Validate the vendor-free release state. |

## Cross-Stage Rules

- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules inside `light_text_process/rules/`.
- Do not route non-zh/en vendor languages through zh/en helper logic.
- Do not expose a route as first-party replacement until golden cases,
  differential behavior, and failure modes are covered.
- Do not add direct vendor grammar imports, vendor package-data metadata, or
  runtime path insertion for removed vendor trees.
- If a removed route is requested, fail visibly instead of keeping a
  compatibility facade.
- Keep runtime path resolution project-local. Do not introduce absolute model,
  data, cache, or whitelist paths.
- Do not add Web/API/UI code to this repository.
- Missing dependencies, unsupported languages, unsupported modes, malformed
  input, and invalid project-local paths should fail visibly.

## Validation Gates

Run these for the vendor-free release state:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

For vendor-removal regressions, also run the search validators in
`todo/TODO_07_VENDOR_REMOVAL.md`.

## Completion Policy

A phase is complete only when:

- Its detailed TODO file has all required checklist items checked.
- Public API behavior remains compatible unless the phase explicitly documents a
  supported breaking change and the user accepts it.
- Golden rule cases pass for every affected language and operation.
- Differential results against the vendor baseline are either matching or
  documented as intentional product improvements.
- Generated caches and one-off validation artifacts are removed or kept under
  ignored `runtime/`.
