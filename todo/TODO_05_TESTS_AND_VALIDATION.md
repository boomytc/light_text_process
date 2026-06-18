# TODO 05: Tests and Validation

## Objective

Validate the native Web product without duplicating engine rule tests.

## Product Test Scope

Keep product tests focused on Web/API behavior:

- [ ] FastAPI app can be imported and created.
- [ ] `/health` returns ok.
- [ ] `/api/v1/capabilities` returns the native capability structure.
- [ ] `/api/v1/tn` works for a representative zh and en sample.
- [ ] `/api/v1/itn` works for a representative zh and en sample.
- [ ] `/api/v1/num2words` works for a representative en sample.
- [ ] `/api/v1/batch` returns mixed row output/error results where applicable.
- [ ] UI asset routes and template rendering work.
- [ ] Product error mapping returns 400 for unsupported language/mode and 500
  only for unexpected system failures.

## Tests Not To Copy

- [ ] Do not copy `test_en_*_rule_helpers.py` or `test_zh_*_rule_helpers.py` into
  the product; rule helper tests belong to the root engine package.
- [ ] Do not copy runtime engine tests for `fun_text_processing`.
- [ ] Do not copy cache maintenance tests.
- [ ] Do not copy rule-case data tests into the product.

## Repository-Level Validation

Run from `/Users/boom/workspace/light_text_process`:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

## Product-Level Validation

Run from `products/light_text_process_web` after the product exists:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q app.py api tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -c "from app import create_app; app = create_app(); print(app.title)"
```

Runtime smoke checks:

- [ ] Start the product with a local port.
- [ ] Call `/api/v1/capabilities`.
- [ ] Call `/api/v1/tn`.
- [ ] Call `/api/v1/itn`.
- [ ] Call `/api/v1/num2words`.
- [ ] Call `/api/v1/batch`.
- [ ] Stop the local server before finishing validation.

## Cleanup Checks

- [ ] Remove transient `__pycache__` and `.pytest_cache`.
- [ ] Remove one-off runtime outputs.
- [ ] Confirm product source grep has no forbidden runtime identifiers.
