from __future__ import annotations

from light_text_process.runtime.base import NativeRouteUnsupportedError
from light_text_process.schemas import ITNOptions, TNOptions


class NativeTextProcessingEngine:
    name = "light_text_process_native"

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        raise NativeRouteUnsupportedError(f"native TN route is not enabled for language: {language}")

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        raise NativeRouteUnsupportedError(f"native ITN route is not enabled for language: {language}")

    def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
        return None

    def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
        return None
