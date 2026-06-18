# TODO 05: Multilingual ITN Parity

## Purpose

Bring non-zh/en public ITN routes to replacement-grade coverage for the former
vendor ITN surface.

## Public ITN Routes

- `de`
- `es`
- `fr`
- `id`
- `ja`
- `ko`
- `pt`
- `ru`
- `tl`
- `vi`

`en` and `zh` are tracked in `TODO_03_ZH_EN_DEEP_PARITY.md`.

## Route Tasks

For each public ITN route:

- [ ] Cover cardinal, decimal, ordinal, date, time, money, measure, telephone,
  electronic, fraction, whitelist, and negative ordinary-text cases.
- [ ] Add route-specific character, roman numeral, or name-preservation cases
  when the language needs them.
- [ ] Add noisy ASR-style inputs where the product is likely to process speech
  transcripts.
- [ ] Compare route output against the oracle.
- [ ] Classify every output difference as match, accepted improvement,
  regression, or unsupported gap.
- [ ] Fix regressions before expanding lower-priority categories.

## Language-Specific Checks

- [ ] `fr`: roman numeral and ordinal behavior.
- [ ] `id`: common date/time/money wording and ordinary-text preservation.
- [ ] `ja`: `enable_standalone_number` and `enable_0_to_9` behavior, name
  preservation, full-width/half-width effects.
- [ ] `ko`: character preservation and common number/date forms.
- [ ] `tl` and `vi`: common ASR transcript forms and negative ordinary text.
- [ ] `de`, `es`, `pt`, `ru`: cardinal/decimal/date/money/measure forms with
  language-specific wording.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --operation itn
.venv/bin/python scripts/fun_text_processing_oracle.py compare --reference /path/to/fun_text_processing --operation itn --strict
```

## Completion Criteria

- Every public non-zh/en ITN route has meaningful route/category coverage.
- Japanese option behavior is covered by golden cases and service tests.
- Oracle comparison has no unreviewed regression or unsupported gap.
- Unsupported public behavior fails visibly rather than falling through.

## Non-Goals

- Do not expose ITN routes that are not in `light_text_process.capabilities`.
- Do not add language-wide transliteration features unless they replace a public
  ITN behavior.
- Do not preserve vendor output when native output is reviewed and better.
