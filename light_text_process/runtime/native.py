from __future__ import annotations

from light_text_process.runtime.base import NativeRouteUnsupportedError
from light_text_process.paths import resolve_project_path
from light_text_process.rules import (
    de_itn,
    de_tn,
    en_itn,
    en_tn,
    es_itn,
    es_tn,
    fr_itn,
    id_itn,
    ja_itn,
    ko_itn,
    pt_itn,
    ru_itn,
    ru_tn,
    tl_itn,
    vi_itn,
    zh_itn,
    zh_tn,
)
from light_text_process.schemas import ITNOptions, TNOptions


class NativeTextProcessingEngine:
    name = "light_text_process_native"

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        if language == "de":
            return _apply_tn_whitelist([de_tn.prepare_input(text) for text in texts], options)
        if language == "en":
            return _apply_tn_whitelist([_normalize_en_tn(text) for text in texts], options)
        if language == "es":
            return _apply_tn_whitelist([es_tn.prepare_input(text) for text in texts], options)
        if language == "ru":
            return _apply_tn_whitelist([ru_tn.prepare_input(text) for text in texts], options)
        if language == "zh":
            return _apply_tn_whitelist([_normalize_zh_tn(text) for text in texts], options)
        raise NativeRouteUnsupportedError(f"native TN route is not enabled for language: {language}")

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        if language == "de":
            return de_itn.finalize_outputs(texts)
        if language == "en":
            return [_normalize_en_itn(text) for text in texts]
        if language == "es":
            return es_itn.finalize_outputs(texts)
        if language == "fr":
            return fr_itn.finalize_outputs(texts)
        if language == "id":
            return id_itn.finalize_outputs(texts)
        if language == "ja":
            return ja_itn.finalize_outputs(
                texts,
                enable_standalone_number=options.enable_standalone_number,
                enable_0_to_9=options.enable_0_to_9,
            )
        if language == "ko":
            return ko_itn.finalize_outputs(texts)
        if language == "pt":
            return pt_itn.finalize_outputs(texts)
        if language == "ru":
            return ru_itn.finalize_outputs(texts)
        if language == "tl":
            return tl_itn.finalize_outputs(texts)
        if language == "vi":
            return vi_itn.finalize_outputs(texts)
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


def _apply_tn_whitelist(texts: list[str], options: TNOptions) -> list[str]:
    replacements = _load_tn_whitelist(options.whitelist_path)
    if not replacements:
        return texts
    outputs = []
    for text in texts:
        output = text
        for source, target in replacements:
            output = output.replace(source, target)
        outputs.append(output)
    return outputs


def _load_tn_whitelist(raw_path: str | None) -> list[tuple[str, str]]:
    path = resolve_project_path(raw_path)
    if path is None:
        return []
    if not path.is_file():
        raise ValueError(f"whitelist file does not exist: {raw_path}")
    replacements = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            raise ValueError(f"whitelist line {line_number} must use tab-separated source and target")
        source, target = line.split("\t", 1)
        if not source or not target:
            raise ValueError(f"whitelist line {line_number} must include source and target")
        replacements.append((source, target))
    return replacements
