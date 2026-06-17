# TODO 02: Chinese ITN Native

## Objective

Build the first production-grade native ITN path for Chinese. This should focus
on ASR-facing text because Chinese ITN is the highest-value migration surface
for downstream recognition, search, and storage.

## Scope

- Chinese number reading to digits.
- Dates, times, durations, money, measures, percentages, ranges, temperatures,
  phone-like identifiers, punctuation, ASR fillers, and common colloquial forms.
- Existing `ITNOptions` behavior.
- Output finalization currently handled by `light_text_process/rules/zh_itn.py`.

## Deliverables

- [ ] Native Chinese number parser shared by category rules.
- [ ] Native Chinese ITN pipeline with ordered category passes.
- [ ] Category-focused modules under `light_text_process/rules/` or a native
      runtime package, without adding broad compatibility facades.
- [ ] Differential tests against vendor output for selected categories.
- [ ] Golden cases expanded for every migrated category.
- [ ] Decision log for intentional improvements over vendor behavior.

## Suggested Category Order

- [ ] Number and decimal readings.
- [ ] Date and time.
- [ ] Money and percentages.
- [ ] Measures and units.
- [ ] Phone, ID, order, and other digit-sequence contexts.
- [ ] Punctuation and ASR cleanup.
- [ ] Ranges, ratings, promotions, and mixed expressions.

## Detailed Tasks

- [ ] Extract reusable Chinese digit, unit, decimal, and magnitude parsing.
- [ ] Separate strict numeric parsing from context-sensitive digit-sequence
      parsing.
- [ ] Ensure `零`, `〇`, `两`, `幺`, colloquial `块/毛/分`, and half quantities
      are covered where expected.
- [ ] Preserve or improve existing `zh_itn.prepare_input` and
      `zh_itn.finalize_outputs` behavior.
- [ ] Add negative cases where native parsing must leave text unchanged.
- [ ] Add batch tests for mixed successful and malformed inputs.

## Acceptance Gates

- [ ] All `zh/itn` golden cases pass with the native route.
- [ ] Differential comparison shows no unexplained regressions against vendor.
- [ ] Engine metadata correctly reports the native route when selected.
- [ ] Vendor fallback remains available until cutover.
- [ ] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language zh --operation itn
.venv/bin/python -m unittest tests/test_zh_itn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```

