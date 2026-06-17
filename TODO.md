# Light Text Process Vendor-Preserving TODO

This file is the root progress index for the vendor-preserving direction:
keep the full `fun_text_processing` backend available, and strengthen zh/en TN
and ITN through first-party `light_text_process/rules` helpers.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

The repository now keeps `fun_text_processing` as the default grammar backend.
zh/en enhancement hooks live at the runtime adapter boundary; non-zh/en routes
remain vendor-owned.

## Phase Index

| Status | Phase | File | Purpose |
| --- | --- | --- | --- |
| [x] | V0 | [TODO_00_VENDOR_BASELINE.md](todo/TODO_00_VENDOR_BASELINE.md) | Restore and preserve the full vendored grammar backend. |
| [x] | V1 | [TODO_01_PUBLIC_CAPABILITIES.md](todo/TODO_01_PUBLIC_CAPABILITIES.md) | Expose vendor TN/ITN language coverage while keeping unsupported routes explicit. |
| [x] | V2 | [TODO_02_ZH_EN_ENHANCEMENT.md](todo/TODO_02_ZH_EN_ENHANCEMENT.md) | Keep zh/en enhancement hooks at the adapter boundary. |
| [ ] | V3 | [TODO_03_GOLDEN_EXPANSION.md](todo/TODO_03_GOLDEN_EXPANSION.md) | Add product-driven zh/en cases for behavior beyond the current suite. |
| [ ] | V4 | [TODO_04_RELEASE_VALIDATION.md](todo/TODO_04_RELEASE_VALIDATION.md) | Validate packaging, cache maintenance, and vendor-preserving release notes. |

## Cross-Phase Rules

- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules inside `light_text_process/rules/`.
- Keep direct `fun_text_processing` imports limited to
  `light_text_process/runtime/fun_text_processing.py`.
- Keep runtime path resolution project-local. Do not introduce absolute model,
  data, cache, or whitelist paths.
- Do not add Web/API/UI code to this repository.
- Do not route non-zh/en vendor languages through zh/en helper logic.
- Missing dependencies, unsupported languages, unsupported modes, malformed
  input, and invalid project-local paths should fail visibly.

## Global Validation Gates

Run these before marking a phase complete:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

Additional phase-specific validators are listed in each `todo/TODO_*.md` file.

## Completion Policy

A phase is complete only when:

- Its detailed TODO file has all required checklist items checked.
- Public API behavior remains compatible unless the phase explicitly documents a
  supported breaking change and the user accepts it.
- Golden rule cases pass for every affected zh/en language and operation.
- Non-zh/en vendor routes remain vendor-owned and are not changed accidentally.
- Generated caches and one-off validation artifacts are removed or kept under
  ignored `runtime/`.
