# TODO 04: Multilingual TN Parity

## Purpose

Bring non-zh/en public TN routes to replacement-grade coverage for the former
vendor TN surface.

## Public TN Routes

- `de`
- `es`
- `ru`

`en` and `zh` are tracked in `TODO_03_ZH_EN_DEEP_PARITY.md`.

## Route Tasks

For each public TN route:

- [x] Expand cardinal and decimal cases across small numbers, large numbers,
  negative numbers, and grouped numbers.
- [x] Cover ordinal forms used by the language.
- [x] Cover date and time variants that the former route handled.
- [x] Cover money with common currency symbols and decimals.
- [x] Cover measures and units with language-appropriate wording.
- [x] Cover telephone and electronic forms.
- [x] Cover fractions and ranges where supported.
- [x] Cover whitelist replacement through project-local files.
- [x] Add negative ordinary-text cases.
- [x] Compare against oracle output and classify every meaningful difference.

## Language-Specific Checks

- [x] `de`: compound number behavior, decimal separator expectations, currency
  wording, ordinal suffixes, and measurement wording.
- [x] `es`: gender-sensitive wording where public output requires it, decimal
  wording, dates, currencies, and ordinal behavior.
- [x] `ru`: number wording, decimal wording, currency and unit morphology where
  public output depends on it.

## Validation

```bash
.venv/bin/python scripts/validate_rules.py --operation tn --language de
.venv/bin/python scripts/validate_rules.py --operation tn --language es
.venv/bin/python scripts/validate_rules.py --operation tn --language ru
.venv/bin/python scripts/fun_text_processing_oracle.py compare --reference /path/to/fun_text_processing --operation tn --language de --language es --language ru --strict
```

## Completion Criteria

- Every public non-zh/en TN route has category and variant coverage.
- Oracle comparison has no unreviewed regression or unsupported gap.
- No new TN route is exposed only because vendor code had one.

## Non-Goals

- Do not implement TN routes for languages outside the public capability list
  without a separate product decision.
- Do not copy vendor grammar internals.
- Do not make `num2words` behavior a hidden substitute where route-specific
  formatting is required.
