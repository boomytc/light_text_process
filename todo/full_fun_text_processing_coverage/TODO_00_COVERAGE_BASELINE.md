# TODO 00: Coverage Baseline

## Objective

Define the measurable target for fully covering the former
`fun_text_processing` TN/ITN surface.

## Required Work

- [ ] Reconstruct the former vendor public route list from repository history,
      release notes, and current capabilities.
- [ ] For every route, list the former vendor categories that must be covered.
- [ ] Mark current first-party category coverage as `covered`, `partial`,
      `missing`, or `intentional-delta`.
- [ ] Identify language-specific options and behaviors, including Japanese ITN
      standalone-number handling.
- [ ] Record known current gaps, especially non-zh/en ITN cardinal, money,
      date, time, measure, telephone, electronic, ordinal, and fraction cases.
- [ ] Update `docs/replacement_matrix.md` so it reflects real coverage status
      instead of only route ownership.

## Acceptance

- [ ] Each former vendor TN/ITN route has a category matrix.
- [ ] Each category has an owner module and a current coverage status.
- [ ] The baseline distinguishes language availability from behavioral parity.
- [ ] No route is described as fully covered without category evidence.
