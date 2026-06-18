# TODO 08: Release Gate and Old Product Retirement

## Purpose

Define the evidence required before saying `light_text_process` fully replaces
the former `fun_text_processing` capability surface and before considering the
old LightASR Web product removable.

## Release Gate Tasks

- [ ] C0 through C7 are complete.
- [ ] Full rule validation passes.
- [ ] Full unit test suite passes.
- [ ] Oracle comparison strict mode has no unreviewed `regression`.
- [ ] Oracle comparison strict mode has no unreviewed `unsupported-gap`.
- [ ] Every accepted improvement has explicit expected output and reason.
- [ ] `docs/replacement_matrix.md` reflects final route/category status.
- [ ] `docs/route_ownership.md` reflects final owner modules.
- [ ] Web product examples match current root engine output.
- [ ] Vendor audit confirms runtime code has no vendor coupling.
- [ ] Release notes describe customer-visible behavior changes.
- [ ] Old LightASR product retirement is proposed separately with evidence,
  not bundled into rule coverage work.

## Final Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python scripts/fun_text_processing_oracle.py compare --reference /path/to/fun_text_processing --strict
rg -n "from fun_text_processing|import fun_text_processing|pynini|FAR|FST|GrammarWarmup|DEFAULT_GRAMMAR|GRAMMAR_WARMUP|cache_enabled|overwrite_cache|third_party" light_text_process products/light_text_process_web pyproject.toml
```

## Completion Criteria

- The replacement claim is backed by validation output, oracle diff evidence,
  docs, and product smoke checks.
- No compatibility-era implementation remains hidden in runtime code.
- No over-broad unsupported routes or options are exposed.
- The old LightASR product can be archived only after a separate explicit
  decision.

## Non-Goals

- Do not delete the old LightASR product as part of this phase automatically.
- Do not make release success depend on matching low-quality vendor quirks.
- Do not expand scope beyond public TN/ITN replacement capability.
