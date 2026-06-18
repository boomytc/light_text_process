# Full fun_text_processing Coverage TODO

This is the active TODO index for making `light_text_process` fully cover the
behavioral surface previously provided by `fun_text_processing`.

The target is not just matching public language names. Completion requires
route-level and category-level coverage for the former TN and ITN grammars, plus
the existing first-party zh/en improvements.

## Active Directory

All active TODO files live under:

```text
todo/full_fun_text_processing_coverage/
```

Completed vendor-removal TODO files have been removed from the active TODO
surface.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

Current work is P5: run the release gates, refresh validation evidence, and
remove transient artifacts.

## Phase Index

| Status | Phase | File | Purpose |
| --- | --- | --- | --- |
| [x] | P0 | [TODO_00_COVERAGE_BASELINE.md](todo/full_fun_text_processing_coverage/TODO_00_COVERAGE_BASELINE.md) | Define the full route/category coverage target. |
| [x] | P1 | [TODO_01_ORACLE_AND_DIFF.md](todo/full_fun_text_processing_coverage/TODO_01_ORACLE_AND_DIFF.md) | Build a safe comparison oracle for former vendor behavior. |
| [x] | P2 | [TODO_02_ROUTE_CATEGORY_PARITY.md](todo/full_fun_text_processing_coverage/TODO_02_ROUTE_CATEGORY_PARITY.md) | Close parity gaps route by route and category by category. |
| [x] | P3 | [TODO_03_ZH_EN_SUPERSET.md](todo/full_fun_text_processing_coverage/TODO_03_ZH_EN_SUPERSET.md) | Preserve and expand the stronger zh/en TN/ITN behavior. |
| [x] | P4 | [TODO_04_MULTILINGUAL_PARITY.md](todo/full_fun_text_processing_coverage/TODO_04_MULTILINGUAL_PARITY.md) | Bring non-zh/en routes up to the former vendor surface. |
| [ ] | P5 | [TODO_05_RELEASE_GATES.md](todo/full_fun_text_processing_coverage/TODO_05_RELEASE_GATES.md) | Prove full coverage before claiming completion. |

## Coverage Scope

The coverage target includes these former vendor public routes:

- TN: `de`, `en`, `es`, `ru`, `zh`
- ITN: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh`

The category target includes the applicable former grammar categories:
cardinal, ordinal, decimal, date, time, money, measure, telephone, electronic,
fraction, range, roman, whitelist, word, punctuation, and language-specific
character or name handling.

## Non-Negotiable Rules

- Keep runtime code first-party and project-local.
- Do not reintroduce `fun_text_processing` as a runtime dependency or import.
- Use `scripts/fun_text_processing_oracle.py` for isolated reference checks;
  pass the external reference path explicitly with `--reference`.
- Do not use a language route name as proof of capability coverage.
- Do not mark a route complete until its former vendor categories are covered
  or explicitly documented as intentional first-party product differences.
- Keep TN, ITN, and num2words separate.
- Preserve current zh/en improvements while closing former vendor parity gaps.
- Keep unsupported language, unsupported mode, malformed input, and invalid
  project-local path failures visible.

## Completion Definition

Full coverage is complete only when:

- Every former public TN/ITN route has category-level first-party coverage.
- Golden cases cover each route/category pair with positive and negative cases.
- Differential reports compare current output against the former vendor oracle.
- Intentional zh/en product improvements are documented as accepted deltas.
- Non-zh/en routes cover more than simple digit-sequence smoke cases.
- Validation passes with no runtime dependency on `fun_text_processing`.
