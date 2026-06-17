# TODO 04: Zh/En Native Parity

## Objective

Make zh/en TN and ITN independently strong enough to run without vendor fallback.

## Required Work

- [x] Expand zh/en golden cases for product-critical ASR post-processing,
      dates, times, money, measures, identifiers, electronic strings,
      addresses, punctuation, and mixed-language inputs.
- [x] Add a differential validator that compares first-party zh/en output
      against the vendor-enhanced baseline.
- [x] Keep intentional product improvements documented case by case.
      Current zh/en native validation has no intentional golden differences.
- [x] Replace compatibility-map behavior with explicit first-party rule logic
      where practical.
- [x] Add tests proving zh/en routes can execute without importing
      `fun_text_processing`.
- [x] Switch zh/en default routes only after parity gates pass.
      The parity gate now passes; default route migration is tracked in
      `TODO_06_ROUTE_MIGRATION.md`.

## Acceptance

- [x] `scripts/validate_rules.py --language zh --engine native` passes on first-party routes.
- [x] `scripts/validate_rules.py --language en --engine native` passes on first-party routes.
- [x] zh/en `TextProcessor` metadata or route tests prove no vendor fallback is
      used for migrated zh/en routes.
- [x] Vendor remains available only for routes not yet migrated.
