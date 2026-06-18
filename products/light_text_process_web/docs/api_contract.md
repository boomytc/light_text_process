# Light Text Process Web API Contract

Base URL: product root.

The product exposes a native Web/API shell over the root `light_text_process`
package. Request and response bodies are aligned with
`light_text_process.schemas`; capability metadata is aligned with
`light_text_process.capabilities`.

## Current Endpoints

- `GET /health`
- `GET /api/v1/capabilities`
- `POST /api/v1/tn`
- `POST /api/v1/itn`
- `POST /api/v1/num2words`
- `POST /api/v1/batch`
- `GET /partials/capabilities`

## Capabilities

`GET /api/v1/capabilities`

Returns supported operations, languages, modes, option keys, and UI-facing
labels. Stable request values are operation keys, language codes, mode codes,
and option keys.

`num2words` includes per-language modes and currency metadata. `itn` includes
language-scoped option metadata for controls that only apply to specific
languages.

## TN

`POST /api/v1/tn`

```json
{
  "text": "今天是 2026 年 6 月 15 日。",
  "language": "zh",
  "options": {
    "input_case": "cased",
    "deterministic": true,
    "whitelist_path": null,
    "post_process": true,
    "punct_pre_process": false,
    "punct_post_process": false,
    "batch_size": 1,
    "n_jobs": 1
  }
}
```

## ITN

`POST /api/v1/itn`

```json
{
  "text": "二零二六年六月十五日",
  "language": "zh",
  "options": {
    "enable_standalone_number": true,
    "enable_0_to_9": true
  }
}
```

## num2words

`POST /api/v1/num2words`

```json
{
  "number": "12345",
  "language": "en",
  "options": {
    "mode": "cardinal",
    "currency": null
  }
}
```

## Batch

`POST /api/v1/batch`

```json
{
  "operation": "tn",
  "items": ["今天是 2026 年 6 月 15 日。"],
  "language": "zh",
  "tn_options": {},
  "itn_options": {},
  "num2words_options": {}
}
```

## Response Shape

Single-operation responses use `ProcessResponse`:

```json
{
  "operation": "tn",
  "language": "zh",
  "input": "今天是 2026 年 6 月 15 日。",
  "output": "今天是 二零二六 年 六 月 一五 日。",
  "warnings": [],
  "metadata": {
    "engine": "native",
    "elapsed_seconds": 0.01
  }
}
```

Batch responses use `BatchResponse`:

```json
{
  "operation": "num2words",
  "language": "en",
  "items": [
    {"index": 0, "input": "123", "output": "one hundred and twenty-three", "error": null}
  ],
  "success_count": 1,
  "error_count": 0,
  "metadata": {
    "elapsed_seconds": 0.01
  }
}
```

Service errors are JSON responses with a `detail` field. Request validation is
handled by FastAPI. `ValueError` from native request processing maps to HTTP
400; unexpected exceptions map to HTTP 500.
