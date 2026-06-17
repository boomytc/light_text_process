# TODO 05: English TN Native

## Objective

Build native English text normalization while preserving the public options and
deterministic behavior currently provided by the vendor-backed route.

## Scope

- English written forms to readable spoken forms.
- Numbers, ordinals, dates, times, money, measures, fractions, ranges,
  temperatures, addresses, electronic strings, identifiers, and punctuation.
- `TNOptions` compatibility.

## Deliverables

- [x] English number and ordinal verbalizers.
- [x] Native English TN pipeline with category ordering.
- [x] Casing behavior compatible with `input_case`.
- [x] Project-local whitelist handling compatible with existing behavior.
- [x] Golden and differential coverage for every enabled category.

## Suggested Category Order

- [x] Numbers, decimals, ordinals, and fractions.
- [x] Dates, times, AM/PM ranges, and timezones.
- [x] Money, measures, ratings, durations, and rates.
- [x] Addresses, pages, chapters, sections, and room codes.
- [x] Electronic strings, URLs, email, domains, and IP addresses.
- [x] Versions, ports, HTTP status, IDs, and mixed technical expressions.

## Detailed Tasks

- [x] Reuse `light_text_process/rules/en_dates.py` where it already defines
      product behavior.
- [x] Add tests for abbreviations such as page, chapter, section, apartment,
      suite, and room.
- [x] Add tests for casing-sensitive and punctuation-sensitive options.
- [x] Keep deterministic and non-deterministic behavior explicit. Do not expose
      non-deterministic native output until it has a clear product use.
- [x] Preserve batch behavior and row-level error reporting.

## Acceptance Gates

- [x] All `en/tn` golden cases pass with the native route.
- [x] Differential comparison shows no unexplained regressions against vendor.
- [x] Whitelist and bad path behavior remains visible and project-local.
- [x] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language en --operation tn
.venv/bin/python -m unittest tests/test_en_tn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```
