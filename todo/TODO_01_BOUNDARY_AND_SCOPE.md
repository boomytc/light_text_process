# TODO 01: Boundary and Scope Reset

## Objective

Make this repository explicitly own both the reusable engine and its official
Web/API product shell, without weakening the engine boundary.

## Tasks

- [ ] Update root `AGENTS.md` to allow `products/` as a product layer while
  keeping `light_text_process/` as the only engine package.
- [ ] Add product-specific guidance for `products/light_text_process_web/` once
  the product directory exists.
- [ ] Document that `playground/` is for experiments only and must not host the
  stable Web/API product.
- [ ] Confirm the target product path:
  `products/light_text_process_web`.
- [ ] Confirm the source product is a reference only:
  `/Users/boom/workspace/LightASR/products/light_text_process_web`.
- [ ] Decide which source assets are product assets and may move:
  `app.py`, `api/`, `templates/`, `static/`, API docs, start scripts, and
  Web/API tests.
- [ ] Decide which source assets must not move:
  `core/`, `third_party/`, generated `runtime/`, rule golden cases, grammar
  cache maintenance scripts, and vendor-specific tests.

## Explicit Non-Goals

- [ ] Do not preserve the old `core.*` import surface.
- [ ] Do not create a compatibility package to make old tests pass unchanged.
- [ ] Do not copy first-party engine code into product-local `third_party/`.
- [ ] Do not retain `fun_text_processing` as a fallback backend.
- [ ] Do not support old FAR/FST cache operations in the native product.

## Acceptance Gate

- [ ] The repository instructions describe `products/` clearly.
- [ ] The Web product boundary is documented before implementation starts.
- [ ] A grep plan exists for later cleanup of forbidden identifiers:
  `fun_text_processing`, `pynini`, `core.runtime`, `TextProcessingService`,
  `cache_enabled`, `overwrite_cache`.
