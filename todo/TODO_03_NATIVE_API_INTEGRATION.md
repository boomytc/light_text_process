# TODO 03: Native API Integration

## Objective

Recreate the HTTP API surface using native `light_text_process` APIs directly.

## Target Endpoints

- [ ] `GET /health`
- [ ] `GET /api/v1/capabilities`
- [ ] `POST /api/v1/tn`
- [ ] `POST /api/v1/itn`
- [ ] `POST /api/v1/num2words`
- [ ] `POST /api/v1/batch`
- [ ] `GET /partials/capabilities` if the UI still uses the HTMX partial.

## Direct Engine Contract

Use these first-party imports directly in the product boundary:

```python
from light_text_process import TextProcessor
from light_text_process.capabilities import build_capabilities
from light_text_process.schemas import (
    BatchRequest,
    BatchResponse,
    ITNRequest,
    Num2WordsRequest,
    ProcessResponse,
    TNRequest,
)
```

## Tasks

- [ ] Replace `TextProcessingService` with `TextProcessor`.
- [ ] Replace product-local capability metadata with
  `light_text_process.capabilities.build_capabilities`.
- [ ] Replace product-local schemas with `light_text_process.schemas`.
- [ ] Keep request error mapping simple: validation/model errors by FastAPI,
  `ValueError` as HTTP 400, unexpected exceptions as HTTP 500.
- [ ] Preserve the public response shape from `ProcessResponse` and
  `BatchResponse`.
- [ ] Let capabilities expose the native engine's real language surface instead
  of freezing the old Web product to zh/en.
- [ ] Avoid service wrappers unless they remove product-specific HTTP noise;
  do not add a wrapper just to preserve old class names.
- [ ] Remove all cache options from request construction and server-side logic.

## Explicit Deletions From Source Product Model

- [ ] Delete `DEFAULT_GRAMMAR_WARMUP_PROFILES` and `GRAMMAR_WARMUP_PROFILES`.
- [ ] Delete `warmup_default_grammars()` and startup prewarm env vars.
- [ ] Delete `cache_enabled` and `overwrite_cache` handling.
- [ ] Delete any API path that mentions grammar cache rebuilds.

## Acceptance Gate

- [ ] API routes contain no `core.` imports.
- [ ] API routes contain no `fun_text_processing` imports or strings except in
  migration notes outside runtime code.
- [ ] Native smoke examples work through HTTP for TN, ITN, num2words, and batch.
