from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from num2words import num2words


_NUMBER_RE = re.compile(r"(?<![\w.])[-+]?\d+(?:[.,]\d+)?(?!\w)")
_ISO_DATE_RE = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")
_TIME_RE = re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_CURRENCY_RE = re.compile(r"(?<!\w)([$€£¥])\s*(-?\d+(?:[.,]\d{1,2})?)(?!\w)")
_PERCENT_RE = re.compile(r"(?<!\w)([-+]?\d+(?:[.,]\d+)?)%")
_FRACTION_RE = re.compile(r"(?<!\w)(\d+)\s*/\s*(\d+)(?!\w)")
_ORDINAL_RE = re.compile(r"(?<!\w)(\d+)(?:\.|º|ª)(?!\w)")
_MEASURE_RE = re.compile(r"(?<!\w)([-+]?\d+(?:[.,]\d+)?)\s*(kg|km|cm|mm|m|l|ml)\b", re.IGNORECASE)
_TELEPHONE_RE = re.compile(
    r"\b(?P<label>telefon|teléfono|telefono|телефон|tel)\s*[:：]?\s*(?P<number>\+?\d[\d\s-]{4,}\d)",
    re.IGNORECASE,
)

_CURRENCY_WORDS = {
    "de": {"$": ("Dollar", "Cent"), "€": ("Euro", "Cent"), "£": ("Pfund", "Pence"), "¥": ("Yen", "Sen")},
    "es": {"$": ("dólares", "centavos"), "€": ("euros", "céntimos"), "£": ("libras", "peniques"), "¥": ("yenes", "sen")},
    "ru": {"$": ("долларов", "центов"), "€": ("евро", "центов"), "£": ("фунтов", "пенсов"), "¥": ("иен", "сен")},
}

_DATE_WORDS = {
    "de": ("Jahr", "Monat", "Tag"),
    "es": ("año", "mes", "día"),
    "ru": ("год", "месяц", "день"),
}

_TIME_WORDS = {
    "de": ("Uhr", "Minuten"),
    "es": ("horas", "minutos"),
    "ru": ("часов", "минут"),
}

_PERCENT_WORDS = {"de": "Prozent", "es": "por ciento", "ru": "процентов"}
_PLUS_WORDS = {"de": "plus", "es": "más", "ru": "плюс"}
_ORDINAL_SUFFIX_WORDS = {"de": ".", "es": ".", "ru": ""}
_FRACTION_WORDS = {
    "de": "{numerator} durch {denominator}",
    "es": "{numerator} sobre {denominator}",
    "ru": "{numerator} из {denominator}",
}
_UNIT_WORDS = {
    "de": {
        "kg": "Kilogramm",
        "km": "Kilometer",
        "cm": "Zentimeter",
        "mm": "Millimeter",
        "m": "Meter",
        "l": "Liter",
        "ml": "Milliliter",
    },
    "es": {
        "kg": "kilogramos",
        "km": "kilómetros",
        "cm": "centímetros",
        "mm": "milímetros",
        "m": "metros",
        "l": "litros",
        "ml": "mililitros",
    },
    "ru": {
        "kg": "килограмм",
        "km": "километров",
        "cm": "сантиметров",
        "mm": "миллиметров",
        "m": "метров",
        "l": "литров",
        "ml": "миллилитров",
    },
}


def normalize_tn(text: str, language: str) -> str:
    normalized = _EMAIL_RE.sub(_verbalize_email, text)
    normalized = _TELEPHONE_RE.sub(lambda match: _verbalize_telephone(match, language), normalized)
    normalized = _CURRENCY_RE.sub(lambda match: _verbalize_currency(match, language), normalized)
    normalized = _ISO_DATE_RE.sub(lambda match: _verbalize_date(match, language), normalized)
    normalized = _TIME_RE.sub(lambda match: _verbalize_time(match, language), normalized)
    normalized = _FRACTION_RE.sub(lambda match: _verbalize_fraction(match, language), normalized)
    normalized = _ORDINAL_RE.sub(lambda match: _verbalize_ordinal(match, language), normalized)
    normalized = _MEASURE_RE.sub(lambda match: _verbalize_measure(match, language), normalized)
    normalized = _PERCENT_RE.sub(lambda match: f"{_format_number(match.group(1), language)} {_PERCENT_WORDS[language]}", normalized)
    return _NUMBER_RE.sub(lambda match: _format_number(match.group(0), language), normalized)


def _verbalize_email(match: re.Match[str]) -> str:
    return (
        match.group(0)
        .replace("@", " at ")
        .replace(".", " dot ")
        .replace("_", " underscore ")
        .replace("-", " dash ")
    )


def _verbalize_currency(match: re.Match[str], language: str) -> str:
    symbol = match.group(1)
    major_word, minor_word = _CURRENCY_WORDS[language][symbol]
    major, minor = _split_decimal(match.group(2))
    output = f"{_format_number(major, language)} {major_word}"
    if minor is not None and int(minor) != 0:
        output = f"{output} {_format_number(minor, language)} {minor_word}"
    return output


def _verbalize_date(match: re.Match[str], language: str) -> str:
    year_word, month_word, day_word = _DATE_WORDS[language]
    year, month, day = match.groups()
    return (
        f"{_format_number(year, language)} {year_word} "
        f"{_format_number(month, language)} {month_word} "
        f"{_format_number(day, language)} {day_word}"
    )


def _verbalize_time(match: re.Match[str], language: str) -> str:
    hour_word, minute_word = _TIME_WORDS[language]
    hour, minute = match.groups()
    return f"{_format_number(hour, language)} {hour_word} {_format_number(minute, language)} {minute_word}"


def _verbalize_fraction(match: re.Match[str], language: str) -> str:
    numerator = _format_number(match.group(1), language)
    denominator = _format_number(match.group(2), language)
    return _FRACTION_WORDS[language].format(numerator=numerator, denominator=denominator)


def _verbalize_ordinal(match: re.Match[str], language: str) -> str:
    value = int(match.group(1))
    suffix = _ORDINAL_SUFFIX_WORDS[language]
    return f"{num2words(value, lang=language, to='ordinal')}{suffix}"


def _verbalize_measure(match: re.Match[str], language: str) -> str:
    value = _format_number(match.group(1), language)
    unit = _UNIT_WORDS[language][match.group(2).lower()]
    return f"{value} {unit}"


def _verbalize_telephone(match: re.Match[str], language: str) -> str:
    number = match.group("number")
    spoken = []
    for char in number:
        if char.isdigit():
            spoken.append(_format_number(char, language))
        elif char == "+":
            spoken.append(_PLUS_WORDS[language])
    return f"{match.group('label')} {' '.join(spoken)}"


def _split_decimal(raw: str) -> tuple[str, str | None]:
    normalized = raw.replace(",", ".")
    if "." not in normalized:
        return normalized, None
    major, minor = normalized.split(".", 1)
    return major, minor.ljust(2, "0")[:2]


def _format_number(raw: str, language: str) -> str:
    value = raw.replace(",", ".")
    try:
        number = Decimal(value)
    except InvalidOperation:
        return raw
    if number == number.to_integral():
        return num2words(int(number), lang=language)
    return num2words(float(number), lang=language)
