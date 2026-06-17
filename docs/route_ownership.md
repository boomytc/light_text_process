# Route Ownership Plan

This file assigns first-party ownership, migration priority, and minimum
golden coverage for every non-zh/en route currently served by the temporary
`fun_text_processing` backend.

## Ownership Rules

- TN and ITN routes have separate owner modules.
- Route modules live under `light_text_process/rules/` and do not import
  runtime adapters or vendor packages.
- Shared helpers may cover neutral parsing or formatting primitives, but route
  behavior stays language and operation scoped.
- Public capabilities keep each route visible until its first-party owner is
  active.
- Japanese ITN keeps `enable_standalone_number` and `enable_0_to_9` behavior
  until the first-party route supports equivalent options.

## TN Routes

| Route | Owner module | Priority | Minimum golden coverage |
| --- | --- | --- | --- |
| `tn:de` | `light_text_process/rules/de_tn.py` | P1 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `tn:es` | `light_text_process/rules/es_tn.py` | P1 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `tn:ru` | `light_text_process/rules/ru_tn.py` | P2 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |

## ITN Routes

| Route | Owner module | Priority | Minimum golden coverage |
| --- | --- | --- | --- |
| `itn:de` | `light_text_process/rules/de_itn.py` | P1 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:es` | `light_text_process/rules/es_itn.py` | P1 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:fr` | `light_text_process/rules/fr_itn.py` | P2 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal, roman |
| `itn:id` | `light_text_process/rules/id_itn.py` | P3 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:ja` | `light_text_process/rules/ja_itn.py` | P2 | cardinal, standalone-number options, date, time, money, measure, telephone, electronic, ordinal |
| `itn:ko` | `light_text_process/rules/ko_itn.py` | P3 | cardinal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:pt` | `light_text_process/rules/pt_itn.py` | P2 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:ru` | `light_text_process/rules/ru_itn.py` | P2 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:tl` | `light_text_process/rules/tl_itn.py` | P3 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |
| `itn:vi` | `light_text_process/rules/vi_itn.py` | P3 | cardinal, decimal, date, time, money, measure, telephone, electronic, ordinal |

## Migration Order

1. Complete zh/en native parity without runtime vendor imports.
2. Migrate P1 TN and ITN routes: `tn:de`, `tn:es`, `itn:de`, `itn:es`.
3. Migrate P2 routes: `tn:ru`, `itn:fr`, `itn:ja`, `itn:pt`, `itn:ru`.
4. Migrate P3 routes: `itn:id`, `itn:ko`, `itn:tl`, `itn:vi`.
5. Remove the vendor runtime, vendor tree, package metadata, and grammar-cache
   assumptions after every listed route is first-party active.
