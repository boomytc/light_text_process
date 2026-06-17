# TODO 03: Replacement Inventory

## Objective

Build a route-by-route matrix that makes the replacement scope explicit before
more code is migrated.

## Required Work

- [ ] Inventory vendor TN routes: `de`, `en`, `es`, `ru`, `zh`.
- [ ] Inventory vendor ITN routes: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`,
      `pt`, `ru`, `tl`, `vi`, `zh`.
- [ ] For each language/operation pair, list major categories such as date,
      time, cardinal, ordinal, money, measure, telephone, electronic, fraction,
      whitelist, and punctuation.
- [ ] Record which categories already have first-party helper coverage.
- [ ] Record which routes depend on FAR/FST cache generation, checked-in
      grammar artifacts, TSV/TXT data files, or language-specific options.
- [ ] Identify current golden coverage under `data/rule_cases/` and missing
      coverage for every public route.
- [ ] Create or update a replacement matrix document under `docs/`.

## Acceptance

- [ ] Every public TN/ITN route has an owner decision placeholder: replace,
      retire, or defer.
- [ ] The matrix distinguishes current vendor support from first-party support.
- [ ] Future migration phases can pick routes from the matrix without guessing
      scope.
