# Light Text Process Native Migration TODO

This file is the root progress index for the completed migration from the old
vendored grammar backend into first-party `light_text_process` implementations.

The goal was not to copy the vendor tree mechanically. The goal was to turn this
repository into a stronger, more controllable TN, ITN, and num2words engine
while preserving the existing public API, project-local path boundary, and
golden behavior. The final state is a native `light_text_process` engine that
does not import, package, install, or require the old vendored backend.

## Progress Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked or needs a decision

## Current Phase

Migration is complete. Chinese and English TN/ITN default to native routes, and
the vendored backend, package metadata, cache commands, and vendor-only
dependencies have been removed.

## Phase Index

| Status | Phase | File | Purpose |
| --- | --- | --- | --- |
| [x] | P0 | [TODO_00_BASELINE_AND_SCOPE.md](todo/TODO_00_BASELINE_AND_SCOPE.md) | Freeze the baseline, inventory vendor capabilities, and define migration gates. |
| [x] | P1 | [TODO_01_ENGINE_ABSTRACTION.md](todo/TODO_01_ENGINE_ABSTRACTION.md) | Add a native-ready runtime boundary without changing `TextProcessor` callers. |
| [x] | P2 | [TODO_02_ZH_ITN_NATIVE.md](todo/TODO_02_ZH_ITN_NATIVE.md) | Migrate Chinese ITN categories first because they are high-value for ASR output. |
| [x] | P3 | [TODO_03_EN_ITN_NATIVE.md](todo/TODO_03_EN_ITN_NATIVE.md) | Migrate English ITN with ASR-friendly post-processing and ambiguity controls. |
| [x] | P4 | [TODO_04_ZH_TN_NATIVE.md](todo/TODO_04_ZH_TN_NATIVE.md) | Migrate Chinese TN while preserving deterministic readout behavior. |
| [x] | P5 | [TODO_05_EN_TN_NATIVE.md](todo/TODO_05_EN_TN_NATIVE.md) | Migrate English TN categories and keep casing/punctuation options compatible. |
| [x] | P6 | [TODO_06_NUM2WORDS_AND_MULTILINGUAL.md](todo/TODO_06_NUM2WORDS_AND_MULTILINGUAL.md) | Decide which num2words and non-zh/en language surfaces become first-party. |
| [x] | P7 | [TODO_07_CUTOVER_AND_RELEASE.md](todo/TODO_07_CUTOVER_AND_RELEASE.md) | Cut over validated native defaults and prepare release documentation. |
| [x] | P8 | [TODO_08_REMOVE_FUN_TEXT_PROCESSING.md](todo/TODO_08_REMOVE_FUN_TEXT_PROCESSING.md) | Remove `fun_text_processing` imports, package data, dependencies, caches, and vendor files. |

## Cross-Phase Rules

- Keep TN, ITN, and num2words as separate task surfaces.
- Keep first-party rules inside `light_text_process/rules/`.
- Keep runtime path resolution project-local. Do not introduce absolute model,
  data, cache, or whitelist paths.
- Do not add Web/API/UI code to this repository.
- Keep runtime code free of removed vendor backend imports.
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
- Historical differential comparisons either matched or documented intentional
  improvements.
- The final phase removed the old vendored backend from runtime imports,
  packaging metadata, dependency requirements, cache maintenance assumptions,
  and the project tree.
- Generated caches and one-off validation artifacts are removed or kept under
  ignored `runtime/`.
