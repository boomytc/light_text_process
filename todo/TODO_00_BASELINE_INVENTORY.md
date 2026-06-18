# TODO 00: Baseline Inventory

## Purpose

Freeze the current replacement baseline before adding more rules. This prevents
future work from drifting into broad compatibility shims or unbounded language
growth.

## Tasks

- [ ] Record the current public TN and ITN route list from
  `light_text_process.capabilities`.
- [ ] Record the current case count by file and route from `data/rule_cases/`.
- [ ] Record category coverage by route using `scripts/validate_rules.py --list`
  or an equivalent read-only inventory.
- [ ] Identify which public routes are first-party rule implementations and
  which shared helper modules they use.
- [ ] Record the exact external oracle reference path used for comparison, such
  as a preserved `fun_text_processing` directory outside runtime code.
- [ ] Confirm that the root package imports and runtime code do not import
  `fun_text_processing`.
- [ ] Confirm the Web product imports root `TextProcessor`, root schemas, and
  root capability metadata instead of owning engine code.
- [ ] Add a short baseline note to `docs/replacement_matrix.md` if the current
  documented route list or category list is stale.

## Required Evidence

- Current route list.
- Current case-count table.
- Current category coverage table.
- Current oracle reference path.
- Current vendor audit output.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --list
rg -n "from fun_text_processing|import fun_text_processing|pynini|third_party" light_text_process pyproject.toml
```

## Completion Criteria

- Baseline is documented before new capability work begins.
- No runtime dependency on vendor code is introduced.
- No route is added or removed during this phase.

## Non-Goals

- Do not change rule behavior.
- Do not add new compatibility options.
- Do not expand language support in this phase.
