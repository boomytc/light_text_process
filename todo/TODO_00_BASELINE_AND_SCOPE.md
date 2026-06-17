# TODO 00: Baseline And Scope

## Objective

Build the evidence base for a safe native migration. This phase keeps
`third_party/fun_text_processing` as the equivalence oracle and defines what
must be true before any native implementation can replace it.

## Scope

- Inventory vendor TN and ITN languages, categories, data files, and runtime
  options.
- Map current first-party behavior in `light_text_process/rules/`,
  `light_text_process/runtime/`, `light_text_process/processor.py`, and
  `data/rule_cases/`.
- Expand regression coverage before changing engine selection.
- Define differential comparison output so native work can be judged category
  by category.

## Deliverables

- [x] Vendor capability inventory for TN and ITN.
- [x] Current native supplement inventory for zh/en TN and ITN.
- [x] Rule-case category matrix for `data/rule_cases/*.json`.
- [x] Differential runner plan or script that compares vendor and native output
      for selected language, operation, category, and case IDs.
- [x] Baseline cache behavior documented for warmup and rebuild flows.
- [x] Explicit migration acceptance gates for each later phase.

## Detailed Tasks

- [x] Count vendor files by operation, language, and category.
- [x] List current supported public languages from
      `light_text_process/capabilities.py`.
- [x] List current public request and option models from
      `light_text_process/schemas.py`.
- [x] Confirm `fun_text_processing` imports are restricted to the runtime
      adapter boundary.
- [x] Confirm path validation rejects absolute and out-of-project paths.
- [x] Audit golden cases for weak categories, especially mixed, electronic,
      address, telephone, identity, temperature, money, date, time, and measure.
- [x] Add missing golden cases before migrating the corresponding category.
- [x] Decide and document how intentional improvements are recorded when native
      output should differ from vendor output.

## Acceptance Gates

- [x] `scripts/validate_rules.py --list` shows all expected zh/en TN/ITN cases.
- [x] Golden cases cover every category selected for the first native migration.
- [x] A future native engine can be compared against vendor output without
      changing public API callers.
- [x] The root [TODO.md](../TODO.md) phase status is updated when this phase is
      complete.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --list
.venv/bin/python -m unittest tests/test_architecture_boundaries.py
.venv/bin/python -m unittest tests/test_rule_cases_data.py
```
