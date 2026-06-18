# Release Notes

## Replacement Coverage

- Public TN routes remain `de`, `en`, `es`, `ru`, and `zh`.
- Public ITN routes remain `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`,
  `ru`, `tl`, `vi`, and `zh`.
- Golden rule coverage expanded from the C0 baseline of 538 cases to 705 cases.
- Non-zh/en routes now include additional per-category variants instead of a
  single representative fixture per category.
- TL and VI ITN include ASR-style postprocess fixtures; multilingual TN routes
  include punctuation and mixed product-token boundary fixtures.

## Oracle Gate

The external oracle reference is outside runtime code:

```bash
/Users/boom/workspace/LightASR/light_funasr/third_party/fun_text_processing
```

Strict comparison command:

```bash
.venv/bin/python scripts/fun_text_processing_oracle.py compare \
  --reference /Users/boom/workspace/LightASR/light_funasr/third_party/fun_text_processing \
  --oracle-timeout-seconds 10 \
  --strict \
  --output runtime/oracle/fun_text_processing_diff.json
```

Latest strict result: 705 total cases, 76 `match`, 629 reviewed
`accepted-improvement`, and no `regression` or `unsupported-gap`.

This is complete replacement coverage for the public route/category surface,
not bit-for-bit vendor parity. `match` means the first-party output still
matches the preserved oracle, while `accepted-improvement` means the native
`expected` output is the reviewed release contract for that case. External
claims should describe the result as vendor-free replacement coverage instead
of vendor-identical output coverage.

Reviewed improvements are recorded in the golden cases with explicit
`expected`, `oracle_status: accepted-improvement`, and `oracle_note` fields.
The notes cover deterministic first-party formatting, product-token restoration,
ordinary-text preservation, and external oracle timeouts for routes whose
preserved vendor grammar does not complete within the release gate timeout.

## Product/API Boundary

- `products/light_text_process_web` stays a thin shell over root
  `TextProcessor`, root schemas, and root capability metadata.
- Web/API options do not expose removed cache-era fields such as
  `cache_enabled` or `overwrite_cache`.
- Batch behavior keeps row-level input errors and surfaces system-level failures
  visibly.
- Product examples are tested against real root engine outputs.

## Runtime and Cache Policy

- Runtime code remains vendor-free: no runtime import of `fun_text_processing`,
  `third_party`, `pynini`, FAR/FST grammar caches, or grammar warmup controls.
- `scripts/cache_maintenance.py status` remains the cache policy check; vendor
  grammar caches are not used.
- `num2words` remains a separate operation and is not an implicit TN/ITN
  fallback.

## Old Product Retirement

The old LightASR Web product is not deleted as part of this rule-coverage work.
Retirement should be proposed separately with evidence after this replacement
surface is accepted.
