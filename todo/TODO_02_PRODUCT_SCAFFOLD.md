# TODO 02: Product Scaffold

## Objective

Create a minimal standalone FastAPI product shell under
`products/light_text_process_web` without copying engine internals.

## Target Layout

```text
products/light_text_process_web/
  AGENTS.md
  README.md
  pyproject.toml
  app.py
  product_paths.py
  api/
    __init__.py
    routes.py
  docs/
    api_contract.md
  static/
    css/
    data/
    js/
    vendor/
  templates/
    index.html
    partials/
  tests/
  start.sh
  start.bat
```

## Tasks

- [ ] Create `products/light_text_process_web/AGENTS.md` with product-local
  setup, run, validation, and cleanup rules.
- [ ] Create product `pyproject.toml` with only Web dependencies:
  `fastapi`, `jinja2`, `python-multipart`, `pydantic`, and
  `uvicorn[standard]` if needed by the product process.
- [ ] Keep the engine dependency external to the product source tree:
  install repository root editable during development, then install the product.
- [ ] Do not commit an absolute local path dependency for the root package.
- [ ] Add `product_paths.py` for product-only paths such as `PRODUCT_DIR`,
  `STATIC_DIR`, and `TEMPLATES_DIR`.
- [ ] Port `app.py` as FastAPI startup and static/template wiring only.
- [ ] Remove grammar-cache startup behavior from the scaffold.
- [ ] Port start scripts only if they stay simple and product-local.
- [ ] Keep checked-in browser assets self-contained; do not introduce a Node.js
  build step unless the existing product genuinely needs one.

## Do Not Add

- [ ] No product `core/` package.
- [ ] No product `third_party/` package.
- [ ] No product `data/rule_cases/` copy.
- [ ] No product `scripts/cache_maintenance.py`.
- [ ] No backend registry or dependency injection framework.

## Acceptance Gate

- [ ] `products/light_text_process_web` imports no product-local engine code.
- [ ] Product installation instructions are explicit and reproducible.
- [ ] Product startup can import FastAPI app without touching grammar caches.
