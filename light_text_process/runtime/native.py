from __future__ import annotations

from light_text_process.runtime.base import NativeRouteUnsupportedError
from light_text_process.rules import en_itn, en_tn, zh_itn, zh_tn
from light_text_process.schemas import ITNOptions, TNOptions


class NativeTextProcessingEngine:
    name = "light_text_process_native"

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        if language == "en":
            return [_normalize_en_tn(text) for text in texts]
        if language == "zh":
            return [_normalize_zh_tn(text) for text in texts]
        raise NativeRouteUnsupportedError(f"native TN route is not enabled for language: {language}")

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        if language == "en":
            return [_normalize_en_itn(text) for text in texts]
        if language == "zh":
            return [_normalize_zh_itn(text) for text in texts]
        raise NativeRouteUnsupportedError(f"native ITN route is not enabled for language: {language}")

    def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
        return None

    def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
        return None


def _normalize_zh_itn(text: str) -> str:
    return zh_itn.finalize_outputs([zh_itn.prepare_input(text)])[0]


def _normalize_en_itn(text: str) -> str:
    return en_itn.finalize_outputs([en_itn.prepare_input(text)])[0]


def _normalize_zh_tn(text: str) -> str:
    return zh_tn.prepare_input(text)


def _normalize_en_tn(text: str) -> str:
    return en_tn.prepare_input(text)
