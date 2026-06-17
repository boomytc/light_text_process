# TODO 05: Language Support Decisions

## Objective

Decide the future of every non-zh/en vendor route before removing the vendor
tree.

## Required Work

- [x] For each TN route `de`, `es`, and `ru`, decide whether to replace,
      retire, or defer.
- [x] For each ITN route `de`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`,
      and `vi`, decide whether to replace, retire, or defer.
- [x] If a route will be replaced, define minimal golden coverage and first-party
      module ownership.
- [x] If a route will be retired, update capability policy and document the
      breaking change before removing vendor.
- [x] Preserve language-specific options only when the route remains public.

## Acceptance

- [x] No public route depends on an implicit vendor-only promise.
- [x] `light_text_process/capabilities.py` matches the accepted future route
      policy.
- [x] Unsupported language tests cover every retired route.
