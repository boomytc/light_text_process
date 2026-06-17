# TODO 05: Language Support Decisions

## Objective

Decide the future of every non-zh/en vendor route before removing the vendor
tree.

## Required Work

- [ ] For each TN route `de`, `es`, and `ru`, decide whether to replace,
      retire, or defer.
- [ ] For each ITN route `de`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`,
      and `vi`, decide whether to replace, retire, or defer.
- [ ] If a route will be replaced, define minimal golden coverage and first-party
      module ownership.
- [ ] If a route will be retired, update capability policy and document the
      breaking change before removing vendor.
- [ ] Preserve language-specific options only when the route remains public.

## Acceptance

- [ ] No public route depends on an implicit vendor-only promise.
- [ ] `light_text_process/capabilities.py` matches the accepted future route
      policy.
- [ ] Unsupported language tests cover every retired route.
