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

## Temporary Fallback Policy

The engine abstraction can still host a fallback engine during the migration
window, but no supported default TN/ITN route requires it after P5. The fallback
exists only as a temporary bridge until P8 removes the vendored backend and its
cache maintenance assumptions.

## Dependency Cleanup Plan

P8 can remove dependencies that only existed for the vendored grammar backend:

- `pynini`
- `joblib`
- `tqdm`
- vendor package discovery and package data
- vendor-specific FAR/FST cache commands

The following dependencies remain required after cutover:

- `num2words` for the separate number-to-words surface.
- `pydantic` for request/response schemas.
- `inflect`, `PyYAML`, and `regex` until a focused dependency audit proves they
  are unused by first-party runtime code.

## Cache State

Native zh/en TN and ITN routes do not require FAR/FST caches. Existing files
under ignored `runtime/cache/` are transient validation artifacts and can be
removed. P8 should retire vendor-specific cache commands or replace them with
native cache handling if a future native cache is introduced.

## Known Limits

- Native output is validated against the current golden suite.
- num2words remains dependency-backed and intentionally separate from TN/ITN.
- Non-zh/en TN/ITN languages are unsupported until first-party rules and golden
  cases are added.

## P8 Prerequisites

- Remove the vendored runtime adapter and `third_party/fun_text_processing`.
- Remove vendor package discovery, package data, and vendor-only dependencies.
- Update architecture tests to reject vendor imports and metadata entries.
- Clean ignored validation caches before final status reporting.
