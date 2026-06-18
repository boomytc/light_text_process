# TODO 07: Performance and Robustness

## Purpose

Prove that first-party native rules are practical for product use without
bringing back vendor grammar caches.

## Tasks

- [x] Add a lightweight benchmark script or documented command for route-level
  batch performance.
- [x] Measure high-priority `zh` and `en` TN/ITN routes on representative batch
  sizes.
- [x] Measure multilingual routes after C4 and C5 coverage work.
- [x] Add long-input tests for routes with complex regex processing.
- [x] Add malformed-input and mixed-script tests for public routes.
- [x] Check that ordinary-text negative cases remain fast and unchanged.
- [x] Review regex patterns for accidental catastrophic backtracking.
- [x] Confirm service batch fallback does not hide system-level failures.
- [x] Record acceptable performance thresholds in docs only after measurement.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -m unittest discover -s tests
```

Add benchmark command here after the benchmark entrypoint exists.

## Completion Criteria

- Native route performance is measured on realistic batches.
- No route requires grammar cache prewarming to be usable.
- Long or malformed input fails visibly or processes within documented limits.
- Robustness work does not introduce broad parser abstractions without measured
  need.

## Non-Goals

- Do not optimize before a measured bottleneck exists.
- Do not add cache layers that recreate FAR/FST lifecycle complexity.
- Do not add heavyweight dependencies for narrow regex or formatting issues.
