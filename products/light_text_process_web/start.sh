#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

HOST="${LIGHT_TEXT_PROCESS_WEB_HOST:-127.0.0.1}"
PORT="${LIGHT_TEXT_PROCESS_WEB_PORT:-8011}"

exec .venv/bin/python -m uvicorn app:app --host "$HOST" --port "$PORT"
