# TODO 04: Zh/En Native Parity

## Objective

Keep zh/en TN and ITN independently strong enough to run without vendor
fallback while continuing to harden first-party coverage.

## Required Work

- [ ] Expand zh/en golden cases for product-critical ASR post-processing,
      dates, times, money, measures, identifiers, electronic strings,
      addresses, punctuation, and mixed-language inputs.
- [ ] Add a differential validator that compares first-party zh/en output
      against the vendor-enhanced baseline.
- [ ] Keep intentional product improvements documented case by case.
- [ ] Replace compatibility-map behavior with explicit first-party rule logic
      where practical.
- [ ] Add tests proving zh/en routes can execute without importing
      `fun_text_processing`.
- [x] Keep zh/en default routes on first-party native routing.

## Acceptance

- [ ] `scripts/validate_rules.py --language zh` passes on first-party routes.
- [ ] `scripts/validate_rules.py --language en` passes on first-party routes.
- [x] zh/en `TextProcessor` metadata or route tests prove no vendor fallback is
      used for migrated zh/en routes.
- [ ] Vendor remains available only for routes not yet migrated.
