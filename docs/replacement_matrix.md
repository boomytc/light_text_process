# Replacement Matrix

This matrix records the first-party replacement coverage for the former
`fun_text_processing` TN/ITN surface. Runtime code is vendor-free: every public
TN/ITN route is served by `light_text_process_native` rule modules.

The frozen replacement baseline is recorded in
[`docs/baseline_inventory.md`](baseline_inventory.md), including route lists,
case counts, category coverage, owner modules, oracle reference path, and
runtime vendor audit commands.

## Status Values

- `covered`: first-party rule code, route/category golden cases, and the
  `scripts/validate_rules.py` coverage gate cover the category.
- `intentional-delta`: first-party output is deliberately stronger than the
  former route and representative fixtures carry `oracle_status:
  accepted-improvement`.

## Public Routes

- TN: `de`, `en`, `es`, `ru`, `zh`
- ITN: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh`

The tracked category vocabulary is: cardinal, ordinal, decimal, date, time,
money, measure, telephone, electronic, fraction, range, roman, whitelist, word,
punctuation, and language-specific character or name handling. Ordinary-text
negative cases are included to prevent broad regex substitutions.

## TN Coverage

| Route | Owner module | Coverage status |
| --- | --- | --- |
| `tn/de` | `light_text_process/rules/de_tn.py`, `multilingual_tn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `tn/en` | `light_text_process/rules/en_tn.py` | `covered`: date, time, money, measure, telephone, electronic, fraction, ordinal, range, roman, punctuation, address, identity, math, mixed ASR/product tokens. `intentional-delta`: technical identifiers, file paths, social handles, and product-token behavior. |
| `tn/es` | `light_text_process/rules/es_tn.py`, `multilingual_tn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `tn/ru` | `light_text_process/rules/ru_tn.py`, `multilingual_tn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `tn/zh` | `light_text_process/rules/zh_tn.py` | `covered`: date, time, money, measure, telephone, electronic, punctuation, address, identity, math, mixed ASR/product tokens. `intentional-delta`: technical identifiers, file paths, social handles, and product-token behavior. |

## ITN Coverage

| Route | Owner module | Coverage status |
| --- | --- | --- |
| `itn/de` | `light_text_process/rules/de_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/en` | `light_text_process/rules/en_itn.py` | `covered`: cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, address, identity, math, mixed ASR cleanup, product tokens. `intentional-delta`: technical identifiers, file paths, social handles, and product-token behavior. |
| `itn/es` | `light_text_process/rules/es_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/fr` | `light_text_process/rules/fr_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, roman, telephone, time, whitelist, negative ordinary text. |
| `itn/id` | `light_text_process/rules/id_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/ja` | `light_text_process/rules/ja_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, name-preservation, ordinal, telephone, time, whitelist, `enable_standalone_number`, `enable_0_to_9`, negative ordinary text. |
| `itn/ko` | `light_text_process/rules/ko_itn.py`, `multilingual_itn.py` | `covered`: cardinal, char-preservation, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/pt` | `light_text_process/rules/pt_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/ru` | `light_text_process/rules/ru_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/tl` | `light_text_process/rules/tl_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/vi` | `light_text_process/rules/vi_itn.py`, `multilingual_itn.py` | `covered`: cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, negative ordinary text. |
| `itn/zh` | `light_text_process/rules/zh_itn.py` | `covered`: cardinal, char, date, electronic, fraction, math, measure, money, telephone/phone, time, address, identity, mixed ASR cleanup, product tokens. `intentional-delta`: technical identifiers, file paths, social handles, and product-token behavior. |

## Validation Contract

- `scripts/validate_rules.py` defaults to a full route/category coverage gate
  before running selected cases.
- `scripts/validate_rules.py --language ... --operation ... --category ...`
  still runs focused subsets for route/category triage.
- `scripts/fun_text_processing_oracle.py compare --strict` fails only
  `regression` and `unsupported-gap`; reviewed `accepted-improvement` cases are
  allowed by strict mode.
- Complete replacement requires a clean validation pass and no runtime
  `fun_text_processing`, `third_party`, FAR/FST cache, or compatibility-shim
  coupling.
