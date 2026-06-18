# Light Text Process Web

FastAPI Web product for the repository-level `light_text_process` engine.

## Setup

Run from this directory:

```bash
uv venv --python 3.12
uv pip install -e ../..
uv pip install -e .
```

The first editable install provides the root engine package. The second
editable install provides this Web product. No absolute local dependency is
committed in `pyproject.toml`.

## Run

```bash
./start.sh
```

On Windows:

```bat
start.bat
```

Default URL: `http://127.0.0.1:8011`.

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q app.py api tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -c "from app import create_app; app = create_app(); print(app.title)"
```
