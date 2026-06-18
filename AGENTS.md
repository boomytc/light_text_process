# Light Text Process Instructions

## Scope

- Treat this directory as a standalone Python project root.
- Run, test, install, and debug from this directory.
- This project owns the reusable TN, ITN, and num2words text-processing engine,
  plus product shells under `products/`.
- Runtime code must resolve paths from this project directory only.

## Layout

- `light_text_process/processor.py` exposes the public engine API.
- `light_text_process/schemas.py` contains request, response, and option models.
- `light_text_process/capabilities.py` contains operation and language metadata.
- `light_text_process/runtime/` contains runtime adapters.
- `light_text_process/rules/` contains first-party TN/ITN rules. Keep new rule helpers in focused language/operation modules.
- `data/rule_cases/` is the golden regression suite for public TN/ITN behavior.
- `products/` contains product shells that call the root package instead of owning
  reusable text-processing logic.
- `products/light_text_process_web/` is the official Web/API product for this
  engine. Keep product-specific setup, routes, templates, static files, docs,
  scripts, and Web/API tests there.
- `playground/` is for experiments only and must not host stable product code.
- Generated caches and one-off runtime outputs belong under ignored `runtime/`.

## Boundaries

- Do not add Web/API/UI code under the root engine package. Product code belongs
  under `products/`.
- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules inside `light_text_process/rules/`.
- Do not reintroduce `third_party/`, `fun_text_processing`, FAR/FST grammar caches, or vendor compatibility shims.
- Missing `num2words`, unsupported language, unsupported mode, malformed input, or bad project-local paths should fail visibly.
- Do not add compatibility facades for old internal import paths.
- Product shells may import `TextProcessor`, schemas, and capability metadata
  from `light_text_process`, but must not copy engine code, rule data, runtime
  adapters, or cache maintenance flows.

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
