# Vendor Replacement Roadmap

## Final Direction

The final target is for first-party `light_text_process` code to replace
`third_party/fun_text_processing`, so the package no longer depends on the
third-party grammar tree.

During the transition, `fun_text_processing` remains only as a temporary backend
for code that has not yet been removed. Non-zh/en TN/ITN routes are no longer
public capabilities because they have no first-party owner or golden coverage.

## Stages

| Stage | Purpose | Vendor state |
| --- | --- | --- |
| A | Preserve the current vendor baseline and add zh/en enhancement hooks. | Required |
| B | Inventory, decide, and migrate routes one language/operation pair at a time. | Partially required |
| C | Remove vendor files, imports, dependencies, package metadata, and cache assumptions. | Removed |

## Current Public Surface

| Operation | Current public languages | Current runtime |
| --- | --- | --- |
| TN | en, zh | first-party route policy; temporary backend still present before removal |
| ITN | en, zh | first-party route policy; temporary backend still present before removal |
| num2words | installed `num2words` converter languages | `num2words` |

The non-zh/en vendor TN/ITN routes are explicitly retired from the public
surface before vendor removal. This is the breaking change that prevents a
vendor-only route from surviving as an implicit promise.

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
