# TODO 00: Coverage Baseline

## Objective

Define the measurable target for fully covering the former
`fun_text_processing` TN/ITN surface.

## Required Work

- [x] Reconstruct the former vendor public route list from repository history,
      release notes, and current capabilities.
- [x] For every route, list the former vendor categories that must be covered.
- [x] Mark current first-party category coverage as `covered`, `partial`,
      `missing`, or `intentional-delta`.
- [x] Identify language-specific options and behaviors, including Japanese ITN
      standalone-number handling.
- [x] Record known current gaps, especially non-zh/en ITN cardinal, money,
      date, time, measure, telephone, electronic, ordinal, and fraction cases.
- [x] Update `docs/replacement_matrix.md` so it reflects real coverage status
      instead of only route ownership.

## Acceptance

- [x] Each former vendor TN/ITN route has a category matrix.
- [x] Each category has an owner module and a current coverage status.
- [x] The baseline distinguishes language availability from behavioral parity.
- [x] No route is described as fully covered without category evidence.
