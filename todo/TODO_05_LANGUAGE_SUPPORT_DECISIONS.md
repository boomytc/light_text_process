# TODO 05: Non-Zh/En Route Ownership

## Objective

Define ownership, priority, and golden coverage for every non-zh/en vendor
route so that no existing `fun_text_processing` capability is lost during
replacement.

## Required Work

- [x] For each TN route `de`, `es`, and `ru`, assign first-party module
      ownership and migration priority.
- [x] For each ITN route `de`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`,
      and `vi`, assign first-party module ownership and migration priority.
- [x] Define minimal golden coverage for each route before implementation work.
- [x] Preserve language-specific options such as Japanese standalone-number
      toggles until first-party replacements support them.
- [x] Keep all current vendor routes in public capabilities until their
      first-party replacements are active.

## Acceptance

- [x] Every current vendor route stays in public capabilities until its
      first-party replacement is active.
- [x] `light_text_process/capabilities.py` continues to expose all current
      vendor TN/ITN languages during the transition.
- [x] Each route has a concrete first-party migration owner and test plan.

## Evidence

- Route owners, priorities, option preservation, and minimum golden coverage are
  recorded in `docs/route_ownership.md`.
