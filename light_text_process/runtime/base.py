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


class CompositeTextProcessingEngine:
    name = "composite"

    def __init__(
        self,
        *,
        native_engine: TextProcessingEngine,
        fallback_engine: TextProcessingEngine,
        native_routes: set[tuple[str, str]] | None = None,
    ) -> None:
        self.native_engine = native_engine
        self.fallback_engine = fallback_engine
        self.native_routes = native_routes or set()
        self.last_engine_name: str | None = None

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        engine = self._engine_for("tn", language)
        self.last_engine_name = engine.name
        return engine.normalize(texts, language, options)

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        engine = self._engine_for("itn", language)
        self.last_engine_name = engine.name
        return engine.inverse_normalize(texts, language, options)

    def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
        engine = self._engine_for("tn", language)
        self.last_engine_name = engine.name
        engine.warmup_tn(language, options)

    def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
        engine = self._engine_for("itn", language)
        self.last_engine_name = engine.name
        engine.warmup_itn(language, options)

    def _engine_for(self, operation: str, language: str) -> TextProcessingEngine:
        if (operation, language) in self.native_routes:
            return self.native_engine
        return self.fallback_engine
