from __future__ import annotations

from functools import lru_cache

from light_text_process.paths import GRAMMAR_CACHE_DIR, ensure_runtime_dirs, resolve_project_path
from light_text_process.rules import en_itn, en_tn, zh_itn, zh_tn
from light_text_process.schemas import ITNOptions, TNOptions


def _cache_dir(enabled: bool) -> str | None:
    if not enabled:
        return None
    ensure_runtime_dirs()
    return str(GRAMMAR_CACHE_DIR)


@lru_cache(maxsize=24)
def _cached_tn(
    input_case: str,
    language: str,
    deterministic: bool,
    cache_dir: str | None,
    whitelist: str | None,
    post_process: bool,
):
    from fun_text_processing.text_normalization.normalize import Normalizer

    return Normalizer(
        input_case=input_case,
        lang=language,
        deterministic=deterministic,
        cache_dir=cache_dir,
        overwrite_cache=False,
        whitelist=whitelist,
        post_process=post_process,
    )


@lru_cache(maxsize=24)
def _cached_itn(
    language: str,
    cache_dir: str | None,
    enable_standalone_number: bool,
    enable_0_to_9: bool,
):
    from fun_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

    return InverseNormalizer(
        lang=language,
        cache_dir=cache_dir,
        overwrite_cache=False,
        enable_standalone_number=enable_standalone_number,
        enable_0_to_9=enable_0_to_9,
    )


def clear_tn_cache() -> None:
    _cached_tn.cache_clear()


def clear_itn_cache() -> None:
    _cached_itn.cache_clear()


class FunTextProcessingEngine:
    name = "fun_text_processing"

    def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
        options = options or TNOptions()
        whitelist_path = resolve_project_path(options.whitelist_path)
        cache_dir = _cache_dir(options.cache_enabled)
        whitelist = str(whitelist_path) if whitelist_path else None
        _cached_tn(
            options.input_case,
            language,
            options.deterministic,
            cache_dir,
            whitelist,
            options.post_process,
        )

    def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
        options = options or ITNOptions()
        cache_dir = _cache_dir(options.cache_enabled)
        _cached_itn(
            language,
            cache_dir,
            options.enable_standalone_number,
            options.enable_0_to_9,
        )

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        whitelist_path = resolve_project_path(options.whitelist_path)
        cache_dir = _cache_dir(options.cache_enabled)
        whitelist = str(whitelist_path) if whitelist_path else None
        if options.overwrite_cache:
            from fun_text_processing.text_normalization.normalize import Normalizer

            normalizer = Normalizer(
                input_case=options.input_case,
                lang=language,
                deterministic=options.deterministic,
                cache_dir=cache_dir,
                overwrite_cache=True,
                whitelist=whitelist,
                post_process=options.post_process,
            )
            clear_tn_cache()
        else:
            normalizer = _cached_tn(
                options.input_case,
                language,
                options.deterministic,
                cache_dir,
                whitelist,
                options.post_process,
            )
        if language == "en":
            prepared_texts = [en_tn.prepare_input(text) for text in texts]
        elif language == "zh":
            prepared_texts = [zh_tn.prepare_input(text) for text in texts]
        else:
            prepared_texts = texts
        return normalizer.normalize_list(
            prepared_texts,
            punct_pre_process=options.punct_pre_process,
            punct_post_process=options.punct_post_process,
            batch_size=options.batch_size,
            n_jobs=options.n_jobs,
        )

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        cache_dir = _cache_dir(options.cache_enabled)
        if language == "en":
            prepared_texts = [en_itn.prepare_input(text) for text in texts]
        elif language == "zh":
            prepared_texts = [zh_itn.prepare_input(text) for text in texts]
        else:
            prepared_texts = texts
        if options.overwrite_cache:
            from fun_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

            inverse_normalizer = InverseNormalizer(
                lang=language,
                cache_dir=cache_dir,
                overwrite_cache=True,
                enable_standalone_number=options.enable_standalone_number,
                enable_0_to_9=options.enable_0_to_9,
            )
            clear_itn_cache()
        else:
            inverse_normalizer = _cached_itn(
                language,
                cache_dir,
                options.enable_standalone_number,
                options.enable_0_to_9,
            )
        outputs = inverse_normalizer.inverse_normalize_list(prepared_texts)
        if language == "en":
            return en_itn.finalize_outputs(outputs)
        if language == "zh":
            return zh_itn.finalize_outputs(outputs)
        return outputs
