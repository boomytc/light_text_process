# TODO 03: English ITN Native

## Objective

Build the native English ITN path after the Chinese ITN infrastructure proves
the migration pattern.

## Scope

- English number words to digits.
- Ordinals, dates, times, durations, money, measures, fractions, percentages,
  temperatures, ratings, identifiers, electronic strings, punctuation, and ASR
  filler cleanup.
- Existing `ITNOptions` behavior and finalization logic.

## Deliverables

- [x] English number parser that handles cardinal, ordinal, decimal, and digit
      sequence modes.
- [x] Native English ITN pipeline with ordered category passes.
- [x] Tests for ambiguity-sensitive expressions.
- [x] Differential comparison against vendor output.
- [x] Golden cases expanded before each migrated category is enabled.

## Suggested Category Order

- [x] Number, decimal, ordinal, and digit sequence parsing.
- [x] Date and time, including month-name and numeric date variants.
- [x] Money, fractions, percentages, ratings, and durations.
- [x] Measures, data sizes, and rates.
- [x] Electronic strings and identifiers.
- [x] Punctuation, quotes, and ASR cleanup.

## Detailed Tasks

- [x] Reuse `light_text_process/rules/en_dates.py` where it already captures
      accepted product behavior.
- [x] Keep strict parsing and context-sensitive parsing separate.
- [x] Handle `oh/o/zero`, hyphenated number words, `and`, multipliers such as
      `double`, and colloquial money forms.
- [x] Add negative cases for ordinary prose that should not normalize.
- [x] Preserve existing casing and punctuation finalization expectations.

## Acceptance Gates

- [x] All `en/itn` golden cases pass with the native route.
- [x] Differential comparison shows no unexplained regressions against vendor.
- [x] Engine metadata correctly reports the native route when selected.
- [x] Vendor fallback remains available until cutover.
- [x] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language en --operation itn
.venv/bin/python -m unittest tests/test_en_itn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```
