# TODO 08: Release Validation

## Objective

Validate the final vendor-free release state.

## Required Work

- [ ] Run the full basic validation command set from `AGENTS.md`, adjusted for
      the vendor-free cache policy.
- [ ] Confirm `pyproject.toml` has no vendor package discovery, vendor package
      data, or vendor-only dependencies.
- [ ] Confirm public capabilities list only retained first-party or accepted
      dependency-backed routes.
- [ ] Confirm generated cache files stay under ignored runtime directories or no
      longer exist.
- [ ] Update release notes with removed languages, migrated routes, dependency
      changes, and customer-visible behavior changes.

## Acceptance

- [ ] Unit tests, rule validation, and num2words smoke test pass.
- [ ] Vendor-removal search checks pass.
- [ ] `git status --short` shows no accidental generated runtime artifacts.
