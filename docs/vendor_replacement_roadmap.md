# Vendor Replacement Roadmap

## Final State

First-party `light_text_process` code has replaced `third_party/fun_text_processing`,
so runtime capability is owned by this package rather than the third-party
grammar tree.

## Stages

| Stage | Purpose | Vendor state |
| --- | --- | --- |
| A | Preserve the current vendor baseline and add zh/en enhancement hooks. | Complete |
| B | Inventory, decide, and migrate routes one language/operation pair at a time. | Complete |
| C | Remove vendor files, imports, dependencies, package metadata, and cache assumptions. | Removed |

## Current Public Surface

| Operation | Current public languages | Current runtime |
| --- | --- | --- |
| TN | de, en, es, ru, zh | `light_text_process_native` |
| ITN | de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh | `light_text_process_native` |
| num2words | installed `num2words` converter languages | `num2words` |

This table is the vendor-free public surface. Each non-zh/en route has
first-party ownership, golden coverage, and migration order recorded in
`docs/route_ownership.md`.

## Runtime Boundary

- `TextProcessor` uses native routes for every public TN/ITN language.
- `light_text_process/rules/` remains first-party and must not import vendor modules.
- FAR/FST grammar caches are not used.

## Replacement Gates

A route can leave vendor only when:

- Golden cases cover its product-critical categories.
- Differential behavior against the vendor baseline is recorded.
- Intentional product improvements are documented.
- Unsupported options and malformed inputs fail visibly.
- Tests prove the route does not import or read from `third_party/fun_text_processing`.

The vendor tree was removed after every public TN/ITN route had a first-party
implementation and remained covered by public capabilities.
