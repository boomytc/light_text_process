from __future__ import annotations

import re


_EMAIL_SPOKEN_RE = re.compile(
    r"\b([a-z0-9](?:\s+[a-z0-9])*)\s+(?:at|arroba|at-sign)\s+"
    r"([a-z0-9](?:\s+[a-z0-9])*)\s+(?:dot|punto|punkt|точка|ponto)\s+([a-z]{2,})\b",
    re.IGNORECASE,
)

_DIGIT_WORDS = {
    "de": {"null": "0", "eins": "1", "ein": "1", "zwei": "2", "drei": "3", "vier": "4", "fünf": "5", "fuenf": "5", "sechs": "6", "sieben": "7", "acht": "8", "neun": "9"},
    "es": {"cero": "0", "uno": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9"},
    "fr": {"zéro": "0", "zero": "0", "un": "1", "une": "1", "deux": "2", "trois": "3", "quatre": "4", "cinq": "5", "six": "6", "sept": "7", "huit": "8", "neuf": "9"},
    "id": {"nol": "0", "satu": "1", "dua": "2", "tiga": "3", "empat": "4", "lima": "5", "enam": "6", "tujuh": "7", "delapan": "8", "sembilan": "9"},
    "ja": {"zero": "0", "rei": "0", "ichi": "1", "ni": "2", "san": "3", "yon": "4", "shi": "4", "go": "5", "roku": "6", "nana": "7", "shichi": "7", "hachi": "8", "kyu": "9", "ku": "9"},
    "ko": {"yeong": "0", "gong": "0", "il": "1", "i": "2", "sam": "3", "sa": "4", "o": "5", "yuk": "6", "chil": "7", "pal": "8", "gu": "9"},
    "pt": {"zero": "0", "um": "1", "uma": "1", "dois": "2", "duas": "2", "três": "3", "tres": "3", "quatro": "4", "cinco": "5", "seis": "6", "sete": "7", "oito": "8", "nove": "9"},
    "ru": {"ноль": "0", "нуль": "0", "один": "1", "одна": "1", "два": "2", "две": "2", "три": "3", "четыре": "4", "пять": "5", "шесть": "6", "семь": "7", "восемь": "8", "девять": "9", "odin": "1", "dva": "2", "tri": "3"},
    "tl": {"sero": "0", "isa": "1", "dalawa": "2", "tatlo": "3", "apat": "4", "lima": "5", "anim": "6", "pito": "7", "walo": "8", "siyam": "9"},
    "vi": {"không": "0", "khong": "0", "một": "1", "mot": "1", "hai": "2", "ba": "3", "bốn": "4", "bon": "4", "năm": "5", "nam": "5", "sáu": "6", "sau": "6", "bảy": "7", "bay": "7", "tám": "8", "tam": "8", "chín": "9", "chin": "9"},
}


def normalize_itn(text: str, language: str) -> str:
    words = _DIGIT_WORDS[language]
    normalized = _EMAIL_SPOKEN_RE.sub(_restore_email, text)
    pattern = re.compile(
        r"\b(?:" + "|".join(re.escape(word) for word in sorted(words, key=len, reverse=True)) + r")(?:\s+(?:" +
        "|".join(re.escape(word) for word in sorted(words, key=len, reverse=True)) + r"))+\b",
        re.IGNORECASE,
    )
    return pattern.sub(lambda match: _digits_for_phrase(match.group(0), words), normalized)


def _restore_email(match: re.Match[str]) -> str:
    local = "".join(match.group(1).split())
    domain = "".join(match.group(2).split())
    return f"{local}@{domain}.{match.group(3).lower()}"


def _digits_for_phrase(phrase: str, words: dict[str, str]) -> str:
    output = []
    for token in phrase.lower().split():
        digit = words.get(token)
        if digit is None:
            return phrase
        output.append(digit)
    return "".join(output)
