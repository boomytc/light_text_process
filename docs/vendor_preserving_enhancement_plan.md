# Vendor-Preserving Enhancement Plan

## Direction

`fun_text_processing` remains the grammar backend and public multilingual TN/ITN
baseline. First-party `light_text_process/rules` helpers are used as a focused
enhancement layer for zh/en TN and ITN.

This project is not attempting to fully replace the upstream grammar tree.

## Public Surface

| Operation | Public languages | Runtime |
| --- | --- | --- |
| TN | de, en, es, ru, zh | `fun_text_processing` with zh/en prepare helpers |
| ITN | de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh | `fun_text_processing` with zh/en prepare/finalize helpers |
| num2words | installed `num2words` converter languages | `num2words` |

## Runtime Boundary

- `TextProcessor` uses `FunTextProcessingEngine` by default.
- Direct imports from `fun_text_processing` are allowed only inside
  `light_text_process/runtime/fun_text_processing.py`.
- `light_text_process/rules/` remains first-party and must not import vendor
  modules.
- Vendor caches are project-local under ignored `runtime/cache/fun_text_processing/`.

## Validation Policy

- zh/en TN/ITN behavior is validated by `data/rule_cases/`.
- New zh/en enhancements must add golden cases before helper changes.
- Non-zh/en languages stay vendor-owned; do not route them through zh/en helper
  logic.
- Missing `pynini`, missing `num2words`, unsupported languages, malformed input,
  and bad project-local paths must fail visibly.
