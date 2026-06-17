# Light Text Process

Standalone Python engine for text normalization (TN), inverse text normalization (ITN), and multilingual number-to-words conversion.

This repository is intended to become the long-term `light_text_process` engine. The current implementation provides an equivalent baseline to the `light_text_process_web` product engine: product-owned rules live in `light_text_process/rules`, the runtime adapter lives in `light_text_process/runtime`, and golden regression cases live in `data/rule_cases`.

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
- `light_text_process/runtime/` contains runtime adapters.
- `third_party/fun_text_processing/` is the initial grammar backend used to keep the baseline equivalent while this project grows toward a native replacement.
- `data/rule_cases/` is the golden regression suite for zh/en TN/ITN behavior.
- `scripts/validate_rules.py` runs the golden suite.
- `scripts/cache_maintenance.py` inspects and rebuilds grammar caches under `runtime/cache`.

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q light_text_process scripts tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/validate_rules.py
.venv/bin/python -c "from light_text_process import TextProcessor; print(TextProcessor().number_to_words('123', 'en').output)"
```

## Direction

The immediate goal is an equivalent standalone engine. The long-term goal is to progressively replace the vendored `fun_text_processing` backend with first-party Light Text Process implementations while preserving the public API and golden behavior.
