# TODO 01: Oracle And Differential Checks

## Objective

Create repeatable comparison evidence against the former `fun_text_processing`
behavior without reintroducing it into runtime code.

## Required Work

- [ ] Define an oracle source for former vendor behavior, such as a historical
      checkout, archived wheel, fixture export, or one-off isolated tool.
- [ ] Keep the oracle outside runtime imports, package data, and public
      dependency surfaces.
- [ ] Add a script that compares current native output with oracle output for
      selected route/category fixtures.
- [ ] Store differential reports under ignored runtime output paths or committed
      summary docs, depending on stability.
- [ ] Classify diffs as `match`, `accepted-improvement`, `regression`, or
      `unsupported-gap`.
- [ ] Make the differential checker support operation, language, category, and
      fixture-file filters.

## Acceptance

- [ ] Differential checks can run without importing vendor modules from
      `light_text_process` runtime code.
- [ ] At least one TN route and one ITN route have comparison reports.
- [ ] Diff output is structured enough to drive route/category TODO work.
- [ ] Regressions and unsupported gaps fail visibly in strict mode.
