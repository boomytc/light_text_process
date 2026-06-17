# Light Text Process

Standalone Python engine for text normalization (TN), inverse text normalization (ITN), and multilingual number-to-words conversion.

This repository is the standalone `light_text_process` engine. Public TN and
ITN routes use first-party native code, and multilingual number-to-words remains
dependency-backed through `num2words`. Product-owned rules live in
`light_text_process/rules`, runtime adapters live in `light_text_process/runtime`,
and golden regression cases live in `data/rule_cases`.

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
- `light_text_process/rules/` contains owned TN/ITN rule modules.
- `light_text_process/runtime/` contains runtime adapters and the engine boundary.
- `data/rule_cases/` is the golden regression suite for public TN/ITN behavior.
- `scripts/validate_rules.py` runs the golden suite.
- `scripts/cache_maintenance.py` reports the vendor-free cache policy.
- `docs/vendor_replacement_roadmap.md` records the completed vendor removal.

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

The vendor grammar backend has been removed. Public TN/ITN routes are served by
first-party `light_text_process` rules, and num2words remains a separate
dependency-backed surface.
