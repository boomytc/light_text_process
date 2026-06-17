# TODO 06: Num2Words And Multilingual Expansion

## Objective

Decide how far `light_text_process` should go beyond zh/en TN and ITN, and
which num2words or multilingual surfaces should become first-party instead of
third-party pass-throughs.

## Scope

- Keep num2words separate from TN and ITN.
- Review current `num2words` dependency behavior and public language exposure.
- Decide whether non-zh/en TN/ITN languages should be native, vendor-backed,
  experimental, or unsupported.
- Avoid advertising unsupported native coverage.

## Deliverables

- [ ] Public capability policy for native, vendor-backed, experimental, and
      unsupported languages.
- [ ] Decision on whether `num2words` remains a dependency or selected language
      converters become first-party.
- [ ] Language priority list based on product value and testability.
- [ ] Golden case template for any newly exposed language.
- [ ] Documentation of language-specific dependencies and failure behavior.

## Candidate Language Review

- [ ] TN vendor languages: de, en, es, ru, zh.
- [ ] ITN vendor languages: de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh.
- [ ] num2words languages exposed by the installed `num2words` converter set.

## Detailed Tasks

- [ ] Compare vendor language coverage against actual product needs.
- [ ] Separate language support from runtime availability. A language is not
      native just because vendor data exists.
- [ ] Define golden case minimums before adding a language to
      `TN_LANGUAGES` or `ITN_LANGUAGES`.
- [ ] Review currency support and mode support for num2words languages.
- [ ] Add tests that unsupported languages and unsupported num2words modes fail
      visibly.

## Acceptance Gates

- [ ] Capabilities reflect only validated support.
- [ ] No language is marked native without golden cases and validation commands.
- [ ] num2words behavior remains separate from TN and ITN.
- [ ] Root [TODO.md](../TODO.md) phase status is updated.

## Validation

```bash
.venv/bin/python -m unittest tests/test_capabilities.py
.venv/bin/python -m unittest tests/test_services.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

