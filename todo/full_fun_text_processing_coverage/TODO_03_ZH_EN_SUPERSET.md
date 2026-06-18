# TODO 03: Zh/En Superset

## Objective

Keep zh/en TN and ITN stronger than the former vendor behavior while proving
that vendor-era baseline categories are still covered.

## Required Work

- [ ] Map zh/en first-party cases to former vendor categories and product-only
      improvement categories.
- [ ] Add differential checks for zh/en TN and ITN against the oracle.
- [ ] Mark accepted zh/en differences where current product behavior is
      intentionally better for ASR, product tokens, mixed-language text, or
      technical identifiers.
- [ ] Add regression cases for zh/en dates, times, money, measures, telephone,
      electronic strings, identifiers, addresses, punctuation, math, fractions,
      ranges, and mixed ASR text.
- [ ] Add negative cases that prove zh/en rules do not over-normalize ordinary
      text.

## Acceptance

- [ ] zh/en cover all applicable former vendor categories.
- [ ] zh/en accepted improvements are documented as deltas, not hidden mismatches.
- [ ] Existing zh/en product improvements remain covered by golden cases.
- [ ] Strict validation can distinguish vendor parity failures from accepted
      product improvements.
