# TODO 08: Release Validation

## Objective

Validate the final vendor-free release state.

## Required Work

- [x] Run the full basic validation command set from `AGENTS.md`, adjusted for
      the vendor-free cache policy.
- [x] Confirm `pyproject.toml` has no vendor package discovery, vendor package
      data, or vendor-only dependencies.
- [x] Confirm public capabilities still list every replacement-target route,
      with each TN/ITN route served by first-party runtime code.
- [x] Confirm generated cache files stay under ignored runtime directories or no
      longer exist.
- [x] Update release notes with route migration status, capability preservation
      evidence, dependency changes, and customer-visible behavior changes.

## Acceptance

- [x] Unit tests, rule validation, and num2words smoke test pass.
- [x] Vendor-removal search checks pass.
- [x] `git status --short` shows no accidental generated runtime artifacts.

## Evidence

- Unit tests: 43 passed.
- Rule validation: 389 passed, 0 failed.
- Cache policy: `cache_policy: none`.
- num2words smoke: `one hundred and twenty-three`.
- Public capabilities: TN `de,en,es,ru,zh`; ITN
  `de,en,es,fr,id,ja,ko,pt,ru,tl,vi,zh`.
