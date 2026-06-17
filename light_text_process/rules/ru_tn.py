from __future__ import annotations

from light_text_process.rules.multilingual_tn import normalize_tn


def prepare_input(text: str) -> str:
    return normalize_tn(text, "ru")
