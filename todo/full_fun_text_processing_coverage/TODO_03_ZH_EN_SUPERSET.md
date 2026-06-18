# TODO 03: Zh/En Superset

## Objective

Keep zh/en TN and ITN stronger than the former vendor behavior while proving
that vendor-era baseline categories are still covered.

## Required Work

- [x] Map zh/en first-party cases to former vendor categories and product-only
      improvement categories.
- [x] Add differential checks for zh/en TN and ITN against the oracle.
- [x] Mark accepted zh/en differences where current product behavior is
      intentionally better for ASR, product tokens, mixed-language text, or
      technical identifiers.
- [x] Add regression cases for zh/en dates, times, money, measures, telephone,
      electronic strings, identifiers, addresses, punctuation, math, fractions,
      ranges, and mixed ASR text.
- [x] Add negative cases that prove zh/en rules do not over-normalize ordinary
      text.

## Acceptance

- [x] zh/en cover all applicable former vendor categories.
- [x] zh/en accepted improvements are documented as deltas, not hidden mismatches.
- [x] Existing zh/en product improvements remain covered by golden cases.
- [x] Strict validation can distinguish vendor parity failures from accepted
      product improvements.
