# Baseline Inventory

This inventory freezes the replacement baseline before additional capability
work. It records the current public routes, golden case coverage, first-party
rule ownership, oracle reference path, and vendor audit result.

## Public Routes

Source: `light_text_process.capabilities`.

| Operation | Public languages |
| --- | --- |
| TN | `de`, `en`, `es`, `ru`, `zh` |
| ITN | `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh` |

The `num2words` operation remains separate and is not used as an implicit TN or
ITN fallback.

## Golden Case Inventory

Source: `data/rule_cases/`, 538 total cases.

| Case file | Route | Cases | Category counts |
| --- | --- | ---: | --- |
| `de_itn.json` | `itn/de` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `de_tn.json` | `tn/de` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `en_itn.json` | `itn/en` | 111 | address: 1, asr-postprocess: 34, date: 3, electronic: 13, fraction: 1, identity: 1, math: 2, measure: 19, mixed: 25, money: 3, ordinal: 2, telephone: 2, time: 5 |
| `en_tn.json` | `tn/en` | 75 | address: 1, date: 3, electronic: 12, identity: 2, math: 3, measure: 20, mixed: 19, money: 4, ordinal: 4, telephone: 2, temperature: 1, time: 4 |
| `es_itn.json` | `itn/es` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `es_tn.json` | `tn/es` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `fr_itn.json` | `itn/fr` | 13 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, roman: 1, telephone: 1, time: 1, whitelist: 1 |
| `id_itn.json` | `itn/id` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `ja_itn.json` | `itn/ja` | 16 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, name: 1, negative: 1, option: 3, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `ko_itn.json` | `itn/ko` | 13 | cardinal: 1, char: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `pt_itn.json` | `itn/pt` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `ru_itn.json` | `itn/ru` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `ru_tn.json` | `tn/ru` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `tl_itn.json` | `itn/tl` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `vi_itn.json` | `itn/vi` | 12 | cardinal: 1, date: 1, decimal: 1, electronic: 1, fraction: 1, measure: 1, money: 1, negative: 1, ordinal: 1, telephone: 1, time: 1, whitelist: 1 |
| `zh_itn.json` | `itn/zh` | 119 | address: 2, asr-postprocess: 33, date: 2, electronic: 9, fraction: 1, identity: 1, math: 2, measure: 24, mixed: 24, money: 11, ordinal: 1, phone: 2, temperature: 1, time: 6 |
| `zh_tn.json` | `tn/zh` | 71 | address: 2, date: 4, electronic: 11, identity: 1, math: 3, measure: 21, mixed: 19, money: 5, ordinal: 2, telephone: 1, temperature: 1, time: 1 |

## Owner Modules

Source: `light_text_process/runtime/native.py`,
`docs/route_ownership.md`, and route modules under `light_text_process/rules/`.

| Route group | Owner modules |
| --- | --- |
| `tn/de`, `tn/es`, `tn/ru` | `de_tn.py`, `es_tn.py`, `ru_tn.py`, shared `multilingual_tn.py` |
| `tn/en` | `en_tn.py`, `en_dates.py` |
| `tn/zh` | `zh_tn.py` |
| non-zh/en ITN | language modules plus shared `multilingual_itn.py` |
| `itn/en` | `en_itn.py` |
| `itn/zh` | `zh_itn.py` |

## Oracle Reference

Local comparison uses an external preserved vendor checkout, not runtime code:

```bash
/Users/boom/workspace/LightASR/light_funasr/third_party/fun_text_processing
```

Oracle reports and caches are generated only under ignored `runtime/oracle/`.

## Boundary Audit

Current audit commands:

```bash
.venv/bin/python scripts/validate_rules.py --list
rg -n "from fun_text_processing|import fun_text_processing|pynini|third_party" light_text_process pyproject.toml
rg -n "from fun_text_processing|import fun_text_processing|pynini|third_party|cache_enabled|overwrite_cache|GrammarWarmup|DEFAULT_GRAMMAR|GRAMMAR_WARMUP" light_text_process products/light_text_process_web pyproject.toml
```

The runtime/vendor audits returned no matches. The Web product imports root
`TextProcessor`, root schemas, and root capability metadata.
