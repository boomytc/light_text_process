# Replacement Matrix

This matrix records the first-party replacement target for the former
`fun_text_processing` TN/ITN surface. Runtime code is vendor-free: coverage gaps
are tracked as first-party work, not as fallback or compatibility behavior.

## Status Values

- `covered`: first-party rule code and golden cases cover the category.
- `partial`: first-party behavior exists, but coverage is narrower than the
  former route/category target.
- `missing`: the category is part of the former route target and has no focused
  first-party coverage yet.
- `intentional-delta`: first-party output is deliberately different and must be
  documented in oracle diff classification.

## Former Public Routes

- TN: `de`, `en`, `es`, `ru`, `zh`
- ITN: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh`

The target category vocabulary is: cardinal, ordinal, decimal, date, time,
money, measure, telephone, electronic, fraction, range, roman, whitelist, word,
punctuation, and language-specific character or name handling.

## TN Coverage Baseline

| Route | Owner module | Former categories | Current category status |
| --- | --- | --- | --- |
| `tn/de` | `light_text_process/rules/de_tn.py`, `multilingual_tn.py` | cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, word | `covered`: cardinal, decimal, date, electronic, money, time. `partial`: word. `missing`: fraction, measure, ordinal, telephone. |
| `tn/en` | `light_text_process/rules/en_tn.py` | abbreviation, cardinal, date, decimal, electronic, fraction, measure, money, ordinal, range, roman, telephone, time, whitelist, word | `covered`: date, time, money, measure, telephone, electronic, fraction, ordinal, range, roman, punctuation, word/product-token behavior. `intentional-delta`: ASR and technical-token handling beyond former vendor behavior. |
| `tn/es` | `light_text_process/rules/es_tn.py`, `multilingual_tn.py` | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal, decimal, date, electronic, money, time. `partial`: word. `missing`: fraction, measure, ordinal, telephone, whitelist. |
| `tn/ru` | `light_text_process/rules/ru_tn.py`, `multilingual_tn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal, decimal, date, electronic, money, time. `partial`: word. `missing`: measure, ordinal, telephone, whitelist. |
| `tn/zh` | `light_text_process/rules/zh_tn.py` | cardinal, char, date, electronic, measure, money, sport, telephone, time, whitelist, word | `covered`: date, time, money, measure, telephone, electronic, punctuation, math, word/product-token behavior. `intentional-delta`: ASR and mixed technical-token handling beyond former vendor behavior. |

## ITN Coverage Baseline

| Route | Owner module | Former categories | Current category status |
| --- | --- | --- | --- |
| `itn/de` | `light_text_process/rules/de_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, word. |
| `itn/en` | `light_text_process/rules/en_itn.py` | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist/product tokens, word cleanup. `intentional-delta`: ASR cleanup and technical identifiers beyond former vendor behavior. |
| `itn/es` | `light_text_process/rules/es_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/fr` | `light_text_process/rules/fr_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word, roman | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, fraction, measure, money, ordinal, telephone, time, whitelist, word, roman. |
| `itn/id` | `light_text_process/rules/id_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/ja` | `light_text_process/rules/ja_itn.py`, `multilingual_itn.py` | cardinal, char, date, decimal, electronic, fraction, measure, money, name, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `partial`: `enable_standalone_number`, `enable_0_to_9` options are exposed but not behaviorally distinct yet. `missing`: date, decimal, fraction, measure, money, name, ordinal, telephone, time, whitelist, word. |
| `itn/ko` | `light_text_process/rules/ko_itn.py`, `multilingual_itn.py` | cardinal, char, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/pt` | `light_text_process/rules/pt_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/ru` | `light_text_process/rules/ru_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/tl` | `light_text_process/rules/tl_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/vi` | `light_text_process/rules/vi_itn.py`, `multilingual_itn.py` | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | `covered`: cardinal digit sequences, electronic. `missing`: date, decimal, fraction, measure, money, ordinal, telephone, time, whitelist, word. |
| `itn/zh` | `light_text_process/rules/zh_itn.py` | cardinal, char, date, electronic, fraction, math, measure, money, sport, telephone, time, whitelist, word | `covered`: cardinal, char, date, electronic, fraction, math, measure, money, telephone, time, whitelist/product tokens, word cleanup. `intentional-delta`: ASR cleanup and mixed technical-token handling beyond former vendor behavior. |

## Gap Summary

- Non-zh/en ITN must move beyond digit-sequence cardinal and electronic smoke
  coverage into decimal, date, time, money, measure, telephone, ordinal,
  fraction where applicable, whitelist, and negative cases.
- Non-zh/en TN must split the existing mixed smoke cases into category-specific
  golden cases and add missing measure, telephone, ordinal, fraction, and
  whitelist coverage where applicable.
- Japanese ITN option behavior for standalone numbers and 0-to-9 handling must
  be proven with dedicated cases.
- zh/en accepted differences must be classified as reviewed deltas in oracle
  output, not hidden as generic mismatches.

## Release Gate

Complete replacement can only be claimed when this matrix has no `missing` or
unexplained `partial` category, rule validation passes for all route/category
fixtures, strict oracle comparison has no `regression` or `unsupported-gap`, and
runtime code still has no `fun_text_processing` dependency or package-data
coupling.
