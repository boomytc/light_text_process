# TODO 06: Route Migration

## Objective

Migrate approved routes one language/operation pair at a time from vendor code
to first-party `light_text_process` rules.

## Required Work

- [x] Create focused first-party modules for each approved route.
- [x] Keep TN and ITN migration separate; do not merge rule surfaces.
- [x] Add route-specific golden cases before implementation changes.
- [x] Add operation-scoped validators for each migrated language.
- [x] Switch default routing route by route, not as a broad repository cutover.
- [x] Keep vendor fallback only for routes that are still explicitly marked
      vendor-backed.
- [x] Confirm migrated routes do not read vendor TSV/TXT/FAR/FST assets.

## Acceptance

- [x] Each migrated route passes its golden suite without vendor imports.
- [x] Each migrated route has documented intentional output differences, if any.
- [x] Non-migrated routes keep their previous behavior until their own decision
      or migration phase.
