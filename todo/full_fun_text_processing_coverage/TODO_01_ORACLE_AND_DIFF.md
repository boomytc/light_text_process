# TODO 01: Oracle And Differential Checks

## Objective

Create repeatable comparison evidence against the former `fun_text_processing`
behavior without reintroducing it into runtime code.

## Required Work

- [x] Define an oracle source for former vendor behavior as an explicit
      external `fun_text_processing` package path passed with `--reference`.
- [x] Keep the oracle outside runtime imports, package data, and public
      dependency surfaces.
- [x] Add a script that compares current native output with oracle output for
      selected route/category fixtures.
- [x] Store differential reports under ignored `runtime/oracle/` output paths by
      default.
- [ ] Add reviewed classification for diffs as `match`,
      `accepted-improvement`, `regression`, or `unsupported-gap`.
- [x] Make the differential checker support operation, language, category, and
      fixture-file filters.

## Acceptance

- [x] Differential checks can run without importing vendor modules from
      `light_text_process` runtime code.
- [x] At least one TN route and one ITN route have comparison reports.
- [x] Diff output is structured enough to drive route/category TODO work.
- [x] Regressions and unsupported gaps fail visibly in strict mode.

## Usage

Use the external reference path explicitly:

```bash
.venv/bin/python scripts/fun_text_processing_oracle.py compare \
  --reference /path/to/fun_text_processing \
  --case itn-de-digit-sequence \
  --strict
```

Reports default to ignored `runtime/oracle/fun_text_processing_diff.json`.
