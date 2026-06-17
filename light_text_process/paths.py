from __future__ import annotations

import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
RUNTIME_DIR = PROJECT_DIR / "runtime"


def ensure_runtime_paths() -> None:
    runtime_path_text = str(PROJECT_DIR)
    if runtime_path_text not in sys.path:
        sys.path.insert(0, runtime_path_text)


def ensure_runtime_dirs() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def resolve_project_path(value: str | None) -> Path | None:
    if value is None or not value.strip():
        return None
    path = Path(value).expanduser()
    if path.is_absolute():
        raise ValueError("absolute paths are not allowed")
    resolved = (PROJECT_DIR / path).resolve()
    if not resolved.is_relative_to(PROJECT_DIR):
        raise ValueError("path must stay inside the project directory")
    return resolved


ensure_runtime_paths()
