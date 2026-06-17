# TODO 05: Non-Zh/En Route Ownership

## Objective

Define ownership, priority, and golden coverage for every non-zh/en vendor
route so that no existing `fun_text_processing` capability is lost during
replacement.

## Required Work

- [ ] For each TN route `de`, `es`, and `ru`, assign first-party module
      ownership and migration priority.
- [ ] For each ITN route `de`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`,
      and `vi`, assign first-party module ownership and migration priority.
- [ ] Define minimal golden coverage for each route before implementation work.
- [ ] Preserve language-specific options such as Japanese standalone-number
      toggles until first-party replacements support them.
- [ ] Keep all current vendor routes in public capabilities until their
      first-party replacements are active.

## Acceptance

- [ ] Every current vendor route stays in public capabilities until its
      first-party replacement is active.
- [ ] `light_text_process/capabilities.py` continues to expose all current
      vendor TN/ITN languages during the transition.
- [ ] Each route has a concrete first-party migration owner and test plan.
