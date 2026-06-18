# TODO 01: Oracle Diff Gate

## Purpose

Make replacement quality measurable against a preserved `fun_text_processing`
reference without making `fun_text_processing` a runtime dependency.

## Tasks

- [ ] Standardize the oracle reference path used for local comparison.
- [ ] Run oracle comparison across every public TN/ITN route.
- [ ] Store generated oracle reports only under ignored `runtime/oracle/`.
- [ ] Ensure strict mode fails unreviewed `regression` and `unsupported-gap`
  statuses.
- [ ] Require every `accepted-improvement` case to include:
  - explicit `expected` output,
  - `oracle_status: accepted-improvement`,
  - short `oracle_note` explaining why the native output is better.
- [ ] Add route-level summary output to the oracle report if current output is
  too hard to triage by route.
- [ ] Add category-level summary output if regressions cannot be localized
  quickly.
- [ ] Add tests for oracle parsing and classification whenever the report schema
  changes.
- [ ] Document the exact oracle command in `docs/replacement_matrix.md`.

## Suggested Oracle Command

```bash
.venv/bin/python scripts/fun_text_processing_oracle.py compare \
  --reference /path/to/fun_text_processing \
  --strict \
  --output runtime/oracle/fun_text_processing_diff.json
```

## Completion Criteria

- The strict oracle command completes with no unreviewed `regression`.
- The strict oracle command completes with no unreviewed `unsupported-gap`.
- Every intentional native-vs-oracle difference is encoded in the relevant
  golden case and can be audited without reading implementation code.
- Oracle tooling remains outside runtime imports.

## Non-Goals

- Do not make oracle output a runtime fallback.
- Do not preserve vendor quirks that are lower quality than the first-party
  output.
- Do not classify a difference as accepted merely to pass strict mode.
