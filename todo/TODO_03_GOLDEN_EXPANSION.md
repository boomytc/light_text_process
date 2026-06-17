# TODO 03: Golden Expansion

## Objective

Add product-driven zh/en regression coverage when new enhancement requirements
appear.

## Required Work

- [ ] Record every new zh/en behavior gap as a case under `data/rule_cases/`.
- [ ] Keep expected output focused on product needs, not broad upstream parity.
- [ ] Add edge cases for ASR post-processing, addresses, dates, money, measures,
      identifiers, and mixed-language input as those gaps are discovered.
- [ ] Run operation-scoped validation before changing helper logic.

## Acceptance

- [ ] New cases fail before the helper change and pass after it.
- [ ] No non-zh/en vendor language behavior is changed by zh/en helper updates.
