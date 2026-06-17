# Native Migration Inventory

This document freezes the migration baseline for replacing the vendored grammar
backend with first-party `light_text_process` runtime code.

## Public Surface

- TN languages: `en`, `zh`.
- ITN languages: `en`, `zh`.
- num2words languages: discovered from the installed `num2words` converter set.
- Request and option models live in `light_text_process/schemas.py`:
  - `TNOptions`: case, deterministic output, cache flags, project-local
    whitelist path, punctuation flags, batch size, and job count.
  - `ITNOptions`: cache flags plus legacy standalone-number toggles.
  - `Num2WordsOptions`: conversion mode and optional currency.

Only zh/en TN and ITN are in the first-party migration scope. num2words remains
a separate task surface and is not routed through TN or ITN engines.

## Vendored Capability Baseline

The vendored grammar tree used as the initial equivalence oracle contains:

| Operation | Vendor languages |
| --- | --- |
| TN | de, en, es, ru, zh |
| ITN | de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh |

The tree combines Python grammars, TSV/TXT data files, README material, and a
small number of checked-in FAR/FST artifacts. Native support must not be inferred
from this list; a language becomes public native support only after golden cases
and validation commands exist in this project.

## First-Party Rule Baseline

Current owned rule modules are intentionally language/operation-focused:

- `light_text_process/rules/en_tn.py`
- `light_text_process/rules/en_itn.py`
- `light_text_process/rules/zh_tn.py`
- `light_text_process/rules/zh_itn.py`
- `light_text_process/rules/en_dates.py`

These modules cover dates, times, money, measures, identifiers, electronic
strings, phone-like sequences, ASR post-processing, punctuation, ranges,
ratings, promotions, fractions, comparisons, and technical units. They are the
native migration source of truth.

## Golden Case Matrix

`data/rule_cases/` currently contains 376 zh/en TN/ITN cases:

| Language / Operation | Cases | Categories |
| --- | ---: | --- |
| en/tn | 75 | address, date, electronic, identity, math, measure, mixed, money, ordinal, telephone, temperature, time |
| en/itn | 111 | address, asr-postprocess, date, electronic, fraction, identity, math, measure, mixed, money, ordinal, telephone, time |
| zh/tn | 71 | address, date, electronic, identity, math, measure, mixed, money, ordinal, telephone, temperature, time |
| zh/itn | 119 | address, asr-postprocess, date, electronic, fraction, identity, math, measure, mixed, money, ordinal, phone, temperature, time |

The baseline run on 2026-06-17 passed all 376 cases against the vendored
backend. Later native phases must keep this suite green or document an accepted
intentional improvement before changing expected output.

## Differential Policy

Native work is accepted by operation and language, not by broad repository
claims. For every migrated route:

- Run `scripts/validate_rules.py --language <lang> --operation <op>`.
- Compare selected category outputs against the baseline behavior captured by
  `data/rule_cases/`.
- Treat mismatches as regressions unless the rule case or docs explicitly record
  an intentional product improvement.
- Keep unsupported languages and unsupported modes visibly failing instead of
  falling through to an unvalidated backend.

## Cache And Path Behavior

The baseline backend writes generated grammar artifacts under ignored
`runtime/cache/`. Native engines must not require FAR/FST caches for supported
zh/en TN/ITN behavior. One-off validation output and generated caches remain
outside tracked source.

`resolve_project_path()` rejects absolute paths and paths that escape
`PROJECT_DIR`; native whitelist handling must preserve that visible failure
behavior.

## Later-Phase Gates

- P1 must introduce an internal engine boundary while preserving `TextProcessor`.
- P2-P5 must route zh/en ITN/TN through first-party rules and pass the golden
  suite by language and operation.
- P6 keeps num2words policy separate from TN/ITN language exposure.
- P7 documents route defaults, limitations, dependencies, and cleanup.
- P8 removes runtime, packaging, test, script, and tree dependencies on the
  vendored grammar backend.
