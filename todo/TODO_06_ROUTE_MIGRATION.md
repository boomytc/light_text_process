# TODO 06: Route Migration

## Objective

Migrate approved routes one language/operation pair at a time from vendor code
to first-party `light_text_process` rules.

## Required Work

- [ ] Create focused first-party modules for each approved route.
- [ ] Keep TN and ITN migration separate; do not merge rule surfaces.
- [ ] Add route-specific golden cases before implementation changes.
- [ ] Add operation-scoped validators for each migrated language.
- [ ] Switch default routing route by route, not as a broad repository cutover.
- [ ] Keep vendor fallback only for routes that are still explicitly marked
      vendor-backed.
- [ ] Confirm migrated routes do not read vendor TSV/TXT/FAR/FST assets.

## Acceptance

- [ ] Each migrated route passes its golden suite without vendor imports.
- [ ] Each migrated route has documented intentional output differences, if any.
- [ ] Non-migrated routes keep their previous behavior until their own decision
      or migration phase.
