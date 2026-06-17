from __future__ import annotations

from light_text_process.rules.multilingual_itn import normalize_itn


def finalize_outputs(texts: list[str]) -> list[str]:
    return [normalize_itn(text, "id") for text in texts]
