# TODO 05: Release Gates

## Objective

Define the gates required before `light_text_process` can claim complete
coverage of `fun_text_processing`.

## Required Work

- [x] Run the AGENTS basic validation command set.
- [x] Run full rule validation across every route/category fixture.
- [x] Run differential checks against the oracle in strict mode.
- [x] Confirm runtime code has no `fun_text_processing` imports or package-data
      coupling.
- [x] Confirm all public TN/ITN routes remain available.
- [x] Confirm docs and release notes say "complete coverage" only after the
      coverage matrix and differential reports support that claim.
- [x] Remove transient `__pycache__`, `.pytest_cache`, generated reports, and
      one-off artifacts unless they are under ignored `runtime/`.

## Acceptance

- [x] Unit tests pass.
- [x] Rule validation passes for all expanded fixtures.
- [x] Differential strict mode has no unaccepted regressions.
- [x] Coverage matrix has no `missing` or unexplained `partial` category.
- [x] `git status --short` has no accidental generated artifacts.
