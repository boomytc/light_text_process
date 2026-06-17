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

- [ ] English number and ordinal verbalizers.
- [ ] Native English TN pipeline with category ordering.
- [ ] Casing behavior compatible with `input_case`.
- [ ] Project-local whitelist handling compatible with existing behavior.
- [ ] Golden and differential coverage for every enabled category.

## Suggested Category Order

- [ ] Numbers, decimals, ordinals, and fractions.
- [ ] Dates, times, AM/PM ranges, and timezones.
- [ ] Money, measures, ratings, durations, and rates.
- [ ] Addresses, pages, chapters, sections, and room codes.
- [ ] Electronic strings, URLs, email, domains, and IP addresses.
- [ ] Versions, ports, HTTP status, IDs, and mixed technical expressions.

## Detailed Tasks

- [ ] Reuse `light_text_process/rules/en_dates.py` where it already defines
      product behavior.
- [ ] Add tests for abbreviations such as page, chapter, section, apartment,
      suite, and room.
- [ ] Add tests for casing-sensitive and punctuation-sensitive options.
- [ ] Keep deterministic and non-deterministic behavior explicit. Do not expose
      non-deterministic native output until it has a clear product use.
- [ ] Preserve batch behavior and row-level error reporting.

## Acceptance Gates

- [ ] All `en/tn` golden cases pass with the native route.
- [ ] Differential comparison shows no unexplained regressions against vendor.
- [ ] Whitelist and bad path behavior remains visible and project-local.
- [ ] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language en --operation tn
.venv/bin/python -m unittest tests/test_en_tn_rule_helpers.py
.venv/bin/python -m unittest discover -s tests
```

