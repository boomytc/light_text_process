# TODO 08: Remove Fun Text Processing

## Objective

Finish the migration by removing the `fun_text_processing` dependency from this
repository. After this phase, supported TN and ITN behavior should be provided
by first-party `light_text_process` code, not by the vendored backend.

## Final State

- No runtime import of `fun_text_processing`.
- No `fun_text_processing*` package discovery or package-data entries.
- No dependency on vendor FAR/FST caches for supported native behavior.
- No required `third_party/fun_text_processing` tree in the project.
- No user-facing capability that silently depends on the removed backend.

## Scope

- Runtime imports and adapter cleanup.
- `pyproject.toml` packaging and dependency cleanup.
- Cache maintenance cleanup for vendor-specific FAR files.
- README, AGENTS, and TODO status updates.
- Tests that prove removal is real rather than only unused by the happy path.

## Deliverables

- [ ] Remove or retire `light_text_process/runtime/fun_text_processing.py`.
- [ ] Remove `third_party/fun_text_processing/` from the repository, or move any
      explicitly approved non-runtime reference material outside the package
      boundary.
- [ ] Remove `fun_text_processing*` from package discovery and package data.
- [ ] Remove dependencies that only existed for the vendor backend, such as
      `pynini`, `joblib`, or `tqdm`, if no first-party runtime still needs them.
- [ ] Replace vendor-specific cache maintenance with native cache handling or
      remove the obsolete cache commands.
- [ ] Update architecture tests so any `fun_text_processing` import, package
      metadata entry, or runtime path fails the test suite.
- [ ] Update README to describe native coverage and the absence of the vendor
      dependency.
- [ ] Update root [TODO.md](../TODO.md) to mark the migration complete only
      after validation passes.

## Detailed Tasks

- [ ] Search for `fun_text_processing` across runtime code, tests, scripts,
      docs, packaging, and data.
- [ ] Decide whether historical docs may mention the old dependency. Runtime
      code and packaging must not depend on it.
- [ ] Remove `THIRD_PARTY_DIR` path injection if it only exists for the removed
      backend.
- [ ] Remove vendor cache profile names and expected FAR filenames.
- [ ] Replace any validation command that assumes vendor FAR cache generation.
- [ ] Confirm unsupported languages fail visibly rather than falling through to
      a removed backend.
- [ ] Confirm native-supported zh/en TN/ITN still pass all golden cases.
- [ ] Confirm generated outputs and transient caches are cleaned up.

## Acceptance Gates

- [ ] `rg -n "fun_text_processing|FunTextProcessingEngine" light_text_process scripts tests pyproject.toml`
      returns no runtime or packaging dependency references. Intentional
      historical TODO references must be documented separately.
- [ ] `find third_party -path '*fun_text_processing*' -print` returns no
      required runtime files.
- [ ] All supported TN and ITN operations run through native code.
- [ ] Unsupported languages and modes fail visibly.
- [ ] All global validation gates pass.
- [ ] `git status --short` shows only intentional source and documentation
      changes.

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
rg -n "fun_text_processing|FunTextProcessingEngine" light_text_process scripts tests pyproject.toml
find third_party -path '*fun_text_processing*' -print
git status --short
```

