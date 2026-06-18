# TODO 04: Frontend and Examples

## Objective

Reuse the useful Web UI shape from the LightASR product while aligning all
client requests with the native engine schemas.

## Tasks

- [ ] Port `templates/index.html` and `templates/partials/capabilities.html`
  as product UI assets, not engine assets.
- [ ] Port checked-in CSS, JS, HTMX, and examples data as needed.
- [ ] Remove `cache_enabled` and `overwrite_cache` from `static/js/app.js` API
  samples and request builders.
- [ ] Remove UI branches that display or submit grammar-cache rebuild state.
- [ ] Use `/api/v1/capabilities` as the source of operation/language/mode data.
- [ ] Ensure the language selectors handle the native package's wider TN/ITN
  language surface.
- [ ] Keep examples separate from rule golden cases; examples are UI/demo data,
  not regression truth.
- [ ] Refresh `static/data/examples.json` so every listed example is supported
  by native `TextProcessor`.
- [ ] Keep API sample payloads aligned with `light_text_process.schemas`.
- [ ] Keep the UI implementation plain and local; do not introduce SPA routing,
  a frontend build pipeline, or generated API clients.

## Product Experience To Preserve

- [ ] Single-page text processing workflow.
- [ ] Operation switcher for TN, ITN, and num2words.
- [ ] Batch input and per-row output/error reporting.
- [ ] Capabilities/metadata panel.
- [ ] API sample preview.
- [ ] Local static assets; no CDN dependency for normal startup.

## Acceptance Gate

- [ ] Browser request payloads match native schemas exactly.
- [ ] The UI exposes no cache controls.
- [ ] The UI does not imply `fun_text_processing` or FAR/FST behavior.
- [ ] Text labels describe product behavior, not migration history.
