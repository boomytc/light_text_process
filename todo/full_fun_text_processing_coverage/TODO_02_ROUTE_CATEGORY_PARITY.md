# TODO 02: Route Category Parity

## Objective

Close first-party parity gaps for every former vendor route and category.

## Required Work

- [x] Expand `data/rule_cases/` so each route has category-specific positive
      and negative cases, not just smoke cases.
- [x] Add route/category validators that can run subsets by operation,
      language, and category.
- [x] Implement missing TN categories for `de`, `es`, and `ru`.
- [x] Implement missing ITN categories for `de`, `es`, `fr`, `id`, `ja`, `ko`,
      `pt`, `ru`, `tl`, and `vi`.
- [x] Preserve language-specific formatting expectations rather than routing
      non-zh/en behavior through zh/en helpers.
- [x] Document accepted product differences when first-party output should be
      better than the former vendor output.

## Acceptance

- [x] Every former vendor route has more than smoke-test coverage.
- [x] Every required category either passes parity checks or has an accepted
      first-party delta.
- [x] Route/category failures point to a focused owner module.
- [x] Public language capabilities remain unchanged while parity is improved.
