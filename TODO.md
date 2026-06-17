# Light Text Process Vendor Replacement TODO

This file is the root progress index for the full replacement direction:
`light_text_process` should eventually replace `third_party/fun_text_processing`
and stop depending on the third-party grammar tree.

The current transition state intentionally keeps `fun_text_processing` as the
ability baseline while first-party coverage is built and verified route by
route. Vendor removal is allowed only after every public route is either
covered by owned code or explicitly removed from the public capability surface.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

Stage A is complete: the vendor backend has been restored as the baseline, the
public capability surface reflects vendor language coverage, and zh/en
enhancement hooks live at the runtime adapter boundary.

Next work starts with Stage B0: inventory the vendor routes and decide the
replacement scope before moving more routes to first-party code.

## Phase Index

| Status | Stage | File | Purpose |
| --- | --- | --- | --- |
| [x] | A0 | [TODO_00_VENDOR_BASELINE.md](todo/TODO_00_VENDOR_BASELINE.md) | Restore vendor as the temporary ability baseline. |
| [x] | A1 | [TODO_01_PUBLIC_CAPABILITIES.md](todo/TODO_01_PUBLIC_CAPABILITIES.md) | Expose current vendor TN/ITN coverage and visible unsupported failures. |
| [x] | A2 | [TODO_02_ZH_EN_ENHANCEMENT.md](todo/TODO_02_ZH_EN_ENHANCEMENT.md) | Add zh/en first-party enhancement hooks without dropping vendor routes. |
| [ ] | B0 | [TODO_03_REPLACEMENT_INVENTORY.md](todo/TODO_03_REPLACEMENT_INVENTORY.md) | Build a route-by-route vendor capability and replacement matrix. |
| [ ] | B1 | [TODO_04_ZH_EN_NATIVE_PARITY.md](todo/TODO_04_ZH_EN_NATIVE_PARITY.md) | Harden zh/en native parity before making those routes vendor-free. |
| [ ] | B2 | [TODO_05_LANGUAGE_SUPPORT_DECISIONS.md](todo/TODO_05_LANGUAGE_SUPPORT_DECISIONS.md) | Decide which non-zh/en vendor routes remain public and which are retired. |
| [ ] | B3 | [TODO_06_ROUTE_MIGRATION.md](todo/TODO_06_ROUTE_MIGRATION.md) | Migrate approved routes one language/operation pair at a time. |
| [ ] | C0 | [TODO_07_VENDOR_REMOVAL.md](todo/TODO_07_VENDOR_REMOVAL.md) | Remove `third_party/fun_text_processing` after all gates pass. |
| [ ] | C1 | [TODO_08_RELEASE_VALIDATION.md](todo/TODO_08_RELEASE_VALIDATION.md) | Validate the vendor-free release state. |

## Cross-Stage Rules

- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules inside `light_text_process/rules/`.
- While vendor remains, keep direct `fun_text_processing` imports limited to
  `light_text_process/runtime/fun_text_processing.py`.
- Do not route non-zh/en vendor languages through zh/en helper logic.
- Do not expose a route as first-party replacement until golden cases,
  differential behavior, and failure modes are covered.
- If a vendor route will not be replaced, remove it deliberately from public
  capabilities and document the breaking change before vendor removal.
- Keep runtime path resolution project-local. Do not introduce absolute model,
  data, cache, or whitelist paths.
- Do not add Web/API/UI code to this repository.
- Missing dependencies, unsupported languages, unsupported modes, malformed
  input, and invalid project-local paths should fail visibly.

## Validation Gates

Run these while vendor is still present:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

After C0 removes the vendor backend, replace vendor cache checks with the
vendor-removal validators in `todo/TODO_07_VENDOR_REMOVAL.md`.

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
