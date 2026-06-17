from __future__ import annotations

import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
THIRD_PARTY_DIR = PROJECT_DIR / "third_party"
RUNTIME_DIR = PROJECT_DIR / "runtime"
GRAMMAR_CACHE_DIR = RUNTIME_DIR / "cache" / "fun_text_processing"


def ensure_runtime_paths() -> None:
    for runtime_path in (PROJECT_DIR, THIRD_PARTY_DIR):
        runtime_path_text = str(runtime_path)
        if runtime_path_text not in sys.path:
            sys.path.insert(0, runtime_path_text)


def ensure_runtime_dirs() -> None:
    GRAMMAR_CACHE_DIR.mkdir(parents=True, exist_ok=True)


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
