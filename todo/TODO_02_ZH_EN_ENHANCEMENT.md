# TODO 02: Zh/En Enhancement Layer

## Objective

Strengthen zh/en TN and ITN without removing `fun_text_processing` during the
transition phase.

## Required Work

- [x] Keep all direct vendor imports inside
      `light_text_process/runtime/fun_text_processing.py`.
- [x] Apply `zh_tn` and `en_tn` prepare helpers before vendor TN.
- [x] Apply `zh_itn` and `en_itn` prepare helpers before vendor ITN.
- [x] Apply `zh_itn` and `en_itn` finalize helpers after vendor ITN.
- [x] Preserve vendor behavior for non-zh/en languages by bypassing zh/en
      helpers.

## Acceptance

- [x] zh/en golden rule cases still run through the public `TextProcessor`.
- [x] Architecture tests allow vendor imports only in the runtime adapter.
- [x] This enhancement layer remains a bridge until zh/en routes are proven
      vendor-free.
