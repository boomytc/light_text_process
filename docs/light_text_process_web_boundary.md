# Light Text Process Web Product Boundary

## Ownership

The stable Web/API product lives at `products/light_text_process_web`.
`light_text_process/` remains the only reusable engine package, and
`data/rule_cases/` remains the only golden TN/ITN rule suite.

The source product at
`/Users/boom/workspace/LightASR/products/light_text_process_web` is a reference
for useful endpoint shape, UI workflow, checked-in browser assets, API docs,
start scripts, and Web/API tests. It is not a codebase to copy wholesale.

## Assets Allowed From The Reference Product

- `app.py` structure for FastAPI app creation, static mounting, and templates.
- `api/` route shape when rewritten to call the native root package directly.
- `templates/`, `static/`, example data, API docs, start scripts, and Web/API
  tests after removing cache and legacy engine assumptions.

## Assets Excluded From The Product

- Product-local engine packages or rule helper modules.
- Generated runtime caches and cache maintenance scripts.
- Golden rule-case data and root engine tests.
- Compatibility facades for old internal import paths.
- Any fallback backend that bypasses the first-party `light_text_process`
  package.

## Product Contract

The product exposes FastAPI routes, Jinja templates, static browser assets,
startup scripts, API documentation, and product-level tests. It calls:

- `light_text_process.TextProcessor`
- `light_text_process.capabilities.build_capabilities`
- `light_text_process.schemas`

The product must fail visibly for unsupported language, unsupported mode,
malformed input, missing dependency, or invalid project-local paths. It must not
hide failures behind compatibility behavior.

## Cleanup Grep Plan

Before cutover, search the product runtime and tests for these forbidden
identifiers:

```bash
rg -n "fun_text_processing|pynini|FAR|FST|GrammarWarmup|DEFAULT_GRAMMAR|GRAMMAR_WARMUP|cache_enabled|overwrite_cache|TextProcessingService|core\.runtime|core\.rules|third_party" products/light_text_process_web
```

Runtime source, product dependency metadata, UI payloads, and product tests
should have no matches.
