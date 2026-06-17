# Replacement Matrix

This matrix records the route-level replacement scope for removing the
temporary `third_party/fun_text_processing` backend.

## Decision Values

- `replace`: keep the public route and implement it in first-party runtime code.
- `retire`: remove the route from public TN/ITN capabilities before vendor
  removal.
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
| de | cardinal, decimal, date, electronic, fraction, measure, money, ordinal, telephone, time, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| en | abbreviation, cardinal, date, decimal, electronic, fraction, measure, money, ordinal, range, roman, telephone, time, whitelist, word | dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed ASR/product tokens | TSV data, checked-in FAR files, grammar modules, FAR/FST cache generation | `data/rule_cases/en_tn.json` | replace |
| es | cardinal, date, decimals, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| ru | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| zh | cardinal, char, date, electronic, measure, money, sport, telephone, time, whitelist, word | dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed ASR/product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/zh_tn.json` | replace |

## ITN Routes

| Language | Vendor categories | First-party categories | Vendor assets/options | Golden coverage | Decision |
| --- | --- | --- | --- | --- | --- |
| de | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, word | none | grammar modules, FAR/FST cache generation | none | retire |
| en | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | ASR cleanup, dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/en_itn.json` | replace |
| es | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| fr | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word, roman | none | TSV/TXT data, grammar modules, FAR/FST cache generation | none | retire |
| id | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV/TXT data, grammar modules, FAR/FST cache generation | none | retire |
| ja | cardinal, char, date, decimal, electronic, fraction, measure, money, name, ordinal, telephone, time, whitelist, word | none | TSV/TXT data, grammar modules, FAR/FST cache generation, `enable_standalone_number`, `enable_0_to_9` | none | retire |
| ko | cardinal, char, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| pt | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| ru | cardinal, date, decimals, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | grammar modules, FAR/FST cache generation | none | retire |
| tl | cardinal, date, decimal, electronic, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| vi | cardinal, date, decimal, electronic, fraction, measure, money, ordinal, telephone, time, whitelist, word | none | TSV data, grammar modules, FAR/FST cache generation | none | retire |
| zh | cardinal, char, date, electronic, fraction, math, measure, money, sport, telephone, time, whitelist, word | ASR cleanup, dates, times, money, measures, identifiers, electronic strings, addresses, punctuation, math, mixed product tokens | TSV data, grammar modules, FAR/FST cache generation | `data/rule_cases/zh_itn.json` | replace |

## Final Public Route Policy

The vendor-free release keeps only these TN/ITN routes:

- TN: `en`, `zh`
- ITN: `en`, `zh`
- num2words: dependency-backed languages reported by `num2words`

All non-zh/en TN/ITN routes are retired because they have no first-party rule
owner, no golden coverage, and depend entirely on vendor grammars and data
assets. Retiring them is the explicit breaking change required before removing
the vendor tree.

## Migration Order

1. Make zh/en native routes pass the golden suite without importing
   `fun_text_processing`.
2. Remove non-zh/en TN/ITN routes from public capabilities and add unsupported
   language tests for retired routes.
3. Switch `TextProcessor` to the native engine for retained TN/ITN routes.
4. Delete vendor runtime files, path insertion, package metadata, vendor-only
   dependencies, and grammar cache maintenance assumptions.
