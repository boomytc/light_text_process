from __future__ import annotations

from functools import lru_cache
from typing import Any


TN_LANGUAGES = {
    "en": "英语",
    "zh": "中文",
}

ITN_LANGUAGES = {
    "en": "英语",
    "zh": "中文",
}

NUM2WORDS_MODES = {
    "cardinal": "基数词",
    "ordinal": "序数词",
    "ordinal_num": "序数数字",
    "year": "年份读法",
    "currency": "货币读法",
}

ITN_LANGUAGE_OPTIONS: dict[str, list[str]] = {}

OPERATION_DETAILS = {
    "tn": {
        "label": "TN",
        "display_label": "文本转读法",
        "short_label": "读法",
        "description": "把书面文本转换成规范读法表达。",
        "help_text": "适合处理日期、金额、编号和单位等需要读出来的文本。",
    },
    "itn": {
        "label": "ITN",
        "display_label": "读法转文本",
        "short_label": "还原",
        "description": "把口语读法还原成更适合阅读、检索或入库的书面文本。",
        "help_text": "适合把数字、日期和金额等读法表达还原为常见写法。",
    },
    "num2words": {
        "label": "num2words",
        "display_label": "数字转外语词",
        "short_label": "数字",
        "description": "把数字转换为指定语言的文字读法。",
        "help_text": "适合快速生成外语数字、年份、序数或货币表达。",
    },
}

OPTION_DETAILS = {
    "mode": {
        "label": "转换模式",
        "help": "选择普通数字、序数、年份或货币读法。",
    },
    "currency": {
        "label": "货币",
        "help": "仅在货币读法模式下使用。",
    },
}


def num2words_languages() -> dict[str, str]:
    return {language: language for language in sorted(_num2words_converters().keys())}


def num2words_modes_for_language(language: str) -> dict[str, str]:
    converter = _num2words_converters().get(language)
    if converter is None:
        return {}

    modes = {}
    for mode, label in NUM2WORDS_MODES.items():
        if mode == "currency":
            if num2words_currencies(language):
                modes[mode] = label
            continue
        if hasattr(converter, f"to_{mode}"):
            modes[mode] = label
    return modes


def num2words_currencies(language: str) -> list[str]:
    converter = _num2words_converters().get(language)
    if converter is None:
        return []
    return sorted(getattr(converter, "CURRENCY_FORMS", {}).keys())


def num2words_default_currency(language: str) -> str | None:
    currencies = num2words_currencies(language)
    if not currencies:
        return None
    if "EUR" in currencies:
        return "EUR"
    return currencies[0]


def num2words_modes_by_language() -> dict[str, dict[str, str]]:
    return {
        language: num2words_modes_for_language(language)
        for language in sorted(_num2words_converters().keys())
    }


def num2words_currencies_by_language() -> dict[str, list[str]]:
    return {
        language: currencies
        for language in sorted(_num2words_converters().keys())
        if (currencies := num2words_currencies(language))
    }


def num2words_default_currency_by_language() -> dict[str, str]:
    return {
        language: currency
        for language in sorted(_num2words_converters().keys())
        if (currency := num2words_default_currency(language))
    }


@lru_cache(maxsize=1)
def _num2words_converters() -> dict[str, object]:
    from num2words import CONVERTER_CLASSES

    return dict(CONVERTER_CLASSES)


def build_capabilities() -> dict[str, Any]:
    return {
        "operations": {
            "tn": {
                **OPERATION_DETAILS["tn"],
                "languages": TN_LANGUAGES,
                "options": [],
                "option_details": {},
            },
            "itn": {
                **OPERATION_DETAILS["itn"],
                "languages": ITN_LANGUAGES,
                "language_options": ITN_LANGUAGE_OPTIONS,
                "options": [],
                "option_details": {},
            },
            "num2words": {
                **OPERATION_DETAILS["num2words"],
                "languages": num2words_languages(),
                "modes": NUM2WORDS_MODES,
                "modes_by_language": num2words_modes_by_language(),
                "currencies_by_language": num2words_currencies_by_language(),
                "default_currency_by_language": num2words_default_currency_by_language(),
                "options": ["mode", "currency"],
                "option_details": {
                    key: OPTION_DETAILS[key]
                    for key in [
                        "mode",
                        "currency",
                    ]
                },
            },
        }
    }
