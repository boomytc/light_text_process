# TODO 08: Release Validation

## Objective

Validate the final vendor-free release state.

## Required Work

- [x] Run the full basic validation command set from `AGENTS.md`, adjusted for
      the vendor-free cache policy.
- [x] Confirm `pyproject.toml` has no vendor package discovery, vendor package
      data, or vendor-only dependencies.
- [x] Confirm public capabilities list only retained first-party or accepted
      dependency-backed routes.
- [x] Confirm generated cache files stay under ignored runtime directories or no
      longer exist.
- [x] Update release notes with removed languages, migrated routes, dependency
      changes, and customer-visible behavior changes.

## Acceptance

- [x] Unit tests, rule validation, and num2words smoke test pass.
- [x] Vendor-removal search checks pass.
- [x] `git status --short` shows no accidental generated runtime artifacts.
