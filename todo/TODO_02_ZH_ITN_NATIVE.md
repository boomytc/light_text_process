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

- [x] Native Chinese number parser shared by category rules.
- [x] Native Chinese ITN pipeline with ordered category passes.
- [x] Category-focused modules under `light_text_process/rules/` or a native
      runtime package, without adding broad compatibility facades.
- [x] Differential tests against vendor output for selected categories.
- [x] Golden cases expanded for every migrated category.
- [x] Decision log for intentional improvements over vendor behavior.

## Suggested Category Order

- [x] Number and decimal readings.
- [x] Date and time.
- [x] Money and percentages.
- [x] Measures and units.
- [x] Phone, ID, order, and other digit-sequence contexts.
- [x] Punctuation and ASR cleanup.
- [x] Ranges, ratings, promotions, and mixed expressions.

## Detailed Tasks

- [x] Extract reusable Chinese digit, unit, decimal, and magnitude parsing.
- [x] Separate strict numeric parsing from context-sensitive digit-sequence
      parsing.
- [x] Ensure `零`, `〇`, `两`, `幺`, colloquial `块/毛/分`, and half quantities
      are covered where expected.
- [x] Preserve or improve existing `zh_itn.prepare_input` and
      `zh_itn.finalize_outputs` behavior.
- [x] Add negative cases where native parsing must leave text unchanged.
- [x] Add batch tests for mixed successful and malformed inputs.

## Acceptance Gates

- [x] All `zh/itn` golden cases pass with the native route.
- [x] Differential comparison shows no unexplained regressions against vendor.
- [x] Engine metadata correctly reports the native route when selected.
- [x] Vendor fallback remains available until cutover.
- [x] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language zh --operation itn
.venv/bin/python -m unittest tests/test_zh_itn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```
