# TODO 06: API Product Contract and num2words Boundary

## Purpose

Ensure replacement-grade engine capability is exposed through stable root
schemas and the official Web/API product without copying engine logic into the
product.

## Tasks

- [x] Keep `products/light_text_process_web` as a thin product shell over root
  `TextProcessor`.
- [x] Keep request and response models aligned with `light_text_process.schemas`.
- [x] Keep capability metadata aligned with `light_text_process.capabilities`.
- [x] Ensure removed vendor cache controls are not present in public Web/API
  options.
- [x] Ensure batch behavior reports row-level input errors but surfaces system
  errors visibly.
- [x] Ensure examples in `products/light_text_process_web/static/data/examples.json`
  track real engine outputs.
- [x] Keep `num2words` as a separate operation, not as an implicit TN/ITN
  fallback.
- [x] Add API tests whenever schema or capability metadata changes.
- [x] Add product smoke checks for high-priority routes after engine coverage is
  expanded.

## Validation

```bash
.venv/bin/python -m unittest discover -s tests
cd products/light_text_process_web
.venv/bin/python -m compileall -q app.py api tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -c "from app import create_app; app = create_app(); print(app.title)"
```

## Completion Criteria

- Web/API product exposes root engine behavior without product-local rule
  copies.
- Capability metadata matches actual engine routes.
- Cache-era fields and grammar warmup behavior do not reappear.
- num2words remains independently validated and does not mask TN/ITN gaps.

## Non-Goals

- Do not port `core/runtime`, `core/rules`, or cache scripts from the old
  LightASR Web product into this product.
- Do not preserve old request fields for silent compatibility.
- Do not add Web UI controls for options that no longer exist.
