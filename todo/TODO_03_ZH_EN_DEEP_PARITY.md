# TODO 03: Chinese and English Deep Parity

## Purpose

Make `zh` and `en` TN/ITN strong enough for product use before treating the
broader multilingual replacement as complete.

## Chinese TN Tasks

- [ ] Cover common date formats: `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYY.MM.DD`,
  Chinese year/month/day, compact date, and partial date.
- [ ] Cover time formats: hour/minute, second, AM/PM-like forms when present,
  duration-like text, and mixed date-time.
- [ ] Cover money formats: RMB symbol, yuan/jiao/fen, decimals, comma grouping,
  negative amount, and range.
- [ ] Cover measure formats: temperature, length, area, volume, weight,
  percentage, speed, storage, and energy.
- [ ] Cover phone, ID-like numeric sequences, addresses, product codes, model
  names, file paths, and social handles.
- [ ] Ensure ordinary Chinese prose is not rewritten unexpectedly.

## Chinese ITN Tasks

- [ ] Cover dates, times, money, measure, phone, address, identity, math, and
  ASR cleanup cases.
- [ ] Cover mixed Arabic digits and Chinese numerals in the same sentence.
- [ ] Cover punctuation and spacing normalization without corrupting prose.
- [ ] Cover technical identifiers and product tokens as reviewed
  accepted-improvement cases when native output intentionally differs from the
  oracle.

## English TN Tasks

- [ ] Cover date variants: slash date, ISO date, month names, ordinal day, year
  reading, and date ranges.
- [ ] Cover time, duration, money, measure, percent, fraction, ordinal, roman,
  range, address, phone, email, URL, IP, file path, and product/model tokens.
- [ ] Cover casing-sensitive behavior through `input_case`.
- [ ] Cover technical identifiers without over-normalizing code-like text.

## English ITN Tasks

- [ ] Cover cardinal, ordinal, decimal, date, time, money, measure, telephone,
  electronic, fraction, address, identity, math, and ASR cleanup.
- [ ] Cover `dot`, `dash`, `slash`, `at`, and extension-like phrases.
- [ ] Cover file paths, emails, handles, and version strings only where product
  usage requires them.
- [ ] Preserve ordinary English prose.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --language zh
.venv/bin/python scripts/validate_rules.py --language en
.venv/bin/python scripts/fun_text_processing_oracle.py compare --reference /path/to/fun_text_processing --language zh --language en --strict
```

## Completion Criteria

- `zh` and `en` oracle comparison has no unreviewed regressions or unsupported
  gaps.
- Product-relevant differences from the oracle are documented as accepted
  improvements.
- Rule modules stay focused under `light_text_process/rules/`.

## Non-Goals

- Do not add a general NLP parser.
- Do not normalize code snippets, paths, or social handles unless there is a
  concrete product case.
- Do not reintroduce cache controls to reproduce vendor timing behavior.
