# Num2Words And Multilingual Policy

## Support Classes

| Class | Meaning | Current use |
| --- | --- | --- |
| Native | Implemented by first-party `light_text_process` rules and covered by golden cases. | zh/en TN and ITN. |
| Dependency-backed | Exposed through a focused dependency boundary with visible failures. | num2words via `num2words`. |
| Experimental | May exist in a branch or local prototype but is not advertised by capabilities. | None. |
| Unsupported | Not exposed and must fail visibly when requested. | Non-zh/en TN and ITN languages. |

## TN And ITN Language Policy

TN and ITN support is limited to `zh` and `en` until another language has:

- Product need and owner.
- First-party rule module or accepted dependency boundary.
- Golden cases under `data/rule_cases/`.
- Language/operation validation command in `scripts/validate_rules.py`.
- Explicit failure-mode tests for unsupported options and malformed input.

Vendored data availability is not support. The old vendor tree included more
languages, but this project does not expose them without native coverage.

## num2words Policy

num2words remains a dependency-backed surface because it is separate from TN and
ITN and already has broad language-specific converter behavior. The public
capabilities continue to discover languages, modes, and currencies from the
installed `num2words` converter set.

The engine keeps these visible failure boundaries:

- Unsupported num2words language: rejected before conversion.
- Unsupported mode for a language: rejected before conversion.
- Unsupported currency for a language: rejected before conversion.
- Malformed number input: row-level error in batch mode and `ValueError` in
  single-call mode.

## Language Priority

1. Keep zh/en TN and ITN as native, validated defaults.
2. Keep num2words dependency-backed and separate.
3. Add a non-zh/en TN/ITN language only when product demand justifies a native
   rule module and golden suite.

## Golden Case Template

Any future TN/ITN language must add a file under `data/rule_cases/` with cases
that include:

- `id`
- `operation`
- `language`
- `category`
- `input`
- `expected`
- optional `options`

The file must be wired into `scripts/validate_rules.py` and covered by unit
tests that prove unsupported languages do not silently fall back.
