# Light Text Process Web Product Instructions

## Scope

- Treat this directory as the standalone Web/API product shell for the root
  `light_text_process` engine.
- Run product setup, app imports, product tests, and local HTTP smoke checks from
  this directory.
- Keep product code focused on FastAPI routes, templates, static assets, API
  documentation, start scripts, and product-level tests.

## Boundaries

- Import engine behavior from the repository root package.
- Do not add product-local engine modules, rule suites, generated grammar
  artifacts, cache rebuild controls, or legacy import facades.
- Keep request and response models aligned with `light_text_process.schemas`.
- Keep capability data aligned with `light_text_process.capabilities`.
- Keep UI payloads explicit and current; unsupported inputs should fail visibly.

## Validation

- Product checks:
  - `.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`
  - `.venv/bin/python -m compileall -q app.py api tests`
  - `.venv/bin/python -m unittest discover -s tests`
  - `.venv/bin/python -c "from app import create_app; app = create_app(); print(app.title)"`

## Cleanup

- Stop local servers started for validation.
- Remove transient `__pycache__`, `.pytest_cache`, generated outputs, and
  one-off validation artifacts after checks.
