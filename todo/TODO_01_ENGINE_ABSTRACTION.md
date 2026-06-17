# TODO 01: Engine Abstraction

## Objective

Introduce a first-party runtime boundary that can host both the current vendor
engine and future native engines while keeping `TextProcessor` stable.

## Scope

- Add a small engine protocol or equivalent adapter interface for TN and ITN.
- Keep `TextProcessor.normalize_text`, `TextProcessor.inverse_normalize_text`,
  `TextProcessor.batch`, and warmup behavior compatible.
- Preserve visible error behavior for missing dependencies, unsupported
  language, unsupported mode, malformed input, and invalid paths.
- Keep vendor imports isolated.

## Deliverables

- [x] Runtime engine interface for TN and ITN operations.
- [x] Vendor adapter renamed or wrapped so it implements the engine interface.
- [x] Native engine skeleton with explicit unsupported-category behavior.
- [x] Engine selection mechanism that is internal and conservative by default.
- [x] Tests proving public API callers do not need to know which engine ran.
- [x] Metadata that can report `engine=fun_text_processing` or
      `engine=light_text_process_native` without changing response models.

## Detailed Tasks

- [x] Define the minimal method set: normalize, inverse_normalize, warmup_tn,
      and warmup_itn.
- [x] Remove direct `TextProcessor` dependence on a concrete
      `FunTextProcessingEngine` attribute name.
- [x] Keep batch fallback semantics from `_batch_rows`.
- [x] Keep warmup profile compatibility for existing grammar cache flows.
- [x] Add tests with fake vendor and fake native engines.
- [x] Add tests that unsupported native routes fall back or fail according to
      the selected phase policy.
- [x] Update cache maintenance docs if native engines do not use FAR caches.

## Acceptance Gates

- [x] Public `TextProcessor` calls behave the same under the default engine.
- [x] `fun_text_processing` imports remain limited to the vendor adapter.
- [x] Native engine skeleton can be instantiated without importing vendor code.
- [x] Existing tests pass.
- [x] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python -m unittest tests/test_services.py
.venv/bin/python -m unittest tests/test_runtime_engines.py
.venv/bin/python -m unittest tests/test_architecture_boundaries.py
.venv/bin/python scripts/validate_rules.py
```
