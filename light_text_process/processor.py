from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter

from light_text_process.capabilities import (
    ITN_LANGUAGES,
    TN_LANGUAGES,
    num2words_currencies,
    num2words_default_currency,
    num2words_languages,
    num2words_modes_for_language,
)
from light_text_process.paths import GRAMMAR_CACHE_DIR
from light_text_process.runtime.base import CompositeTextProcessingEngine, TextProcessingEngine
from light_text_process.runtime.fun_text_processing import FunTextProcessingEngine
from light_text_process.runtime.native import NativeTextProcessingEngine
from light_text_process.runtime.num2words_engine import Num2WordsEngine
from light_text_process.schemas import (
    BatchItemResponse,
    BatchResponse,
    ITNOptions,
    Num2WordsOptions,
    ProcessResponse,
    TNOptions,
)


@dataclass(frozen=True)
class GrammarWarmupTask:
    operation: str
    language: str
    expected_cache_files: tuple[str, ...]
    tn_options: TNOptions | None = None
    itn_options: ITNOptions | None = None


DEFAULT_GRAMMAR_WARMUP_PROFILES = ("zh-default",)
DEFAULT_NATIVE_ROUTES = {
    ("tn", "de"),
    ("tn", "en"),
    ("tn", "es"),
    ("tn", "ru"),
    ("tn", "zh"),
    ("itn", "de"),
    ("itn", "en"),
    ("itn", "es"),
    ("itn", "fr"),
    ("itn", "id"),
    ("itn", "ja"),
    ("itn", "ko"),
    ("itn", "pt"),
    ("itn", "ru"),
    ("itn", "tl"),
    ("itn", "vi"),
    ("itn", "zh"),
}
GRAMMAR_WARMUP_PROFILES = {
    "zh-default": (
        GrammarWarmupTask(
            operation="tn",
            language="zh",
            tn_options=TNOptions(),
            expected_cache_files=(
                "zh_tn_True_deterministic_cased__tokenize.far",
                "zh_tn_True_deterministic_verbalizer.far",
            ),
        ),
        GrammarWarmupTask(
            operation="itn",
            language="zh",
            itn_options=ITNOptions(),
            expected_cache_files=("_zh_itn.far",),
        ),
    )
}


class TextProcessor:
    def __init__(self, text_engine: TextProcessingEngine | None = None) -> None:
        self.text_engine = text_engine or CompositeTextProcessingEngine(
            native_engine=NativeTextProcessingEngine(),
            fallback_engine=FunTextProcessingEngine(),
            native_routes=set(DEFAULT_NATIVE_ROUTES),
        )
        self.num2words_engine = Num2WordsEngine()

    def normalize_text(self, text: str, language: str, options: TNOptions | None = None) -> ProcessResponse:
        options = options or TNOptions()
        _ensure_language(language, TN_LANGUAGES, "TN")
        started = perf_counter()
        output = self.text_engine.normalize([text], language, options)[0]
        return ProcessResponse(
            operation="tn",
            language=language,
            input=text,
            output=output,
            metadata={"engine": _engine_name(self.text_engine), "elapsed_seconds": round(perf_counter() - started, 4)},
        )

    def inverse_normalize_text(self, text: str, language: str, options: ITNOptions | None = None) -> ProcessResponse:
        options = options or ITNOptions()
        _ensure_language(language, ITN_LANGUAGES, "ITN")
        started = perf_counter()
        output = self.text_engine.inverse_normalize([text], language, options)[0]
        return ProcessResponse(
            operation="itn",
            language=language,
            input=text,
            output=output,
            metadata={"engine": _engine_name(self.text_engine), "elapsed_seconds": round(perf_counter() - started, 4)},
        )

    def number_to_words(self, number: str, language: str, options: Num2WordsOptions | None = None) -> ProcessResponse:
        options = options or Num2WordsOptions()
        _ensure_language(language, num2words_languages(), "num2words")
        _ensure_num2words_options(language, options)
        started = perf_counter()
        output = self.num2words_engine.convert(number, language, options)
        return ProcessResponse(
            operation="num2words",
            language=language,
            input=number,
            output=output,
            metadata={
                "engine": "num2words",
                "mode": options.mode,
                "currency": _metadata_currency(language, options),
                "elapsed_seconds": round(perf_counter() - started, 4),
            },
        )

    def batch(
        self,
        operation: str,
        items: list[str],
        language: str,
        tn_options: TNOptions,
        itn_options: ITNOptions,
        num2words_options: Num2WordsOptions,
    ) -> BatchResponse:
        started = perf_counter()
        if operation == "tn":
            _ensure_language(language, TN_LANGUAGES, "TN")
            rows = _batch_rows(
                items,
                lambda batch_items: self.text_engine.normalize(batch_items, language, tn_options),
            )
        elif operation == "itn":
            _ensure_language(language, ITN_LANGUAGES, "ITN")
            rows = _batch_rows(
                items,
                lambda batch_items: self.text_engine.inverse_normalize(batch_items, language, itn_options),
            )
        elif operation == "num2words":
            _ensure_language(language, num2words_languages(), "num2words")
            _ensure_num2words_options(language, num2words_options)
            rows = []
            for index, item in enumerate(items):
                try:
                    output = self.num2words_engine.convert(item, language, num2words_options)
                    rows.append(BatchItemResponse(index=index, input=item, output=output))
                except Exception as exc:
                    rows.append(BatchItemResponse(index=index, input=item, error=str(exc)))
        else:
            raise ValueError(f"unsupported operation: {operation}")

        error_count = sum(1 for row in rows if row.error)
        return BatchResponse(
            operation=operation,
            language=language,
            items=rows,
            success_count=len(rows) - error_count,
            error_count=error_count,
            metadata={"elapsed_seconds": round(perf_counter() - started, 4)},
        )

    def warmup(
        self,
        tn_languages: list[str] | None = None,
        itn_languages: list[str] | None = None,
    ) -> dict[str, list[str]]:
        warmed = {"tn": [], "itn": []}
        for language in tn_languages or []:
            _ensure_language(language, TN_LANGUAGES, "TN")
            self.text_engine.warmup_tn(language, TNOptions())
            warmed["tn"].append(language)
        for language in itn_languages or []:
            _ensure_language(language, ITN_LANGUAGES, "ITN")
            self.text_engine.warmup_itn(language, ITNOptions())
            warmed["itn"].append(language)
        return warmed

    def warmup_profiles(self, profile_names: list[str] | tuple[str, ...]) -> dict[str, list[str]]:
        warmed = {"profiles": [], "tn": [], "itn": []}
        for profile_name in profile_names:
            tasks = GRAMMAR_WARMUP_PROFILES.get(profile_name)
            if tasks is None:
                supported = ", ".join(sorted(GRAMMAR_WARMUP_PROFILES))
                raise ValueError(f"unsupported warmup profile: {profile_name} (supported: {supported})")
            for task in tasks:
                self._warmup_task(task, warmed)
            warmed["profiles"].append(profile_name)
        return warmed

    def _warmup_task(self, task: GrammarWarmupTask, warmed: dict[str, list[str]]) -> None:
        if task.operation == "tn":
            _ensure_language(task.language, TN_LANGUAGES, "TN")
            self.text_engine.warmup_tn(task.language, task.tn_options or TNOptions())
            warmed["tn"].append(task.language)
        elif task.operation == "itn":
            _ensure_language(task.language, ITN_LANGUAGES, "ITN")
            self.text_engine.warmup_itn(task.language, task.itn_options or ITNOptions())
            warmed["itn"].append(task.language)
        else:
            raise ValueError(f"unsupported warmup operation: {task.operation}")

        if _engine_name(self.text_engine) != NativeTextProcessingEngine.name:
            _ensure_expected_cache_files(task)


def _ensure_language(language: str, supported: dict[str, str], label: str) -> None:
    if language not in supported:
        raise ValueError(f"unsupported {label} language: {language}")


def _ensure_expected_cache_files(task: GrammarWarmupTask) -> None:
    missing = [
        file_name
        for file_name in task.expected_cache_files
        if not (GRAMMAR_CACHE_DIR / file_name).is_file()
    ]
    if missing:
        missing_text = ", ".join(missing)
        raise RuntimeError(
            f"grammar cache warmup did not create expected files for "
            f"{task.operation}:{task.language}: {missing_text}"
        )


def _engine_name(engine: TextProcessingEngine) -> str:
    last_engine_name = getattr(engine, "last_engine_name", None)
    if isinstance(last_engine_name, str) and last_engine_name:
        return last_engine_name
    return engine.name


def _ensure_num2words_options(language: str, options: Num2WordsOptions) -> None:
    modes = num2words_modes_for_language(language)
    if options.mode not in modes:
        supported = ", ".join(modes) or "none"
        raise ValueError(
            f"unsupported num2words mode for {language}: {options.mode} (supported: {supported})"
        )
    if options.mode != "currency" or not options.currency:
        return

    currency = options.currency.upper()
    currencies = num2words_currencies(language)
    if currencies and currency not in currencies:
        supported = ", ".join(currencies)
        raise ValueError(
            f"unsupported num2words currency for {language}: {currency} (supported: {supported})"
        )


def _metadata_currency(language: str, options: Num2WordsOptions) -> str | None:
    if options.mode != "currency":
        return None
    if options.currency:
        return options.currency.upper()
    return num2words_default_currency(language)


def _batch_rows(items: list[str], processor: Callable[[list[str]], list[str]]) -> list[BatchItemResponse]:
    try:
        outputs = processor(items)
        if len(outputs) != len(items):
            raise ValueError(f"batch output count mismatch: expected {len(items)}, got {len(outputs)}")
        return [BatchItemResponse(index=index, input=item, output=outputs[index]) for index, item in enumerate(items)]
    except Exception as batch_exc:
        rows: list[BatchItemResponse] = []
        for index, item in enumerate(items):
            try:
                output = processor([item])[0]
                rows.append(BatchItemResponse(index=index, input=item, output=output))
            except Exception as exc:
                rows.append(BatchItemResponse(index=index, input=item, error=str(exc)))
        row_errors = [row.error or "" for row in rows if row.error]
        if all(row.error for row in rows) and _is_system_batch_failure(batch_exc, row_errors):
            raise batch_exc
        return rows


_SYSTEM_ERROR_TYPES = (ImportError, ModuleNotFoundError, OSError)
_SYSTEM_ERROR_MARKERS = (
    "file not found",
    "import",
    "module",
    "no module named",
    "no such file",
    "path",
    "permission",
    "runtime",
    "whitelist",
)


def _is_system_batch_failure(batch_exc: Exception, row_errors: list[str]) -> bool:
    if isinstance(batch_exc, _SYSTEM_ERROR_TYPES):
        return True

    if _looks_like_system_error(str(batch_exc)):
        return True

    return any(_looks_like_system_error(error) for error in row_errors)


def _looks_like_system_error(message: str) -> bool:
    normalized = message.lower()
    return any(marker in normalized for marker in _SYSTEM_ERROR_MARKERS)
