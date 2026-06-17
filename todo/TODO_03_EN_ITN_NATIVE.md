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

- [ ] English number parser that handles cardinal, ordinal, decimal, and digit
      sequence modes.
- [ ] Native English ITN pipeline with ordered category passes.
- [ ] Tests for ambiguity-sensitive expressions.
- [ ] Differential comparison against vendor output.
- [ ] Golden cases expanded before each migrated category is enabled.

## Suggested Category Order

- [ ] Number, decimal, ordinal, and digit sequence parsing.
- [ ] Date and time, including month-name and numeric date variants.
- [ ] Money, fractions, percentages, ratings, and durations.
- [ ] Measures, data sizes, and rates.
- [ ] Electronic strings and identifiers.
- [ ] Punctuation, quotes, and ASR cleanup.

## Detailed Tasks

- [ ] Reuse `light_text_process/rules/en_dates.py` where it already captures
      accepted product behavior.
- [ ] Keep strict parsing and context-sensitive parsing separate.
- [ ] Handle `oh/o/zero`, hyphenated number words, `and`, multipliers such as
      `double`, and colloquial money forms.
- [ ] Add negative cases for ordinary prose that should not normalize.
- [ ] Preserve existing casing and punctuation finalization expectations.

## Acceptance Gates

- [ ] All `en/itn` golden cases pass with the native route.
- [ ] Differential comparison shows no unexplained regressions against vendor.
- [ ] Engine metadata correctly reports the native route when selected.
- [ ] Vendor fallback remains available until cutover.
- [ ] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language en --operation itn
.venv/bin/python -m unittest tests/test_en_itn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```

