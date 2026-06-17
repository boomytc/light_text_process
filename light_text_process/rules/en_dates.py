from __future__ import annotations

import re
from collections.abc import Callable


_NUMBER_WORD = (
    r"zero|oh|o|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million"
)
_INTEGER_PHRASE = rf"(?:\d+|(?:{_NUMBER_WORD})(?:[\s-]+(?:{_NUMBER_WORD}))*)"
_MONTH_DAY_PHRASE = (
    r"\d{1,2}|(?:zero|oh|o)\s+(?:one|two|three|four|five|six|seven|eight|nine)|"
    r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty(?:[\s-]+(?:one|two|three|four|five|six|seven|eight|nine))?|"
    r"thirty(?:[\s-]+one)?"
)
_MONTH_NAME = (
    r"jan(?:uary)?\.?|feb(?:ruary)?\.?|mar(?:ch)?\.?|apr(?:il)?\.?|may|jun(?:e)?\.?|jul(?:y)?\.?|"
    r"aug(?:ust)?\.?|sep(?:t|tember)?\.?|oct(?:ober)?\.?|nov(?:ember)?\.?|dec(?:ember)?\.?"
)
_DIGIT_MONTH_NAME_DATE_RE = re.compile(
    rf"\b({_MONTH_NAME})\s+(\d{{1,2}})(?:st|nd|rd|th)?(?:,)?\s+(\d{{4}})\b",
    re.IGNORECASE,
)
_SPOKEN_MONTH_NAME_DATE_RE = re.compile(
    rf"\b({_MONTH_NAME})\s+(?:the\s+)?({_MONTH_DAY_PHRASE})(?:,)?\s+({_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)
_DOTTED_NUMERIC_DATE_RE = re.compile(
    r"\b((?:date|deadline|due(?:\s+date)?|on)\s+)(\d{4})\.(\d{1,2})\.(\d{1,2})\b",
    re.IGNORECASE,
)
_SPOKEN_DOTTED_DATE_RE = re.compile(
    rf"\b((?:date|deadline|due(?:\s+date)?|on)\s+)"
    rf"({_INTEGER_PHRASE})\s+(?:dot|point)\s+({_MONTH_DAY_PHRASE})\s+(?:dot|point)\s+({_MONTH_DAY_PHRASE})\b",
    re.IGNORECASE,
)
_NUMERIC_ORDINAL_RE = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)\b", re.IGNORECASE)
_NUMERIC_ORDINAL_RANGE_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)\s*[-~～–—]\s*(\d{1,2})(?:st|nd|rd|th)\b",
    re.IGNORECASE,
)
_ORDINAL_VALUE_WORD = (
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|"
    r"twentieth|thirtieth"
)
_ORDINAL_PHRASE = (
    rf"(?:{_ORDINAL_VALUE_WORD}|(?:twenty|thirty)[\s-]+"
    r"(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth))"
)
_SPOKEN_ORDINAL_CONTEXT_RE = re.compile(
    rf"\b({_ORDINAL_PHRASE})\s+"
    r"(century|floor|grade|place|rank|chapter|page|section|edition|anniversary)\b",
    re.IGNORECASE,
)
_SPOKEN_ORDINAL_RANGE_CONTEXT_RE = re.compile(
    rf"\b((?:rank|ranks|floor|floors|grade|grades|place|places|chapter|chapters|page|pages|"
    rf"section|sections|edition|editions|anniversary|anniversaries)\s+)"
    rf"({_ORDINAL_PHRASE})\s+to\s+({_ORDINAL_PHRASE})\b",
    re.IGNORECASE,
)
_SPOKEN_NUMERIC_DATE_RE = re.compile(
    rf"\b((?:date|deadline|due(?:\s+date)?|on)\s+(?:is\s+)?)"
    rf"({_MONTH_DAY_PHRASE})\s+({_MONTH_DAY_PHRASE})\s+({_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)
_ISO_DATE_RANGE_RE = re.compile(
    r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\s*[-~–—]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b"
)
_MONTH_NAMES = {
    "jan": "January",
    "january": "January",
    "feb": "February",
    "february": "February",
    "mar": "March",
    "march": "March",
    "apr": "April",
    "april": "April",
    "may": "May",
    "jun": "June",
    "june": "June",
    "jul": "July",
    "july": "July",
    "aug": "August",
    "august": "August",
    "sep": "September",
    "sept": "September",
    "september": "September",
    "oct": "October",
    "october": "October",
    "nov": "November",
    "november": "November",
    "dec": "December",
    "december": "December",
}
_MONTH_NUMBERS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}
_MONTH_NUMBERS_REVERSE = {number: name for name, number in _MONTH_NUMBERS.items()}


def _month_name(raw: str) -> str:
    return _MONTH_NAMES[raw.lower().rstrip(".")]


def _ordinal_suffix(value: int) -> str:
    if 10 <= value % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")


def verbalize_digit_month_name_dates(
    text: str,
    *,
    format_ordinal: Callable[[int], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        day = int(match.group(2))
        if not 1 <= day <= 31:
            return match.group(0)
        ordinal = format_ordinal(day)
        if ordinal is None:
            return match.group(0)
        return f"{_month_name(match.group(1))} {ordinal} {match.group(3)}"

    return _DIGIT_MONTH_NAME_DATE_RE.sub(replace, text)


def normalize_spoken_month_name_dates(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
    parse_year: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        month = _MONTH_NAMES[match.group(1).lower().rstrip(".")]
        day = parse_integer(match.group(2))
        year = parse_year(match.group(3))
        if day is None or year is None or not 1 <= day <= 31:
            return match.group(0)
        return f"{year:04d}-{_MONTH_NUMBERS[month]:02d}-{day:02d}"

    return _SPOKEN_MONTH_NAME_DATE_RE.sub(replace, text)


def verbalize_dotted_numeric_dates(
    text: str,
    *,
    format_ordinal: Callable[[int], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        month = int(match.group(3))
        day = int(match.group(4))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        ordinal = format_ordinal(day)
        if ordinal is None:
            return match.group(0)
        return f"{match.group(1)}{_MONTH_NUMBERS_REVERSE[month]} {ordinal} {match.group(2)}"

    return _DOTTED_NUMERIC_DATE_RE.sub(replace, text)


def normalize_spoken_dotted_dates(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
    parse_year: Callable[[str], int | None],
) -> str:
    def parse_month_day(raw: str) -> int | None:
        value = parse_integer(raw)
        if value is not None:
            return value
        normalized = raw.lower().strip()
        for prefix in ("oh ", "o "):
            if normalized.startswith(prefix):
                return parse_integer(normalized[len(prefix) :])
        return None

    def replace(match: re.Match[str]) -> str:
        year = parse_year(match.group(2))
        month = parse_month_day(match.group(3))
        day = parse_month_day(match.group(4))
        if year is None or month is None or day is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}{year:04d}.{month:02d}.{day:02d}"

    return _SPOKEN_DOTTED_DATE_RE.sub(replace, text)


def verbalize_numeric_ordinals(
    text: str,
    *,
    format_ordinal: Callable[[int], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        ordinal = format_ordinal(int(match.group(1)))
        return ordinal if ordinal is not None else match.group(0)

    return _NUMERIC_ORDINAL_RE.sub(replace, text)


def verbalize_numeric_ordinal_ranges(
    text: str,
    *,
    format_ordinal: Callable[[int], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        start = format_ordinal(int(match.group(1)))
        end = format_ordinal(int(match.group(2)))
        if start is None or end is None:
            return match.group(0)
        return f"{start} to {end}"

    return _NUMERIC_ORDINAL_RANGE_RE.sub(replace, text)


def normalize_spoken_ordinals(
    text: str,
    *,
    parse_ordinal: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        value = parse_ordinal(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}{_ordinal_suffix(value)} {match.group(2)}"

    return _SPOKEN_ORDINAL_CONTEXT_RE.sub(replace, text)


def normalize_spoken_ordinal_ranges(
    text: str,
    *,
    parse_ordinal: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        start = parse_ordinal(match.group(2))
        end = parse_ordinal(match.group(3))
        if start is None or end is None:
            return match.group(0)
        return f"{match.group(1)}{start}{_ordinal_suffix(start)}-{end}{_ordinal_suffix(end)}"

    return _SPOKEN_ORDINAL_RANGE_CONTEXT_RE.sub(replace, text)


def verbalize_iso_date_ranges(text: str) -> str:
    return _ISO_DATE_RANGE_RE.sub(r"\1 to \2", text)


def normalize_spoken_numeric_dates(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
    parse_year: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        month = parse_integer(match.group(2))
        day = parse_integer(match.group(3))
        year = parse_year(match.group(4))
        if month is None or day is None or year is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}{year:04d}-{month:02d}-{day:02d}"

    return _SPOKEN_NUMERIC_DATE_RE.sub(replace, text)
