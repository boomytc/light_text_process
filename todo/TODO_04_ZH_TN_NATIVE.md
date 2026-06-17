# TODO 04: Chinese TN Native

## Objective

Build native Chinese text normalization after native ITN has established shared
number and category infrastructure.

## Scope

- Written Chinese text to readable spoken forms.
- Numbers, decimals, dates, times, money, measures, percentages, ranges,
  temperatures, identifiers, electronic strings, and punctuation.
- Existing `TNOptions` behavior where applicable: input case, deterministic
  output, whitelist path, post processing, punctuation pre/post processing,
  batch size, and jobs.

## Deliverables

- [x] Chinese number verbalizer with deterministic output.
- [x] Native Chinese TN pipeline with category ordering.
- [x] Project-local whitelist handling compatible with `TNOptions`.
- [x] Golden and differential coverage for every enabled category.
- [x] Cache strategy decision for native TN, including whether any generated
      artifacts belong under ignored `runtime/`.

## Suggested Category Order

- [x] Numbers, decimals, signed values, and percentages.
- [x] Dates, date ranges, time, and timezone forms.
- [x] Money and currency symbols.
- [x] Measures, temperatures, speeds, and rates.
- [x] Phone numbers, IDs, order numbers, and codes.
- [x] Electronic strings, URLs, domains, email, and IP addresses.
- [x] Promotions, ratings, mixed expressions, and punctuation.

## Detailed Tasks

- [x] Keep readout rules separate from ITN parsing rules even when they share
      digit maps or unit metadata.
- [x] Preserve existing `zh_tn.prepare_input` behavior until native equivalents
      are proven.
- [x] Add explicit tests for comma-separated money, decimal yuan, signed
      temperatures, percent ranges, and date separators.
- [x] Decide which vendor differences are product improvements rather than
      regressions.

## Acceptance Gates

- [x] All `zh/tn` golden cases pass with the native route.
- [x] Differential comparison shows no unexplained regressions against vendor.
- [x] Whitelist and bad path behavior remains visible and project-local.
- [x] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language zh --operation tn
.venv/bin/python -m unittest tests/test_zh_tn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```
