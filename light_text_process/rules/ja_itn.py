from __future__ import annotations

from light_text_process.rules.multilingual_itn import normalize_itn


def finalize_outputs(
    texts: list[str],
    *,
    enable_standalone_number: bool = True,
    enable_0_to_9: bool = True,
) -> list[str]:
    return [
        normalize_itn(
            text,
            "ja",
            enable_standalone_number=enable_standalone_number,
            enable_0_to_9=enable_0_to_9,
        )
        for text in texts
    ]
