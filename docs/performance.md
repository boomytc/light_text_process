# Performance and Robustness

Native TN and ITN routes are regular Python rules. They do not use FAR/FST
grammar caches, grammar warmup, or vendor cache controls.

## Benchmark Command

Run route-level batch benchmarks from the project root:

```bash
.venv/bin/python scripts/benchmark_routes.py --repeat 25 --batch-size 64
```

Focused examples:

```bash
.venv/bin/python scripts/benchmark_routes.py --operation tn --language zh --language en --repeat 25 --batch-size 64
.venv/bin/python scripts/benchmark_routes.py --operation itn --repeat 25 --batch-size 64
```

## Current Measurement

Measured on June 18, 2026 with the golden case suite expanded to 705 cases.
Representative full-suite command:

```bash
.venv/bin/python scripts/benchmark_routes.py --repeat 25 --batch-size 64
```

Acceptable release threshold: each public route should process representative
golden batches at more than 500 items per second on this local machine. This is
well below observed throughput and leaves margin for product overhead.

| Operation | Language | Items | Elapsed seconds | Items/second |
| --- | --- | ---: | ---: | ---: |
| ITN | `de` | 600 | 0.0584 | 10271.6 |
| ITN | `en` | 2775 | 2.1971 | 1263.1 |
| ITN | `es` | 600 | 0.0513 | 11685.2 |
| ITN | `fr` | 650 | 0.0622 | 10451.8 |
| ITN | `id` | 600 | 0.0577 | 10405.9 |
| ITN | `ja` | 725 | 0.0693 | 10455.0 |
| ITN | `ko` | 650 | 0.0489 | 13279.3 |
| ITN | `pt` | 600 | 0.0567 | 10575.4 |
| ITN | `ru` | 600 | 0.0914 | 6566.2 |
| ITN | `tl` | 625 | 0.0540 | 11568.3 |
| ITN | `vi` | 625 | 0.1040 | 6008.6 |
| ITN | `zh` | 2975 | 0.7512 | 3960.3 |
| TN | `de` | 650 | 0.0307 | 21192.3 |
| TN | `en` | 1875 | 0.3230 | 5805.2 |
| TN | `es` | 650 | 0.0063 | 102816.9 |
| TN | `ru` | 650 | 0.0082 | 78918.2 |
| TN | `zh` | 1775 | 0.1625 | 10925.4 |

## Robustness Checks

- Long ordinary text is covered by unit tests so negative cases stay unchanged.
- Mixed-script technical text is covered by unit tests so code-like tokens are
  not broadly normalized by multilingual routes.
- Bad project-local paths, such as missing whitelist files, fail visibly.
- Batch fallback keeps row-level input errors but reraises system-level
  failures.
- Regexes are intentionally route-local and bounded around concrete token
  classes; no route requires cache prewarming to be usable.
