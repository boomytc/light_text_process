# Native Cutover Release Notes

## Default Route Table

| Operation | Language | Default engine | Status |
| --- | --- | --- | --- |
| TN | zh | `light_text_process_native` | native |
| TN | en | `light_text_process_native` | native |
| ITN | zh | `light_text_process_native` | native |
| ITN | en | `light_text_process_native` | native |
| num2words | installed converter languages | `num2words` | dependency-backed |

No non-zh/en TN or ITN route is supported. Requests for unsupported TN/ITN
languages fail before reaching any runtime engine.

## Fallback Policy

No supported default TN/ITN route requires a fallback engine after P8. The
engine boundary remains for tests and future experiments, but production
`TextProcessor` instances use `light_text_process_native` directly.

## Dependency Cleanup Plan

P8 removed dependencies that only existed for the vendored grammar backend:

- `pynini`
- `joblib`
- `tqdm`
- vendor package discovery and package data
- vendor-specific FAR/FST cache commands

The following dependencies remain required after cutover:

- `num2words` for the separate number-to-words surface.
- `pydantic` for request/response schemas.
No first-party runtime dependency currently requires `inflect`, `PyYAML`, or
`regex`.

## Cache State

Native zh/en TN and ITN routes do not require FAR/FST caches. Existing files
under ignored `runtime/cache/` are transient validation artifacts and can be
removed. Vendor-specific cache commands have been retired.

## Known Limits

- Native output is validated against the current golden suite.
- num2words remains dependency-backed and intentionally separate from TN/ITN.
- Non-zh/en TN/ITN languages are unsupported until first-party rules and golden
  cases are added.

## Final Removal Status

- Vendored runtime adapter removed.
- `third_party/fun_text_processing` removed from the project tree.
- Vendor package discovery, package data, and vendor-only dependencies removed.
- Architecture tests reject vendor imports.
