from __future__ import annotations

from pathlib import Path


PRODUCT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PRODUCT_DIR / "static"
TEMPLATES_DIR = PRODUCT_DIR / "templates"
RUNTIME_DIR = PRODUCT_DIR / "runtime"


def product_path(*parts: str) -> Path:
    return PRODUCT_DIR.joinpath(*parts)
