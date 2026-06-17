# Vendor Replacement Roadmap

## Final Direction

The final target is for first-party `light_text_process` code to replace
`third_party/fun_text_processing`, so the package no longer depends on the
third-party grammar tree.

During the transition, `fun_text_processing` remains the ability baseline. This
prevents losing existing multilingual TN/ITN behavior while first-party route
coverage is built and verified.

## Stages

| Stage | Purpose | Vendor state |
| --- | --- | --- |
| A | Preserve the current vendor baseline and add zh/en enhancement hooks. | Required |
| B | Inventory, decide, and migrate routes one language/operation pair at a time. | Partially required |
| C | Remove vendor files, imports, dependencies, package metadata, and cache assumptions. | Removed |

## Current Public Surface

| Operation | Current public languages | Current runtime |
| --- | --- | --- |
| TN | de, en, es, ru, zh | `fun_text_processing` with zh/en prepare helpers |
| ITN | de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh | `fun_text_processing` with zh/en prepare/finalize helpers |
| num2words | installed `num2words` converter languages | `num2words` |

This table is a transition baseline, not a promise that every vendor language
must remain public forever. Each non-zh/en route needs an explicit replace,
retire, or defer decision before vendor removal.

## Runtime Boundary

- While vendor remains, `TextProcessor` uses `FunTextProcessingEngine` by
  default.
- Direct imports from `fun_text_processing` are allowed only inside
  `light_text_process/runtime/fun_text_processing.py`.
- `light_text_process/rules/` remains first-party and must not import vendor
  modules.
- Vendor caches are project-local under ignored `runtime/cache/fun_text_processing/`.

## Replacement Gates

A route can leave vendor only when:

- Golden cases cover its product-critical categories.
- Differential behavior against the vendor baseline is recorded.
- Intentional product improvements are documented.
- Unsupported options and malformed inputs fail visibly.
- Tests prove the route does not import or read from `third_party/fun_text_processing`.

The vendor tree can be removed only when every public TN/ITN route is either
first-party or deliberately retired from capabilities.
