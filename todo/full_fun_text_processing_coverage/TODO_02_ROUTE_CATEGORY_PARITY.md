# TODO 02: Route Category Parity

## Objective

Close first-party parity gaps for every former vendor route and category.

## Required Work

- [ ] Expand `data/rule_cases/` so each route has category-specific positive
      and negative cases, not just smoke cases.
- [ ] Add route/category validators that can run subsets by operation,
      language, and category.
- [ ] Implement missing TN categories for `de`, `es`, and `ru`.
- [ ] Implement missing ITN categories for `de`, `es`, `fr`, `id`, `ja`, `ko`,
      `pt`, `ru`, `tl`, and `vi`.
- [ ] Preserve language-specific formatting expectations rather than routing
      non-zh/en behavior through zh/en helpers.
- [ ] Document accepted product differences when first-party output should be
      better than the former vendor output.

## Acceptance

- [ ] Every former vendor route has more than smoke-test coverage.
- [ ] Every required category either passes parity checks or has an accepted
      first-party delta.
- [ ] Route/category failures point to a focused owner module.
- [ ] Public language capabilities remain unchanged while parity is improved.
