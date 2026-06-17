# TODO 07: Cutover And Release

## Objective

Move validated native implementations to default behavior and document the
release state clearly. This phase prepares for the final
`fun_text_processing` removal phase, but it does not declare the migration done
while any runtime path still depends on the vendor backend.

## Scope

- Default engine selection for validated language and operation pairs.
- Temporary vendor fallback policy before final removal.
- Cache and runtime artifact cleanup.
- Packaging and dependency simplification.
- README, AGENTS, and TODO status updates.

## Deliverables

- [ ] Default route table for every supported operation and language.
- [ ] Temporary vendor fallback policy for each non-native or partially native
      surface.
- [ ] Dependency cleanup plan for `pynini`, `joblib`, `tqdm`, `regex`, and
      other packages once vendor use changes.
- [ ] Cache maintenance updates for native and vendor cache types.
- [ ] Release notes describing native coverage, known limitations, and the
      remaining work before `fun_text_processing` can be removed.
- [ ] Final TODO index update.

## Detailed Tasks

- [ ] Mark each language/operation as native, temporary vendor-backed,
      experimental, or unsupported.
- [ ] Remove vendor package-data entries only after no supported default path
      requires them.
- [ ] Keep `third_party/fun_text_processing` only as a temporary bridge until
      every retained supported surface has passed the agreed acceptance gates or
      the user accepts dropping that surface.
- [ ] Update README architecture and direction sections.
- [ ] Update validation docs if dependencies or cache behavior changed.
- [ ] Confirm no transient `__pycache__`, `.pytest_cache`, generated outputs, or
      one-off artifacts remain outside ignored `runtime/`.

## Acceptance Gates

- [ ] Default public API uses native implementations for completed surfaces.
- [ ] Temporary vendor fallback behavior is explicit and tested.
- [ ] Packaging includes only required runtime dependencies.
- [ ] All global validation gates pass.
- [ ] Root [TODO.md](../TODO.md) marks completed phases accurately.
- [ ] P8 removal prerequisites are listed before this phase is closed.

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate_rules.py
.venv/bin/python scripts/cache_maintenance.py status
git status --short
```
