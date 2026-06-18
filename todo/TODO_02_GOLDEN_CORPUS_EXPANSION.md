# TODO 02: Golden Corpus Expansion

## Purpose

Grow the test corpus from representative coverage to replacement-grade coverage
for the public `fun_text_processing` TN/ITN surface.

## Current Case Baseline

- `de_tn`: 12
- `de_itn`: 12
- `en_tn`: 75
- `en_itn`: 111
- `es_tn`: 12
- `es_itn`: 12
- `fr_itn`: 13
- `id_itn`: 24
- `ja_itn`: 16
- `ko_itn`: 13
- `pt_itn`: 12
- `ru_tn`: 12
- `ru_itn`: 12
- `tl_itn`: 12
- `vi_itn`: 12
- `zh_tn`: 71
- `zh_itn`: 119

## Tasks

- [ ] For each public route, list required categories and current category
  counts.
- [ ] Expand non-zh/en route coverage beyond one representative case per
  category.
- [ ] Add ordinary-text negative cases for every route so broad substitutions do
  not corrupt normal text.
- [ ] Add boundary cases for punctuation, whitespace, full-width/half-width
  characters, mixed scripts, and casing where relevant.
- [ ] Add ASR-like noisy text for routes that are used downstream from speech
  recognition.
- [ ] Add common product text: model names, file names, paths, versions, email,
  URL, handles, IDs, license-like strings, and metrics.
- [ ] Add case comments only as structured fields such as `oracle_note`; do not
  add prose-only expectations that tests cannot validate.
- [ ] Keep case IDs stable and route-prefixed.
- [ ] Keep expected outputs deterministic.

## Category Targets

Use these as minimum public-surface categories, not as a request to implement
all vendor internals:

- TN: cardinal, decimal, ordinal, date, time, money, measure, telephone,
  electronic, fraction, whitelist, punctuation, negative.
- ITN: cardinal, decimal, ordinal, date, time, money, measure, telephone,
  electronic, fraction, whitelist, negative.
- Route-specific additions: roman, char/name preservation, ASR postprocess,
  address, identity, math, mixed product tokens.

## Completion Criteria

- Every public route has enough fixtures to expose common formatting variants,
  not just category presence.
- `scripts/validate_rules.py` coverage gate reflects the intended category
  vocabulary.
- New corpus entries do not require vendor runtime imports.
- New corpus entries do not add unsupported public routes by accident.

## Non-Goals

- Do not add case volume for obscure categories without observed product value.
- Do not turn examples into runtime configuration.
- Do not use golden cases to freeze low-quality vendor behavior.
