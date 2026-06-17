# Light Text Process Instructions

## Scope

- Treat this directory as a standalone Python project root.
- Run, test, install, and debug from this directory.
- This project owns the reusable TN, ITN, and num2words text-processing engine.
- Runtime code must resolve paths from this project directory only.

## Layout

- `light_text_process/processor.py` exposes the public engine API.
- `light_text_process/schemas.py` contains request, response, and option models.
- `light_text_process/capabilities.py` contains operation and language metadata.
- `light_text_process/runtime/` contains runtime adapters.
- `light_text_process/rules/` contains first-party zh/en TN/ITN supplemental rules. Keep new rule helpers in focused language/operation modules.
- `third_party/fun_text_processing/` is the temporary preserved grammar backend for vendor-supported TN/ITN languages while replacement work progresses.
- `data/rule_cases/` is the golden regression suite for zh/en TN/ITN behavior.
- Generated caches and one-off runtime outputs belong under ignored `runtime/`.

## Boundaries

- Do not add Web/API/UI code here.
- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules outside `third_party/`.
- Keep direct `fun_text_processing` imports inside `light_text_process/runtime/fun_text_processing.py`.
- The final target is to replace `third_party/fun_text_processing` without losing its current TN/ITN language capabilities; do not remove a vendor route as a shortcut for incomplete replacement.
- Missing `pynini`, missing `num2words`, unsupported language, unsupported mode, malformed input, or bad project-local paths should fail visibly.
- Do not add compatibility facades for old internal import paths.

## Validation

- Basic checks:
  - `.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`
  - `.venv/bin/python -m compileall -q light_text_process scripts tests`
  - `.venv/bin/python -m unittest discover -s tests`
  - `.venv/bin/python scripts/cache_maintenance.py status`
  - `.venv/bin/python scripts/validate_rules.py`
  - `.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"`

## Cleanup

- Remove transient `__pycache__`, `.pytest_cache`, generated outputs, and one-off validation artifacts after checks.
