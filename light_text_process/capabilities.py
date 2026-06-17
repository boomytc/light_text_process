from __future__ import annotations

from functools import lru_cache
from typing import Any


TN_LANGUAGES = {
    "de": "德语",
    "en": "英语",
    "es": "西班牙语",
    "ru": "俄语",
    "zh": "中文",
}

ITN_LANGUAGES = {
    "de": "德语",
    "en": "英语",
    "es": "西班牙语",
    "fr": "法语",
    "id": "印尼语",
    "ja": "日语",
    "ko": "韩语",
    "pt": "葡萄牙语",
    "ru": "俄语",
    "tl": "他加禄语",
    "vi": "越南语",
    "zh": "中文",
}

NUM2WORDS_MODES = {
    "cardinal": "基数词",
    "ordinal": "序数词",
    "ordinal_num": "序数数字",
    "year": "年份读法",
    "currency": "货币读法",
}

ITN_LANGUAGE_OPTIONS: dict[str, list[str]] = {
    "ja": ["enable_standalone_number", "enable_0_to_9"],
}

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
    "input_case": {
        "label": "输入大小写",
        "help": "英文等大小写敏感语言可选择保留原大小写或按小写处理。",
    },
    "deterministic": {
        "label": "稳定输出",
        "help": "同一输入尽量给出同一结果，适合批量处理和复现。",
    },
    "whitelist_path": {
        "label": "自定义白名单文件",
        "help": "可选的产品内相对路径，用于指定固定替换词表。",
    },
    "post_process": {
        "label": "标准后处理",
        "help": "对规则输出做常规清理。",
    },
    "punct_pre_process": {
        "label": "输入标点预处理",
        "help": "在规则处理前先整理输入标点。",
    },
    "punct_post_process": {
        "label": "输出标点恢复",
        "help": "在规则处理后整理输出标点。",
    },
    "batch_size": {
        "label": "每批条数",
        "help": "单次送入规则引擎的条数。",
    },
    "n_jobs": {
        "label": "并发任务数",
        "help": "本地并发处理数量，过高可能增加资源占用。",
    },
    "enable_standalone_number": {
        "label": "处理独立数字",
        "help": "日语 ITN 可用，用于处理单独出现的数字读法。",
    },
    "enable_0_to_9": {
        "label": "处理 0 到 9",
        "help": "日语 ITN 可用，用于处理单个数字读法。",
    },
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
                "options": [
                    "input_case",
                    "deterministic",
                    "whitelist_path",
                    "post_process",
                    "punct_pre_process",
                    "punct_post_process",
                    "batch_size",
                    "n_jobs",
                ],
                "option_details": {
                    key: OPTION_DETAILS[key]
                    for key in [
                        "input_case",
                        "deterministic",
                        "whitelist_path",
                        "post_process",
                        "punct_pre_process",
                        "punct_post_process",
                        "batch_size",
                        "n_jobs",
                    ]
                },
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
