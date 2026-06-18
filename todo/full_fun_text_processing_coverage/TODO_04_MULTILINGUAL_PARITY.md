# TODO 04: Multilingual Parity

## Objective

Raise non-zh/en routes from smoke-level native behavior to meaningful coverage
of the former `fun_text_processing` multilingual grammars.

## Required Work

- [x] Replace digit-sequence-only ITN coverage with cardinal and decimal phrase
      parsing for every non-zh/en ITN route.
- [x] Add money, date, time, measure, telephone, electronic, ordinal, fraction,
      and whitelist cases where the former vendor route supported them.
- [x] Add language-specific morphology and formatting rules where required,
      especially for German, Spanish, Russian, French, Japanese, Korean,
      Portuguese, Tagalog, Vietnamese, and Indonesian.
- [x] Support Japanese ITN option behavior for standalone numbers and 0-to-9
      handling.
- [x] Add negative cases to prevent broad regex substitutions from corrupting
      ordinary text.
- [x] Document route-specific limitations only as temporary gaps, not as full
      coverage.

## Acceptance

- [x] Non-zh/en ITN handles more than spoken digit sequences.
- [x] Non-zh/en TN handles category-level text beyond number/date/email smoke
      cases.
- [x] Each non-zh/en route has category coverage comparable to its former
      vendor route.
- [x] Remaining gaps are tracked by route and category.
