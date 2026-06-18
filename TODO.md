# TODO: Native Light Text Process Web Product

## Goal

Recreate the `Light Text Process Web` product inside this repository as
`products/light_text_process_web`, using the first-party native
`light_text_process` package as the only text-processing engine.

Source product for behavior and UI reference:
`/Users/boom/workspace/LightASR/products/light_text_process_web`

Target product:
`/Users/boom/workspace/light_text_process/products/light_text_process_web`

This is a native product rebuild, not a vendor copy and not a compatibility
migration. The product should reproduce the useful Web/API surface while
deleting historical implementation baggage.

## Non-Negotiable Boundaries

- Keep `light_text_process/` as the only engine and rules source.
- Do not copy `light_text_process/` into any product `third_party/` tree.
- Do not create `third_party/light_text_process`, `third_party/fun_text_processing`,
  FAR/FST caches, or `pynini` dependencies in the Web product.
- Do not recreate product-local `core/rules`, `core/runtime`, or
  `core/services` engine layers.
- Do not add compatibility facades for old imports such as `core.services`,
  `core.schemas`, or `core.runtime.fun_text_processing`.
- Keep rule golden cases under repository-level `data/rule_cases/`; the Web
  product should not own a second rule suite.
- Keep the Web product focused on FastAPI routes, templates, static assets,
  API docs, startup scripts, and product-level tests.
- Prefer direct use of `TextProcessor`, `build_capabilities`, and schema models
  from `light_text_process`; add adapters only where HTTP/UI boundaries require
  them.
- No plugin registry, backend registry, cache manager, feature flag system,
  or migration shim unless a concrete product need appears.

## Phase Index

1. [Boundary and scope reset](todo/TODO_01_BOUNDARY_AND_SCOPE.md)
2. [Product scaffold](todo/TODO_02_PRODUCT_SCAFFOLD.md)
3. [Native API integration](todo/TODO_03_NATIVE_API_INTEGRATION.md)
4. [Frontend and examples](todo/TODO_04_FRONTEND_AND_EXAMPLES.md)
5. [Tests and validation](todo/TODO_05_TESTS_AND_VALIDATION.md)
6. [Cutover and cleanup](todo/TODO_06_CUTOVER_AND_CLEANUP.md)

## Completion Definition

The rebuild is complete only when all of these are true:

- `products/light_text_process_web` runs from its own environment.
- The Web API exposes `/api/v1/capabilities`, `/api/v1/tn`, `/api/v1/itn`,
  `/api/v1/num2words`, and `/api/v1/batch` through native `light_text_process`.
- Product startup does not prewarm grammar caches and does not depend on
  generated FAR/FST files.
- Product source contains no `fun_text_processing`, `pynini`,
  `core.runtime.fun_text_processing`, `TextProcessingService`, `cache_enabled`,
  or `overwrite_cache` runtime path.
- Product source contains no product-local rules duplicate and no copied engine.
- Repository-level engine validation still passes.
- Product-level API/UI validation passes.
- The old LightASR product copy is either removed, archived outside the active
  product path, or clearly marked as superseded by this repository.
