from __future__ import annotations

from typing import Protocol

from light_text_process.schemas import ITNOptions, TNOptions


class TextProcessingEngine(Protocol):
    name: str

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        raise NotImplementedError

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        raise NotImplementedError

    def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
        raise NotImplementedError

    def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
        raise NotImplementedError


class NativeRouteUnsupportedError(ValueError):
    pass
