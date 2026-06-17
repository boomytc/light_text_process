# TODO 04: Zh/En Native Parity

## Objective

Keep zh/en TN and ITN independently strong enough to run without vendor
fallback while continuing to harden first-party coverage.

## Required Work

- [x] Expand zh/en golden cases for product-critical ASR post-processing,
      dates, times, money, measures, identifiers, electronic strings,
      addresses, punctuation, and mixed-language inputs.
- [x] Add a differential validator that compares first-party zh/en output
      against the vendor-enhanced baseline.
- [x] Keep intentional product improvements documented case by case.
- [x] Replace compatibility-map behavior with explicit first-party rule logic
      where practical.
- [x] Add tests proving zh/en routes can execute without importing
      `fun_text_processing`.
- [x] Keep zh/en default routes on first-party native routing.

## Acceptance

- [x] `scripts/validate_rules.py --language zh` passes on first-party routes.
- [x] `scripts/validate_rules.py --language en` passes on first-party routes.
- [x] zh/en `TextProcessor` metadata or route tests prove no vendor fallback is
      used for migrated zh/en routes.
- [x] Vendor remains available only for routes not yet migrated.

## Evidence

- `scripts/validate_rules.py --language zh --engine native` passed with
  190/190 cases.
- `scripts/validate_rules.py --language en --engine native` passed with
  186/186 cases.
- `tests.test_runtime_engines` proves native zh/en execution does not load the
  vendor package or runtime adapter.
