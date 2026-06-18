# TODO 06: Cutover and Cleanup

## Objective

Finish the rebuild by making the native product the only active Light Text
Process Web implementation.

## Tasks

- [ ] Compare endpoint behavior against the old LightASR product for the current
  representative samples.
- [ ] Treat intentional native improvements as new behavior, not compatibility
  regressions, when they are already covered by root rule cases.
- [ ] Update README files to point users to
  `/Users/boom/workspace/light_text_process/products/light_text_process_web`.
- [ ] Remove or clearly retire the old LightASR product copy once the new product
  passes validation.
- [ ] Do not keep two active Web products with the same purpose.
- [ ] Delete any temporary migration notes that are no longer actionable.
- [ ] Delete TODO files after their phases are complete and reflected in stable
  docs/tests.

## Final Forbidden Runtime Audit

From the new product directory, these searches should return no runtime-code
matches:

```bash
rg -n "fun_text_processing|pynini|FAR|FST|GrammarWarmup|DEFAULT_GRAMMAR|GRAMMAR_WARMUP|cache_enabled|overwrite_cache|TextProcessingService|core\.runtime|core\.rules|third_party" app.py api tests static templates pyproject.toml README.md AGENTS.md
```

Allowed references after cutover:

- Historical notes in completed migration docs, if they remain useful.
- Root-level oracle tooling that compares against an external reference package.
- No runtime code, product dependency metadata, UI request payload, or product
  test should depend on those names.

## Final Acceptance Gate

- [ ] Root engine tests pass.
- [ ] Root rule validation passes.
- [ ] Product tests pass.
- [ ] Product HTTP smoke checks pass.
- [ ] Product has no copied engine source.
- [ ] Product has no `third_party/` directory.
- [ ] Product has no product-local rule cases.
- [ ] Product docs explain current architecture without migration-era language.
- [ ] Worktree contains only intentional source/docs changes.
