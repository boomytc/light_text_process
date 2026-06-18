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

## API Surface

- `GET /health`
- `GET /api/v1/capabilities`
- `POST /api/v1/tn`
- `POST /api/v1/itn`
- `POST /api/v1/num2words`
- `POST /api/v1/batch`
- `GET /partials/capabilities`

## Validation

```bash
.venv/bin/python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
.venv/bin/python -m compileall -q app.py api tests
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -c "from app import create_app; app = create_app(); print(app.title)"
```

Runtime smoke checks:

```bash
LIGHT_TEXT_PROCESS_WEB_PORT=8011 ./start.sh
curl -s http://127.0.0.1:8011/api/v1/capabilities
curl -s -X POST http://127.0.0.1:8011/api/v1/tn -H 'Content-Type: application/json' -d '{"text":"今天是 2026 年 6 月 15 日。","language":"zh"}'
curl -s -X POST http://127.0.0.1:8011/api/v1/itn -H 'Content-Type: application/json' -d '{"text":"二零二六年六月十五日","language":"zh"}'
curl -s -X POST http://127.0.0.1:8011/api/v1/num2words -H 'Content-Type: application/json' -d '{"number":"123","language":"en"}'
curl -s -X POST http://127.0.0.1:8011/api/v1/batch -H 'Content-Type: application/json' -d '{"operation":"num2words","items":["123","bad-number"],"language":"en"}'
```
