# Vendor Replacement Roadmap

## Final State

First-party `light_text_process` code has replaced the temporary vendor grammar
backend. The package no longer depends on the third-party grammar tree.
Non-zh/en TN/ITN routes are no longer public capabilities because they have no
first-party owner or golden coverage.

## Stages

| Stage | Purpose | Vendor state |
| --- | --- | --- |
| A | Preserve the current vendor baseline and add zh/en enhancement hooks. | Required |
| B | Inventory, decide, and migrate routes one language/operation pair at a time. | Partially required |
| C | Remove vendor files, imports, dependencies, package metadata, and cache assumptions. | Removed |

## Current Public Surface

| Operation | Current public languages | Current runtime |
| --- | --- | --- |
| TN | en, zh | first-party native rules |
| ITN | en, zh | first-party native rules |
| num2words | installed `num2words` converter languages | `num2words` |

The non-zh/en vendor TN/ITN routes are explicitly retired from the public
surface before vendor removal. This is the breaking change that prevents a
vendor-only route from surviving as an implicit promise.

## Runtime Boundary

- `TextProcessor` uses the first-party native engine by default.
- `light_text_process/rules/` remains first-party and must not import vendor modules.
- No runtime path insertion, package discovery, package-data metadata, or cache
  maintenance logic points at the removed vendor tree.

## Replacement Gates

A route can leave vendor only when:

- Golden cases cover its product-critical categories.
- Differential behavior against the vendor baseline is recorded.
- Intentional product improvements are documented.
- Unsupported options and malformed inputs fail visibly.
- Tests prove the route does not import or read removed vendor assets.

The vendor tree can be removed only when every public TN/ITN route is either
first-party or deliberately retired from capabilities.
