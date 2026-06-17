# Light Text Process Native Migration TODO

This file is the root progress index for migrating
`third_party/fun_text_processing` into first-party `light_text_process`
implementations and ultimately removing the `fun_text_processing` runtime
dependency from this project.

The goal is not to copy the vendor tree mechanically. The goal is to turn this
repository into a stronger, more controllable TN, ITN, and num2words engine
while preserving the existing public API, project-local path boundary, and
golden behavior. The final state is a native `light_text_process` engine that
does not import, package, install, or require `fun_text_processing`.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

`P4` is the current implementation phase. Chinese and English ITN now default to
the native route; remaining TN route work must preserve the public API and
golden behavior defined in `docs/native_migration_inventory.md`.

## Phase Index

| Status | Phase | File | Purpose |
| --- | --- | --- | --- |
| [x] | P0 | [TODO_00_BASELINE_AND_SCOPE.md](todo/TODO_00_BASELINE_AND_SCOPE.md) | Freeze the baseline, inventory vendor capabilities, and define migration gates. |
| [x] | P1 | [TODO_01_ENGINE_ABSTRACTION.md](todo/TODO_01_ENGINE_ABSTRACTION.md) | Add a native-ready runtime boundary without changing `TextProcessor` callers. |
| [x] | P2 | [TODO_02_ZH_ITN_NATIVE.md](todo/TODO_02_ZH_ITN_NATIVE.md) | Migrate Chinese ITN categories first because they are high-value for ASR output. |
| [x] | P3 | [TODO_03_EN_ITN_NATIVE.md](todo/TODO_03_EN_ITN_NATIVE.md) | Migrate English ITN with ASR-friendly post-processing and ambiguity controls. |
| [~] | P4 | [TODO_04_ZH_TN_NATIVE.md](todo/TODO_04_ZH_TN_NATIVE.md) | Migrate Chinese TN while preserving deterministic readout behavior. |
| [ ] | P5 | [TODO_05_EN_TN_NATIVE.md](todo/TODO_05_EN_TN_NATIVE.md) | Migrate English TN categories and keep casing/punctuation options compatible. |
| [ ] | P6 | [TODO_06_NUM2WORDS_AND_MULTILINGUAL.md](todo/TODO_06_NUM2WORDS_AND_MULTILINGUAL.md) | Decide which num2words and non-zh/en language surfaces become first-party. |
| [ ] | P7 | [TODO_07_CUTOVER_AND_RELEASE.md](todo/TODO_07_CUTOVER_AND_RELEASE.md) | Cut over validated native defaults and prepare release documentation. |
| [ ] | P8 | [TODO_08_REMOVE_FUN_TEXT_PROCESSING.md](todo/TODO_08_REMOVE_FUN_TEXT_PROCESSING.md) | Remove `fun_text_processing` imports, package data, dependencies, caches, and vendor files. |

## Cross-Phase Rules

- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules outside `third_party/`.
- Keep runtime path resolution project-local. Do not introduce absolute model,
  data, cache, or whitelist paths.
- Do not add Web/API/UI code to this repository.
- Keep `fun_text_processing` imports isolated behind runtime adapter boundaries
  until the final removal phase deletes that dependency completely.
- Do not expose a language or operation as native until its golden cases,
  differential cases, and failure modes are covered.
- Missing dependencies, unsupported languages, unsupported modes, malformed
  input, and invalid project-local paths should fail visibly.

## Global Validation Gates

Run these before marking a phase complete:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

Additional phase-specific validators are listed in each `todo/TODO_*.md` file.

## Completion Policy

A phase is complete only when:

- Its detailed TODO file has all required checklist items checked.
- Public API behavior remains compatible unless the phase explicitly documents a
  supported breaking change and the user accepts it.
- Golden rule cases pass for every affected language and operation.
- Differential comparisons against `third_party/fun_text_processing` either
  match or have documented, intentional improvements.
- The final phase removes `fun_text_processing` from runtime imports,
  packaging metadata, dependency requirements, cache maintenance assumptions,
  and the project tree unless the user explicitly chooses to archive a
  non-runtime reference copy outside the package.
- Generated caches and one-off validation artifacts are removed or kept under
  ignored `runtime/`.
