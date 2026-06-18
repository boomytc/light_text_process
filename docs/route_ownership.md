# Route Ownership Plan

This file assigns first-party ownership, migration priority, and minimum
golden coverage for every non-zh/en route that replaced the former
`fun_text_processing` backend.

## Ownership Rules

- TN and ITN routes have separate owner modules.
- Route modules live under `light_text_process/rules/` and do not import
  runtime adapters or vendor packages.
- Shared helpers may cover neutral parsing or formatting primitives, but route
  behavior stays language and operation scoped.
- Public capabilities stay aligned with active first-party owner modules.
- Japanese ITN supports `enable_standalone_number` and `enable_0_to_9` through
  first-party route options.

## TN Routes

| Route | Owner module | Priority | Minimum golden coverage |
| --- | --- | --- | --- |
| `tn:de` | `light_text_process/rules/de_tn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `tn:es` | `light_text_process/rules/es_tn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `tn:ru` | `light_text_process/rules/ru_tn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |

## ITN Routes

| Route | Owner module | Priority | Minimum golden coverage |
| --- | --- | --- | --- |
| `itn:de` | `light_text_process/rules/de_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:es` | `light_text_process/rules/es_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:fr` | `light_text_process/rules/fr_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, roman, whitelist, negative |
| `itn:id` | `light_text_process/rules/id_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:ja` | `light_text_process/rules/ja_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, name, whitelist, standalone-number options, negative |
| `itn:ko` | `light_text_process/rules/ko_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, char, whitelist, negative |
| `itn:pt` | `light_text_process/rules/pt_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:ru` | `light_text_process/rules/ru_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:tl` | `light_text_process/rules/tl_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |
| `itn:vi` | `light_text_process/rules/vi_itn.py` | Complete | cardinal, decimal, date, time, money, measure, telephone, electronic, fraction, ordinal, whitelist, negative |

## Current Gate

`scripts/validate_rules.py` enforces the current route/category minimums before
running the full golden suite. Focused triage can still run by filtering
operation, language, category, or case id.
