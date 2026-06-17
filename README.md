# Light Text Process

Standalone Python engine for text normalization (TN), inverse text normalization (ITN), and multilingual number-to-words conversion.

This repository is the standalone `light_text_process` engine. zh/en TN and ITN
use first-party native routes, while the full vendored `fun_text_processing`
backend remains available for multilingual TN/ITN routes that have not yet been
integrated into first-party code. Product-owned rules live in
`light_text_process/rules`, runtime adapters live in
`light_text_process/runtime`, and golden regression cases live in
`data/rule_cases`.

## Setup

```bash
uv venv --python 3.12
uv pip install -e .
```

## Usage

```python
from light_text_process import TextProcessor

processor = TextProcessor()
print(processor.normalize_text("日期 2026-06-15。", "zh").output)
print(processor.inverse_normalize_text("二零二六年六月十五日", "zh").output)
print(processor.number_to_words("123", "en").output)
```

## Architecture

- `light_text_process/processor.py` exposes the public engine API.
- `light_text_process/rules/` contains owned zh/en TN/ITN supplemental rules.
- `light_text_process/runtime/` contains runtime adapters and the engine boundary.
- `third_party/fun_text_processing/` is the temporary preserved grammar backend
  for routes not yet integrated into first-party code.
- `data/rule_cases/` is the golden regression suite for zh/en TN/ITN behavior.
- `scripts/validate_rules.py` runs the golden suite.
- `scripts/cache_maintenance.py` inspects and maintains project-local grammar
  caches.
- `docs/vendor_replacement_roadmap.md` describes the transition from retained
  vendor baseline to final vendor removal.

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/cache_maintenance.py status
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

## Direction

The final target is to replace every current `third_party/fun_text_processing`
TN/ITN route with first-party `light_text_process` routes. During the
transition, zh/en use native routes and non-migrated vendor languages continue
through `fun_text_processing` fallback so existing coverage is not lost.
num2words remains a separate dependency-backed surface.
