# Light Text Process fun_text_processing Capability Coverage TODO

## Goal

Make `light_text_process` capable of replacing the public TN/ITN behavior that
the former `fun_text_processing` runtime provided, while keeping the current
vendor-free architecture.

This is a capability coverage plan, not a compatibility-layer plan.

## Current Baseline

- Runtime package dependencies are intentionally small: `num2words` and
  `pydantic`.
- Runtime code must stay vendor-free: no product/runtime dependency on
  `fun_text_processing`, `third_party`, `pynini`, FAR/FST grammar caches, or old
  import facades.
- Current public TN routes: `de`, `en`, `es`, `ru`, `zh`.
- Current public ITN routes: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`,
  `ru`, `tl`, `vi`, `zh`.
- Current golden case suite has 550 cases under `data/rule_cases/`.
- Existing validation tools include `scripts/validate_rules.py`,
  `scripts/fun_text_processing_oracle.py`, and `scripts/cache_maintenance.py`.

## Status Legend

- `[ ]` not started
- `[~]` in progress
- `[x]` complete

## Non-Goals

- Do not reintroduce `third_party/fun_text_processing`.
- Do not add `pynini`, FAR/FST cache generation, grammar warmup, or cache
  rebuild controls to runtime or Web products.
- Do not preserve old internal import paths or add compatibility facades.
- Do not keep removed cache request options such as `cache_enabled` and
  `overwrite_cache`.
- Do not add languages or operations only because the old vendor tree happened
  to contain them. Add only public routes that have product value and explicit
  capability ownership.

## Phase Index

- [x] C0: [Baseline Inventory](todo/TODO_00_BASELINE_INVENTORY.md)
- [ ] C1: [Oracle Diff Gate](todo/TODO_01_ORACLE_DIFF_GATE.md)
- [ ] C2: [Golden Corpus Expansion](todo/TODO_02_GOLDEN_CORPUS_EXPANSION.md)
- [ ] C3: [Chinese and English Deep Parity](todo/TODO_03_ZH_EN_DEEP_PARITY.md)
- [ ] C4: [Multilingual TN Parity](todo/TODO_04_MULTILINGUAL_TN_PARITY.md)
- [ ] C5: [Multilingual ITN Parity](todo/TODO_05_MULTILINGUAL_ITN_PARITY.md)
- [ ] C6: [API Product Contract and num2words Boundary](todo/TODO_06_API_PRODUCT_CONTRACT.md)
- [ ] C7: [Performance and Robustness](todo/TODO_07_PERFORMANCE_ROBUSTNESS.md)
- [ ] C8: [Release Gate and Old Product Retirement](todo/TODO_08_RELEASE_GATE.md)

## Global Validation Gate

Run these from the repository root before closing any phase that changes code or
case data:

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

Runtime vendor audit:

```bash
rg -n "fun_text_processing|pynini|FAR|FST|GrammarWarmup|DEFAULT_GRAMMAR|GRAMMAR_WARMUP|cache_enabled|overwrite_cache|third_party" light_text_process products/light_text_process_web pyproject.toml
```

Expected result: only documentation, tests, oracle tooling, or explicit
vendor-free audit text may mention these strings. Runtime behavior must not
depend on them.

## Definition of Complete Replacement

- All public TN/ITN routes have route/category coverage that reflects common
  real usage, not just one representative fixture per category.
- Oracle comparison has no unreviewed `regression` or `unsupported-gap` for the
  public replacement surface.
- Reviewed `accepted-improvement` cases have explicit expected output and a
  short reason.
- Web/API behavior uses root `TextProcessor`, root schemas, and root
  capabilities.
- The old LightASR `products/light_text_process_web` product is retained only as
  a reference until a separate retirement decision is made.
