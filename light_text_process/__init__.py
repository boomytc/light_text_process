from __future__ import annotations

from light_text_process.schemas import (
    BatchItemResponse,
    BatchRequest,
    BatchResponse,
    ITNOptions,
    Num2WordsOptions,
    ProcessResponse,
    TNOptions,
)

__all__ = [
    "BatchItemResponse",
    "BatchRequest",
    "BatchResponse",
    "ITNOptions",
    "Num2WordsOptions",
    "ProcessResponse",
    "TNOptions",
    "TextProcessor",
]


def __getattr__(name: str) -> object:
    if name == "TextProcessor":
        from light_text_process.processor import TextProcessor

        return TextProcessor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
