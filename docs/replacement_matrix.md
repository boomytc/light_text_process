# Replacement Matrix

This matrix records the route-level replacement scope for removing the
temporary `third_party/fun_text_processing` backend.

## Decision Values

- `replace`: keep the public route and implement it in first-party runtime code.
- `defer`: keep the route vendor-backed only while the vendor tree still exists.

`defer` is not valid for the final vendor-free release.

## Category Legend

Vendor route directories use combinations of these major categories:
cardinal, ordinal, decimal, date, time, money, measure, telephone, electronic,
fraction, range, roman, whitelist, word, punctuation, and language-specific
character or name handling.

First-party route coverage is currently product-owned zh/en rule logic under
`light_text_process/rules/`. Golden coverage is under `data/rule_cases/` and is
limited to zh/en TN/ITN.

## TN Routes

| Language | Vendor categories | First-party categories | Vendor assets | Golden coverage | Decision |
| --- | --- | --- | --- | --- | --- |
| de | cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| en | abbreviation, cardinal, date, decimal, electronic, fraction, measure, money, ordinal, range, roman, telephone, time, whitelist, word | dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed ASR/product tokens | TSV data, checked-in FAR files, grammar modules, FAR/FST cache generation | `data/rule_cases/en_tn.json` | replace |
| es | cardinal, date, decimals, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| ru | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| zh | cardinal, char, date, electronic, measure, money, sport, telephone, time, whitelist, word | dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed ASR/product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/zh_tn.json` | replace |

## ITN Routes

| Language | Vendor categories | First-party categories | Vendor assets/options | Golden coverage | Decision |
| --- | --- | --- | --- | --- | --- |
| de | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, word | none | grammar modules, FAR/FST cache generation | none | replace |
| en | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | ASR cleanup, dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/en_itn.json` | replace |
| es | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| fr | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word, roman | none | TSV/TXT data, grammar modules, FAR/FST cache generation | none | replace |
| id | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV/TXT data, grammar modules, FAR/FST cache generation | none | replace |
| ja | cardinal, char, date, decimal, electronic, fraction, measure, money, name, ordinal, telephone, time, whitelist, word | none | TSV/TXT data, grammar modules, FAR/FST cache generation, `enable_standalone_number`, `enable_0_to_9` | none | replace |
| ko | cardinal, char, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| pt | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| ru | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | grammar modules, FAR/FST cache generation | none | replace |
| tl | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| vi | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | replace |
| zh | cardinal, char, date, electronic, fraction, math, measure, money, sport, telephone, time, whitelist, word | ASR cleanup, dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/zh_itn.json` | replace |

## Final Public Route Policy

The vendor-free release must keep these TN/ITN routes:

- TN: `de`, `en`, `es`, `ru`, `zh`
- ITN: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh`
- num2words: dependency-backed languages reported by `num2words`

No current vendor TN/ITN route is considered replaced until first-party code
preserves its public capability. Routes without first-party coverage stay
vendor-backed during the transition.

## Migration Order

1. Make zh/en native routes pass the golden suite without importing
   `fun_text_processing`.
2. Add first-party modules and golden coverage for remaining vendor TN routes.
3. Add first-party modules and golden coverage for remaining vendor ITN routes.
4. Switch `TextProcessor` route by route from vendor fallback to first-party
   implementations.
5. Delete vendor runtime files, path insertion, package metadata, vendor-only
   dependencies, and grammar cache maintenance assumptions.
