# TODO 01: Public Capabilities

## Objective

Keep the current public capability surface aligned with the vendor backend
while replacement scope is still being decided.

## Required Work

- [x] Expose vendor TN languages: `de`, `en`, `es`, `ru`, `zh`.
- [x] Expose vendor ITN languages: `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`,
      `pt`, `ru`, `tl`, `vi`, `zh`.
- [x] Keep Japanese ITN standalone-number options visible in language-scoped
      metadata.
- [x] Keep TN unsupported-language failures visible for languages not supported
      by vendor TN, such as `ja`.
- [x] Keep ITN unsupported-language failures visible for languages outside the
      vendor set.

## Acceptance

- [x] Capability unit tests assert the restored language coverage.
- [x] Service tests prove non-zh/en vendor languages can pass the public
      language gate.
- [x] Future replacement of any public vendor route is handled by its explicit
      ownership and migration phase.
