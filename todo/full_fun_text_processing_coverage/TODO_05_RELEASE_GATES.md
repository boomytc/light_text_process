# TODO 05: Release Gates

## Objective

Define the gates required before `light_text_process` can claim complete
coverage of `fun_text_processing`.

## Required Work

- [ ] Run the AGENTS basic validation command set.
- [ ] Run full rule validation across every route/category fixture.
- [ ] Run differential checks against the oracle in strict mode.
- [ ] Confirm runtime code has no `fun_text_processing` imports or package-data
      coupling.
- [ ] Confirm all public TN/ITN routes remain available.
- [ ] Confirm docs and release notes say "complete coverage" only after the
      coverage matrix and differential reports support that claim.
- [ ] Remove transient `__pycache__`, `.pytest_cache`, generated reports, and
      one-off artifacts unless they are under ignored `runtime/`.

## Acceptance

- [ ] Unit tests pass.
- [ ] Rule validation passes for all expanded fixtures.
- [ ] Differential strict mode has no unaccepted regressions.
- [ ] Coverage matrix has no `missing` or unexplained `partial` category.
- [ ] `git status --short` has no accidental generated artifacts.
