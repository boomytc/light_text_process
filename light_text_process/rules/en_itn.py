from __future__ import annotations
import re
from collections.abc import Callable
from light_text_process.rules.en_dates import (
    normalize_spoken_dotted_dates,
    normalize_spoken_month_name_dates,
    normalize_spoken_numeric_dates,
    normalize_spoken_ordinal_ranges,
    normalize_spoken_ordinals,
)


_NUMBER_WORD = (
    r"zero|oh|o|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million"
)

_INTEGER_PHRASE = rf"(?:\d+|(?:{_NUMBER_WORD})(?:[\s-]+(?:{_NUMBER_WORD}))*)"

_NUMBER_PHRASE = rf"{_INTEGER_PHRASE}(?:\s+point\s+(?:{_NUMBER_WORD})(?:\s+(?:{_NUMBER_WORD}))*)?"

_A_QUARTER_TIME_RE = re.compile(r"\ba\s+(quarter\s+(?:past|to)\s+)", re.IGNORECASE)

_HALF_QUANTITY_UNIT = (
    r"hours?|minutes?|seconds?|days?|weeks?|months?|years?|"
    r"miles?|yards?|feet|foot|inches?|pounds?|ounces?|"
    r"meters?|kilometers?|centimeters?|millimeters?|grams?|kilograms?|liters?|litres?"
)

_MIXED_HALF_QUANTITY_RE = re.compile(
    rf"\b({_INTEGER_PHRASE})\s+and\s+(?:a\s+half|one\s+half|half)\s+({_HALF_QUANTITY_UNIT})\b",
    re.IGNORECASE,
)

_NAMED_TIME_RE = re.compile(r"\b(noon|midnight)\b", re.IGNORECASE)

_SQUARE_FEET_RE = re.compile(rf"\b({_INTEGER_PHRASE})\s+square\s+(feet|foot)\b", re.IGNORECASE)

_SIGNED_NUMBER_PHRASE = rf"(?:(?:minus|negative)\s+)?{_NUMBER_PHRASE}"

_SPOKEN_TEMPERATURE_RANGE_RE = re.compile(
    rf"\b((?:temperature|temp|feels\s+like|feels|room\s+temperature|body\s+temperature)"
    rf"(?:\s+(?:is|was))?\s+)({_SIGNED_NUMBER_PHRASE})\s+to\s+"
    rf"({_SIGNED_NUMBER_PHRASE})\s+degrees?\s+(celsius|fahrenheit)\b",
    re.IGNORECASE,
)

_WEEKDAY = r"mon(?:day)?|tue(?:sday)?|wed(?:nesday)?|thu(?:rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?"

_SPOKEN_WEEKDAY_RANGE_RE = re.compile(rf"\b({_WEEKDAY})\s+to\s+({_WEEKDAY})\b", re.IGNORECASE)

_SPOKEN_RATING_RE = re.compile(
    rf"\b((?:rating|score|rated|stars?|n\s+p\s+s|nps)(?:\s+(?:is|was))?\s+)"
    rf"({_NUMBER_PHRASE})\s+out\s+of\s+({_NUMBER_PHRASE})\b",
    re.IGNORECASE,
)

_DURATION_HOUR_MINUTE_OUTPUT_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hours?)\s+(\d+(?:\.\d+)?)\s*(?:m|min|mins|minutes?)\b"
    r"(?!\s+\d+(?:\.\d+)?\s*(?:s|sec|secs|seconds?)\b)",
    re.IGNORECASE,
)

_DURATION_MINUTE_SECOND_OUTPUT_RE = re.compile(
    r"(?<!h )\b(\d+(?:\.\d+)?)\s*(?:m|min|mins|minutes?)\s+(\d+(?:\.\d+)?)\s*(?:s|sec|secs|seconds?)\b",
    re.IGNORECASE,
)

_SPOKEN_BUY_GET_RE = re.compile(
    rf"\bbuy\s+({_NUMBER_PHRASE})\s+get\s+({_NUMBER_PHRASE})\s+free\b",
    re.IGNORECASE,
)

_SPOKEN_MONEY_WITH_SUBUNITS_RE = re.compile(
    rf"\b({_NUMBER_PHRASE})\s+(dollars?|bucks?|euros?|pounds?)\s+(?:and\s+)?"
    rf"({_INTEGER_PHRASE})\s+(cents?|pence)\b",
    re.IGNORECASE,
)

_SPOKEN_BUCKS_MINOR_RE = re.compile(
    rf"\b({_NUMBER_PHRASE})\s+bucks?\s+(?:and\s+)?({_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_ASR_FILLER_RE = re.compile(
    r"(?m)^[\s,]*(?:um|uh|er|ah|like|you know)\b[\s,]*|[\s,]*\b(?:you know|um|uh|er|ah)[\s,]*$",
    re.IGNORECASE,
)

_SPOKEN_PUNCTUATION_RE = re.compile(
    r"\b(open parenthesis|close parenthesis|left parenthesis|right parenthesis|"
    r"open bracket|close bracket|left bracket|right bracket|"
    r"quote|unquote|comma|period|full stop|question mark|exclamation mark|"
    r"colon|semicolon)\b",
    re.IGNORECASE,
)

_SPOKEN_PUNCTUATION = {
    "comma": ",",
    "period": ".",
    "full stop": ".",
    "question mark": "?",
    "exclamation mark": "!",
    "colon": ":",
    "semicolon": ";",
    "open parenthesis": "(",
    "left parenthesis": "(",
    "close parenthesis": ")",
    "right parenthesis": ")",
    "open bracket": "[",
    "left bracket": "[",
    "close bracket": "]",
    "right bracket": "]",
    "quote": '"',
    "unquote": '"',
}

_CURRENCY_PER_UNIT_OUTPUT_RE = re.compile(
    r"(?<!\w)([$€£¥]\d[\d,]*(?:\.\d+)?)\s+per\s+"
    r"(kg|kilograms?|g|grams?|lb|pounds?|oz|ounces?|h|hr|hours?|day|days|month|months|year|years|"
    r"square\s+meters?|m²|㎡|m|meters?|km|kilometers?)(?![A-Za-z])",
    re.IGNORECASE,
)

_DATA_SIZE_RE = re.compile(
    rf"\b({_NUMBER_PHRASE})\s+(bytes?|kilobytes?|megabytes?|gigabytes?|terabytes?)\b",
    re.IGNORECASE,
)

_DATA_BYTE_RATE_RE = re.compile(
    rf"\b({_NUMBER_PHRASE})\s+(bytes?|kilobytes?|megabytes?|gigabytes?|terabytes?)\s+per\s+seconds?\b",
    re.IGNORECASE,
)

_DATA_BIT_RATE_RE = re.compile(
    rf"\b({_NUMBER_PHRASE})\s+(bits?|kilobits?|megabits?|gigabits?|terabits?)\s+per\s+seconds?\b",
    re.IGNORECASE,
)

_ORDINAL_DIGIT_FRACTION_RE = re.compile(
    rf"\b({_INTEGER_PHRASE})\s+([2-9]|1[0-2])(?:st|nd|rd|th)s?\b",
    re.IGNORECASE,
)

_SPOKEN_DIGIT_MULTIPLIER_RE = re.compile(
    rf"\b(double|triple|quadruple)\s+({_NUMBER_WORD})\b",
    re.IGNORECASE,
)

_SPOKEN_DOZEN_RE = re.compile(
    rf"\b(?:(a)\s+|(?:({_INTEGER_PHRASE})\s+)|)dozen\b",
    re.IGNORECASE,
)

_DIGIT_WORD_MAP = {
    "zero": "0", "oh": "0", "o": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
}

_DIGIT_MULTIPLIER_MAP = {"double": 2, "triple": 3, "quadruple": 4}

_WEEKDAY_NAMES = {
    "mon": "Monday",
    "monday": "Monday",
    "tue": "Tuesday",
    "tuesday": "Tuesday",
    "wed": "Wednesday",
    "wednesday": "Wednesday",
    "thu": "Thursday",
    "thursday": "Thursday",
    "fri": "Friday",
    "friday": "Friday",
    "sat": "Saturday",
    "saturday": "Saturday",
    "sun": "Sunday",
    "sunday": "Sunday",
}

def normalize_colloquial_time_prefixes(text: str) -> str:
    return _A_QUARTER_TIME_RE.sub(r"\1", text)

def normalize_spoken_punctuation(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1).lower()
        if token == "quote":
            return " __OPEN_QUOTE__ "
        if token == "unquote":
            return " __CLOSE_QUOTE__ "
        marker = {
            ",": "COMMA",
            ".": "PERIOD",
            "?": "QUESTION",
            "!": "EXCLAMATION",
            ":": "COLON",
            ";": "SEMICOLON",
            "(": "OPEN_PAREN",
            ")": "CLOSE_PAREN",
            "[": "OPEN_BRACKET",
            "]": "CLOSE_BRACKET",
        }[_SPOKEN_PUNCTUATION[token]]
        return f" __PUNCT_{marker}__ "

    normalized = _SPOKEN_PUNCTUATION_RE.sub(replace, text)
    for marker, symbol in {
        "COMMA": ",",
        "PERIOD": ".",
        "QUESTION": "?",
        "EXCLAMATION": "!",
        "COLON": ":",
        "SEMICOLON": ";",
    }.items():
        normalized = re.sub(rf"\s*__PUNCT_{marker}__\s*", f"{symbol} ", normalized)
    normalized = re.sub(r"\s*__PUNCT_OPEN_PAREN__\s*", " (", normalized)
    normalized = re.sub(r"\s*__PUNCT_CLOSE_PAREN__\s*", ") ", normalized)
    normalized = re.sub(r"\s*__PUNCT_OPEN_BRACKET__\s*", " [", normalized)
    normalized = re.sub(r"\s*__PUNCT_CLOSE_BRACKET__\s*", "] ", normalized)
    normalized = re.sub(r"\s*__OPEN_QUOTE__\s*", ' "', normalized)
    normalized = re.sub(
        r"\s*__CLOSE_QUOTE__\s*([,.;:?!])?",
        lambda match: f'"{match.group(1) or " "}',
        normalized,
    )
    return re.sub(r"\s{2,}", " ", normalized).strip()

def remove_asr_fillers(text: str) -> str:
    normalized = text
    while True:
        next_normalized = _ASR_FILLER_RE.sub("", normalized).strip()
        if next_normalized == normalized:
            return normalized
        normalized = next_normalized

def normalize_half_quantities(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        value = parse_integer(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value + 0.5:g} {match.group(2)}"

    return _MIXED_HALF_QUANTITY_RE.sub(replace, text)

def normalize_named_times(text: str) -> str:
    return _NAMED_TIME_RE.sub(lambda match: "12:00" if match.group(1).lower() == "noon" else "00:00", text)

def normalize_weekday_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _WEEKDAY_NAMES[match.group(1).lower()].lower()
        end = _WEEKDAY_NAMES[match.group(2).lower()].lower()
        return f"{start}-{end}"

    return _SPOKEN_WEEKDAY_RANGE_RE.sub(replace, text)

def normalize_spoken_ratings(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        numerator = parse_number(match.group(2))
        denominator = parse_number(match.group(3))
        if numerator is None or denominator is None:
            return match.group(0)
        context = re.sub(r"\bn\s+p\s+s\b", "NPS", match.group(1), flags=re.IGNORECASE)
        return f"{context}{numerator}/{denominator}"

    return _SPOKEN_RATING_RE.sub(replace, text)

def compact_duration_sequences(text: str) -> str:
    prepared = _DURATION_HOUR_MINUTE_OUTPUT_RE.sub(r"\1h\2min", text)
    return _DURATION_MINUTE_SECOND_OUTPUT_RE.sub(r"\1min\2s", prepared)

def normalize_buy_get_promotions(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        buy = parse_number(match.group(1))
        get = parse_number(match.group(2))
        if buy is None or get is None:
            return match.group(0)
        return f"buy {buy} get {get} free"

    return _SPOKEN_BUY_GET_RE.sub(replace, text)

def normalize_spoken_money_with_subunits(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
    parse_integer: Callable[[str], int | None],
) -> str:
    currency_symbols = {
        "dollar": "$",
        "dollars": "$",
        "buck": "$",
        "bucks": "$",
        "euro": "€",
        "euros": "€",
        "pound": "£",
        "pounds": "£",
    }

    def replace(match: re.Match[str]) -> str:
        major = parse_number(match.group(1))
        minor = parse_integer(match.group(3))
        if major is None or minor is None or not 0 <= minor <= 99:
            return match.group(0)
        return f"{currency_symbols[match.group(2).lower()]}{major}.{minor:02d}"

    def replace_bucks_minor(match: re.Match[str]) -> str:
        major = parse_number(match.group(1))
        minor = parse_integer(match.group(2))
        if major is None or minor is None or not 0 <= minor <= 99:
            return match.group(0)
        return f"${major}.{minor:02d}"

    normalized = _SPOKEN_MONEY_WITH_SUBUNITS_RE.sub(replace, text)
    return _SPOKEN_BUCKS_MINOR_RE.sub(replace_bucks_minor, normalized)

def compact_currency_per_units(text: str) -> str:
    unit_symbols = {
        "kg": "kg",
        "kilogram": "kg",
        "kilograms": "kg",
        "g": "g",
        "gram": "g",
        "grams": "g",
        "lb": "lb",
        "pound": "lb",
        "pounds": "lb",
        "oz": "oz",
        "ounce": "oz",
        "ounces": "oz",
        "h": "h",
        "hr": "h",
        "hour": "h",
        "hours": "h",
        "day": "day",
        "days": "day",
        "month": "month",
        "months": "month",
        "year": "year",
        "years": "year",
        "m²": "m²",
        "㎡": "m²",
        "square meter": "m²",
        "square meters": "m²",
        "m": "m",
        "meter": "m",
        "meters": "m",
        "km": "km",
        "kilometer": "km",
        "kilometers": "km",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}/{unit_symbols[match.group(2).lower()]}"

    return _CURRENCY_PER_UNIT_OUTPUT_RE.sub(replace, text)

def normalize_data_units(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    size_symbols = {
        "byte": "B",
        "kilobyte": "KB",
        "megabyte": "MB",
        "gigabyte": "GB",
        "terabyte": "TB",
    }
    bit_rate_symbols = {
        "bit": "bps",
        "kilobit": "kbps",
        "megabit": "Mbps",
        "gigabit": "Gbps",
        "terabit": "Tbps",
    }

    def replace_byte_rate(match: re.Match[str]) -> str:
        value = parse_number(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {size_symbols[unit]}/s"

    def replace_bit_rate(match: re.Match[str]) -> str:
        value = parse_number(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {bit_rate_symbols[unit]}"

    def replace_size(match: re.Match[str]) -> str:
        value = parse_number(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {size_symbols[unit]}"

    prepared = _DATA_BYTE_RATE_RE.sub(replace_byte_rate, text)
    prepared = _DATA_BIT_RATE_RE.sub(replace_bit_rate, prepared)
    return _DATA_SIZE_RE.sub(replace_size, prepared)

def compact_ordinal_digit_fractions(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        numerator = parse_integer(match.group(1))
        if numerator is None:
            return match.group(0)
        return f"{numerator}/{match.group(2)}"

    return _ORDINAL_DIGIT_FRACTION_RE.sub(replace, text)

def compact_square_feet(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        value = parse_number(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value} ft²"

    return _SQUARE_FEET_RE.sub(replace, text)

def normalize_spoken_temperature_ranges(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    unit_symbols = {"celsius": "°C", "fahrenheit": "°F"}

    def parse_signed(raw: str) -> str | None:
        normalized = raw.lower().strip()
        sign = ""
        for prefix in ("minus ", "negative "):
            if normalized.startswith(prefix):
                sign = "-"
                normalized = normalized[len(prefix) :]
                break
        value = parse_number(normalized)
        if value is None:
            return None
        return f"{sign}{value}"

    def replace(match: re.Match[str]) -> str:
        start = parse_signed(match.group(2))
        end = parse_signed(match.group(3))
        if start is None or end is None:
            return match.group(0)
        return f"{match.group(1)}{start}-{end}{unit_symbols[match.group(4).lower()]}"

    return _SPOKEN_TEMPERATURE_RANGE_RE.sub(replace, text)

def normalize_spoken_digit_multipliers(
    text: str,
    *,
    parse_number: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        multiplier = _DIGIT_MULTIPLIER_MAP[match.group(1).lower()]
        digit_word = match.group(2).lower().strip()
        digit = _DIGIT_WORD_MAP.get(digit_word)
        if digit is not None:
            return digit * multiplier
        value = parse_number(match.group(2))
        if value is not None and value.isdigit() and len(value) == 1:
            return value * multiplier
        return match.group(0)

    return _SPOKEN_DIGIT_MULTIPLIER_RE.sub(replace, text)

def normalize_spoken_dozens(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        if match.group(1):
            return "12"
        if match.group(2):
            count = parse_integer(match.group(2))
            if count is not None:
                return str(count * 12)
        return match.group(0)

    return _SPOKEN_DOZEN_RE.sub(replace, text)

_EN_ITN_PERCENT_SPACE_RE = re.compile(r"(\d+(?:\.\d+)?)\s+%")

def _restore_itn_format_symbol_match(match: re.Match[str]) -> str:
    symbol = chr(int(match.group(1), 16))
    return f"{symbol} " if symbol == "%" and match.group(2) else symbol

_EN_ITN_NEGATIVE_CURRENCY_RE = re.compile(r"\b(?:minus|negative)\s+([$€£])(\d+(?:\.\d+)?)")

_EN_ITN_POSITIVE_PERCENT_RE = re.compile(r"\bplus\s+(\d+(?:\.\d+)?)\s*%")

_EN_ITN_DOTTED_VERSION_SPACE_RE = re.compile(r"(?<=\d)\s+\.(?=\d)")

_EN_ITN_SPOKEN_COLON_TIME_OUTPUT_RE = re.compile(r"\b(\d{1,2})\s+:\s+([0-5]\d)\b")

_EN_ITN_EXT_OUTPUT_RE = re.compile(r"\bext\s+(\d{1,6})\b", re.IGNORECASE)

_EN_ITN_TIME_SECONDS_OUTPUT_RE = re.compile(
    r"\b(\d{1,2}:\d{2})\s+oh\s+(zero|one|two|three|four|five|six|seven|eight|nine)\b",
    re.IGNORECASE,
)

_EN_ITN_EXPLICIT_EMAIL_RE = re.compile(
    r"\b((?:e-?mail|mail|contact|address)\s+)"
    r"((?:[A-Za-z0-9._+-]+|dot|plus|dash|hyphen|underscore)"
    r"(?:\s+(?:[A-Za-z0-9]+|dot|plus|dash|hyphen|underscore))*)"
    r"\s+at\s+((?:[A-Za-z0-9-]+\s+dot\s+)+(?:[A-Za-z0-9-]+\.)?[A-Za-z]{2,}|"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    re.IGNORECASE,
)

_EN_ITN_KILOWATT_HOURS_RE = re.compile(r"\bkilowatt\s+hours?\b", re.IGNORECASE)

_EN_ITN_MILLIAMPERES_RE = re.compile(r"\bmilliamperes\b", re.IGNORECASE)

_EN_ITN_DIGIT_PER_MILLE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s+per\s+mille\b", re.IGNORECASE)

_EN_ITN_WORD_PER_MILLE_RE = re.compile(
    r"\b(a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+per\s+mille\b",
    re.IGNORECASE,
)

_EN_ITN_FTP_URL_RE = re.compile(
    r"\bf t p\s+colon(?://|\s+slash\s+slash)\s+"
    r"([A-Za-z0-9-]+(?:\s+dot\s+[A-Za-z0-9-]+)+(?:/[A-Za-z0-9._-]+)?)",
    re.IGNORECASE,
)

_EN_ITN_SPOKEN_DOMAIN_RE = re.compile(
    r"\b((?:w\s+){2}w|[A-Za-z0-9-]+)\s+dot\s+"
    r"([A-Za-z0-9-]+(?:\s+dot\s+[A-Za-z0-9-]+)+"
    r"(?:\s+slash\s+[A-Za-z0-9._-]+)?)",
    re.IGNORECASE,
)

_EN_ITN_PARTIAL_WWW_DOMAIN_RE = re.compile(
    r"\bw\s+w\s+w\s+dot\s+([A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[A-Za-z0-9._-]+)?)",
    re.IGNORECASE,
)

_EN_ITN_NEGATIVE_MEASURE_RE = re.compile(
    r"\bnegative\s+(\d+(?:\.\d+)?)(?=(?:\s*%)|\s+(?:degrees?\s+celsius|degrees?\s+fahrenheit|"
    r"celsius|fahrenheit|meters?|kilometers?|centimeters?|millimeters?|grams?|kilograms?|volts?))",
    re.IGNORECASE,
)

_EN_ITN_FRAMES_PER_SECOND_OUTPUT_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s+frames\s+per\s+(?:second|2nd)\b",
    re.IGNORECASE,
)

_EN_ITN_WEIGHT_POUNDS_OUTPUT_RE = re.compile(
    r"\b(weight|weighs|weighed|weighing)\s+£(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)

_EN_ITN_INCH_QUOTE_OUTPUT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s+\"")

_EN_ITN_COMMON_FRACTION_RE = re.compile(
    r"\b(a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(half|halves|quarter|quarters|third|thirds|fourth|fourths|fifth|fifths|"
    r"sixth|sixths|seventh|sevenths|eighth|eighths|ninth|ninths|tenth|tenths)\b",
    re.IGNORECASE,
)

_EN_ITN_TIME_OH_RE = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+oh\s+"
    r"(one|two|three|four|five|six|seven|eight|nine)\b",
    re.IGNORECASE,
)

_EN_ITN_LEADING_ZERO_TIME_OH_RE = re.compile(
    r"\bzero\s+(one|two|three|four|five|six|seven|eight|nine)\s+oh\s+"
    r"(one|two|three|four|five|six|seven|eight|nine)\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXT_CODE_RE = re.compile(
    r"\b((?:order|invoice|tracking|ticket|sku|serial|case|shipment|code|id|issue|priority|"
    r"license\s+plate|plate|vin|passport|driver'?s?\s+license|driver\s+license)"
    r"(?:\s+(?:number|no|id))?\s+)"
    r"((?:[A-Za-z]|zero|oh|one|two|three|four|five|six|seven|eight|nine|dash|hyphen)"
    r"(?:\s+(?:[A-Za-z]|zero|oh|one|two|three|four|five|six|seven|eight|nine|dash|hyphen))*)\b",
    re.IGNORECASE,
)

_EN_ITN_ZIP_CODE_RE = re.compile(
    r"\b(zip(?:\s+code)?\s+)"
    r"((?:zero|oh|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:\s+(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)){4}"
    r"(?:\s+(?:dash|hyphen)\s+(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:\s+(?:zero|oh|one|two|three|four|five|six|seven|eight|nine)){3})?)\b",
    re.IGNORECASE,
)

_EN_ITN_ROOM_CODE_RE = re.compile(
    r"\b((?:meeting\s+room|conference\s+room|room|suite|apartment|apt|unit|building|seat|gate|parking)\s+)"
    r"((?:[A-Za-z]|zero|oh|o|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|dash|hyphen)"
    r"(?:\s+(?:[A-Za-z]|zero|oh|o|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|dash|hyphen))*)\b",
    re.IGNORECASE,
)

_EN_ITN_EXTENSION_RE = re.compile(
    r"\bextension\s+((?:zero|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:\s+(?:zero|one|two|three|four|five|six|seven|eight|nine))*)\b",
    re.IGNORECASE,
)

_EN_ITN_SPOKEN_PHONE_DIGIT = r"(?:zero|oh|o|one|two|three|four|five|six|seven|eight|nine)"

_EN_ITN_SPOKEN_PHONE_NUMBER_RE = re.compile(
    rf"\b((?:phone\s+number|phone|tel|mobile|cell|cellphone|hotline|support)\s+)"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\b",
    re.IGNORECASE,
)

_EN_ITN_SPOKEN_TOLL_FREE_PHONE_RE = re.compile(
    rf"\b((?:call|phone|tel|mobile|hotline|support)\s+)"
    rf"(?:(one)\s+)?(?:eight\s+hundred|eight\s+zero\s+zero)\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\b",
    re.IGNORECASE,
)

_EN_ITN_LAST_FOUR_RE = re.compile(
    rf"\b((?:last\s+four|last\s+four\s+digits|ending\s+in)\s+)"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+"
    rf"({_EN_ITN_SPOKEN_PHONE_DIGIT})\s+({_EN_ITN_SPOKEN_PHONE_DIGIT})\b",
    re.IGNORECASE,
)

_EN_ITN_BLANK_LINE_COMMAND_RE = re.compile(r"\b(?:blank\s+line|empty\s+line)\b", re.IGNORECASE)

_EN_ITN_LINE_BREAK_COMMAND_RE = re.compile(r"\b(?:new\s+line|newline|line\s+break|next\s+line)\b", re.IGNORECASE)

_EN_ITN_TAB_COMMAND_RE = re.compile(r"\b(?:tab\s+character|tab\s+char)\b", re.IGNORECASE)

_EN_ITN_BULLET_COMMAND_RE = re.compile(r"\b(?:bullet\s+point|bullet)\b", re.IGNORECASE)

_EN_ITN_HEADING_COMMAND_RE = re.compile(r"\bheading(?:\s+level)?\s+(one|two|three|1|2|3)\b", re.IGNORECASE)

_EN_ITN_ORDERED_ITEM_COMMAND_RE = re.compile(
    r"(^|\n)[ \t]*(?:(?:numbered\s+item|item|number)\s+)"
    r"(one|two|three|four|five|six|seven|eight|nine|ten|[1-9])\b[ \t]*",
    re.IGNORECASE,
)

_EN_ITN_BOLD_SPAN_RE = re.compile(r"\bbold\s+start\s+(.+?)\s+bold\s+end\b", re.IGNORECASE | re.DOTALL)

_EN_ITN_CODE_SPAN_RE = re.compile(r"\bcode\s+start\s+(.+?)\s+code\s+end\b", re.IGNORECASE | re.DOTALL)

_EN_ITN_FORMAT_SYMBOL_COMMAND_RE = re.compile(
    r"\b(forward\s+slash|slash|dash|hyphen|at\s+sign|hash\s+sign|pound\s+sign|underscore|"
    r"equals?\s+sign|plus\s+sign|minus\s+sign|percent\s+sign|asterisk|ampersand|"
    r"check\s+mark|checkmark|cross\s+mark|x\s+mark|"
    r"open\s+(?:curly\s+)?brace|close\s+(?:curly\s+)?brace|left\s+(?:curly\s+)?brace|right\s+(?:curly\s+)?brace|"
    r"left\s+angle\s+bracket|right\s+angle\s+bracket|backslash|pipe|vertical\s+bar|tilde)\b",
    re.IGNORECASE,
)

_EN_ITN_NUMBER_WORD_VALUES = {
    "a": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}

_EN_ITN_DENOMINATOR_WORD_VALUES = {
    "half": 2,
    "halves": 2,
    "quarter": 4,
    "quarters": 4,
    "third": 3,
    "thirds": 3,
    "fourth": 4,
    "fourths": 4,
    "fifth": 5,
    "fifths": 5,
    "sixth": 6,
    "sixths": 6,
    "seventh": 7,
    "sevenths": 7,
    "eighth": 8,
    "eighths": 8,
    "ninth": 9,
    "ninths": 9,
    "tenth": 10,
    "tenths": 10,
}

_EN_ITN_INTEGER_VALUE_WORD = (
    r"zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million"
)

_EN_ITN_INTEGER_PHRASE = (
    rf"(?:\d+|(?:{_EN_ITN_INTEGER_VALUE_WORD})"
    rf"(?:[\s-]+(?:and[\s-]+)?(?:{_EN_ITN_INTEGER_VALUE_WORD}))*)"
)

_EN_ITN_NUMBER_PHRASE = (
    rf"(?:\d+(?:\.\d+)?|(?:{_EN_ITN_INTEGER_VALUE_WORD})"
    rf"(?:[\s-]+(?:and[\s-]+)?(?:{_EN_ITN_INTEGER_VALUE_WORD}))*)"
)

_EN_ITN_INTEGER_PHRASE_NO_AND = (
    rf"(?:\d+|(?:{_EN_ITN_INTEGER_VALUE_WORD})(?:[\s-]+(?:{_EN_ITN_INTEGER_VALUE_WORD}))*)"
)

_EN_ITN_CONTEXT_YEAR_CODE_RE = re.compile(
    rf"\b((?:order|invoice|tracking|ticket|sku|serial|case|shipment|code|id)"
    rf"(?:\s+(?:number|no|id))?\s+)"
    rf"((?:[A-Za-z]\s+)+)(?:dash|hyphen)\s+({_EN_ITN_INTEGER_PHRASE})\s+"
    r"(?:dash|hyphen)\s+((?:zero|oh|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:\s+(?:zero|oh|one|two|three|four|five|six|seven|eight|nine))*)\b",
    re.IGNORECASE,
)

_EN_ITN_ORDINAL_VALUE_WORD = (
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|"
    r"twentieth|thirtieth"
)

_EN_ITN_ORDINAL_PHRASE = (
    rf"(?:{_EN_ITN_ORDINAL_VALUE_WORD}|"
    rf"(?:twenty|thirty)[\s-]+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth))"
)

_EN_ITN_MONTH_NAME = (
    r"january|jan\.?|february|feb\.?|march|mar\.?|april|apr\.?|may|june|jun\.?|july|jul\.?|"
    r"august|aug\.?|september|sep\.?|sept\.?|october|oct\.?|november|nov\.?|december|dec\.?"
)

_EN_ITN_QUARTER_VALUE = r"1|2|3|4|one|two|three|four"

_EN_ITN_QUARTER_RE = re.compile(
    rf"\bq\s+({_EN_ITN_QUARTER_VALUE})\s+({_EN_ITN_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_FISCAL_YEAR_RE = re.compile(
    rf"\bfiscal\s+year\s+({_EN_ITN_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_FILE_CONTEXT_RE = re.compile(
    r"\b((?:filename|(?<!slash )path|directory|dir|file(?!\s+(?:is|was|size|weighs?)\b))\s+)"
    r"(.+?)(?=\s+(?:file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_FILE_DATA_QUANTITY_PREFIX_RE = re.compile(
    r"^\s*\d+(?:\.\d+)?\s*"
    r"(?:B|KB|MB|GB|TB|KiB|MiB|GiB|bps|kbps|Mbps|Gbps|Tbps|B/s|KB/s|MB/s|GB/s|TB/s)\b",
    re.IGNORECASE,
)

_EN_ITN_VERSION_FRACTION_TOKEN = r"\d+|zero|oh|o|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"

_EN_ITN_CONTEXT_DECIMAL_VERSION_RE = re.compile(
    rf"\b((?:version|release|build)\s+)"
    rf"({_EN_ITN_INTEGER_PHRASE_NO_AND}(?:\s+point\s+"
    rf"(?:{_EN_ITN_VERSION_FRACTION_TOKEN})(?:\s+(?:{_EN_ITN_VERSION_FRACTION_TOKEN}))*)+)\b",
    re.IGNORECASE,
)

_EN_ITN_DIGIT_WORD = r"zero|oh|one|two|three|four|five|six|seven|eight|nine"

_EN_ITN_DIGIT_TOKEN = rf"(?:{_EN_ITN_DIGIT_WORD})"

_EN_ITN_DECIMAL_NUMBER_PHRASE = (
    rf"(?:{_EN_ITN_NUMBER_PHRASE})(?:\s+point\s+{_EN_ITN_DIGIT_TOKEN}(?:\s+{_EN_ITN_DIGIT_TOKEN})*)?"
)

_EN_ITN_MINUTE_PHRASE = (
    rf"(?:(?:oh|o)\s+{_EN_ITN_DIGIT_TOKEN}|zero\s+{_EN_ITN_DIGIT_TOKEN}|{_EN_ITN_INTEGER_PHRASE_NO_AND})"
)

_EN_ITN_HOUR_PHRASE = (
    r"(?:\d{1,2}|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty(?:\s+(?:one|two|three))?)"
)

_EN_ITN_CLOCK_TIME_RE = re.compile(
    rf"\b((?:at|by|from|to|until|before|after|around|about|time\s+is|callback\s+time|appointment\s+time)\s+)"
    rf"({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+({_EN_ITN_MINUTE_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_RELATIVE_CLOCK_TIME_RE = re.compile(
    rf"\b((?:at|by|from|to|until|before|after|around|about|time\s+is|callback\s+time|appointment\s+time)\s+)"
    rf"(?:(?:a\s+)?(quarter)\s+(past|to)|(half)\s+past)\s+({_EN_ITN_HOUR_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_DAYPART_CLOCK_OUTPUT_RE = re.compile(
    r"\b(\d{1,2}:[0-5]\d)\s+in\s+the\s+(morning|afternoon|evening)\b",
    re.IGNORECASE,
)

_EN_ITN_CLOCK_TIME_RANGE_RE = re.compile(
    rf"\b((?:office\s+hours|business\s+hours|hours|meeting|time|from|between)\s+)"
    rf"({_EN_ITN_HOUR_PHRASE})(?:\s+({_EN_ITN_MINUTE_PHRASE}))?\s+to\s+"
    rf"({_EN_ITN_HOUR_PHRASE})(?:\s+({_EN_ITN_MINUTE_PHRASE}))\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXT_HOUR_ONLY_CLOCK_TIME_RANGE_RE = re.compile(
    rf"\b((?:office\s+hours|business\s+hours|hours)\s+)"
    rf"({_EN_ITN_HOUR_PHRASE})\s+to\s+({_EN_ITN_HOUR_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_BARE_CLOCK_TIME_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_HOUR_PHRASE})\s+({_EN_ITN_MINUTE_PHRASE})\s+to\s+"
    rf"({_EN_ITN_HOUR_PHRASE})\s+({_EN_ITN_MINUTE_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_PLUS_MINUS_RE = re.compile(
    rf"\bplus\s+or\s+minus\s+({_EN_ITN_DECIMAL_NUMBER_PHRASE})"
    r"(?:\s+(percent|degrees?\s+celsius|degrees?\s+fahrenheit|millimeters?|centimeters?|meters?|kilometers?|"
    r"grams?|kilograms?))?\b",
    re.IGNORECASE,
)

_EN_ITN_PLUS_OR_SIGNED_RE = re.compile(
    r"\bplus\s+or\s+-(\d+(?:\.\d+)?)"
    r"(?:\s+(percent|degrees?\s+celsius|degrees?\s+fahrenheit|millimeters?|centimeters?|meters?|kilometers?|"
    r"grams?|kilograms?|mm|cm|m|km|g|kg))?\b",
    re.IGNORECASE,
)

_EN_ITN_HTTP_STATUS_RE = re.compile(
    rf"\b((?:HTTP|HTTPS)\s+)({_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN})\b",
    re.IGNORECASE,
)

_EN_ITN_PORT_RE = re.compile(
    rf"\b(port\s+)({_EN_ITN_DIGIT_TOKEN}(?:\s+{_EN_ITN_DIGIT_TOKEN}){{1,4}})\b",
    re.IGNORECASE,
)

_EN_ITN_ISO_DATETIME_RE = re.compile(
    rf"\b((?:{_EN_ITN_DIGIT_TOKEN}\s+){{3}}{_EN_ITN_DIGIT_TOKEN}\s+(?:dash|hyphen)\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+(?:dash|hyphen)\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+[Tt]\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+colon\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}"
    rf"(?:\s+colon\s+{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN})?(?:\s+[Zz])?)\b",
    re.IGNORECASE,
)

_EN_ITN_SPACE_DATETIME_RE = re.compile(
    rf"\b((?:{_EN_ITN_DIGIT_TOKEN}\s+){{3}}{_EN_ITN_DIGIT_TOKEN}\s+(?:dash|hyphen)\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+(?:dash|hyphen)\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN})\s+"
    rf"({_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}\s+colon\s+"
    rf"{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN}"
    rf"(?:\s+colon\s+{_EN_ITN_DIGIT_TOKEN}\s+{_EN_ITN_DIGIT_TOKEN})?)\b",
    re.IGNORECASE,
)

_EN_ITN_SHORTCUT_TOKEN = (
    rf"(?:control|ctrl|command|cmd|shift|alt|option|meta|windows|win|function|fn|"
    rf"escape|esc|tab|enter|return|space|delete|del|backspace|"
    rf"f\s+{_EN_ITN_DIGIT_TOKEN}(?:\s+{_EN_ITN_DIGIT_TOKEN})?|[A-Za-z])"
)

_EN_ITN_SHORTCUT_RE = re.compile(
    rf"\b({_EN_ITN_SHORTCUT_TOKEN}(?:\s+plus\s+{_EN_ITN_SHORTCUT_TOKEN}){{1,5}})\b",
    re.IGNORECASE,
)

_EN_ITN_ELECTRONIC_WORD = (
    r"zero|oh|one|two|three|four|five|six|seven|eight|nine|[A-Za-z][A-Za-z0-9]*|"
    r"slash|backslash|dot|point|underscore|dash|hyphen|colon|tilde|"
    r"question|mark|equal|sign|equals|ampersand|hash|plus"
)

_EN_ITN_URL_RE = re.compile(
    rf"\b((?:h\s+t\s+t\s+p\s+s|h\s+t\s+t\s+p|f\s+t\s+p|https|http|ftp)"
    rf"\s+colon\s+slash\s+slash\s+(?:{_EN_ITN_ELECTRONIC_WORD})"
    rf"(?:\s+(?:{_EN_ITN_ELECTRONIC_WORD}))*?)"
    r"(?=\s+(?:email|file|filename|path|directory|dir|handle|account|hashtag|server|host|"
    r"mac|bssid|uuid|isbn|doi|version|release|tag|package)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_SEMVER_RE = re.compile(
    rf"\b((?:version|release)\s+)"
    rf"((?:{_EN_ITN_ELECTRONIC_WORD})(?:\s+(?:{_EN_ITN_ELECTRONIC_WORD}))*?)"
    r"(?=\s+(?:email|file|filename|path|directory|dir|handle|account|hashtag|server|host|"
    r"mac|bssid|uuid|isbn|doi|url|link|package)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_IPV4_OCTET = rf"(?:{_EN_ITN_DIGIT_WORD})(?:\s+(?:{_EN_ITN_DIGIT_WORD})){{0,2}}"

_EN_ITN_IPV4_PORT_RE = re.compile(
    rf"\b({_EN_ITN_IPV4_OCTET}(?:\s+(?:dot|point)\s+{_EN_ITN_IPV4_OCTET}){{3}}"
    rf"\s+colon\s+(?:{_EN_ITN_DIGIT_WORD})(?:\s+(?:{_EN_ITN_DIGIT_WORD})){{0,4}})\b",
    re.IGNORECASE,
)

_EN_ITN_IPV6_RE = re.compile(
    rf"\b(ipv6\s+)((?:{_EN_ITN_ELECTRONIC_WORD})(?:\s+(?:{_EN_ITN_ELECTRONIC_WORD}))*?)"
    r"(?=\s+(?:server|host|port|url|email|mac|bssid|uuid|color|colour|hex|"
    r"file|filename|path|directory|dir|handle|account|hashtag|isbn|doi)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_ISBN_RE = re.compile(
    rf"\b(ISBN(?:-1[03])?\s+)((?:{_EN_ITN_ELECTRONIC_WORD})(?:\s+(?:{_EN_ITN_ELECTRONIC_WORD}))*?)"
    r"(?=\s+(?:server|host|port|url|email|mac|bssid|uuid|color|colour|hex|"
    r"file|filename|path|directory|dir|handle|account|hashtag|ipv6|doi)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_DOI_RE = re.compile(
    rf"\b(DOI\s+)((?:{_EN_ITN_ELECTRONIC_WORD})(?:\s+(?:{_EN_ITN_ELECTRONIC_WORD}))*?)"
    r"(?=\s+(?:server|host|port|url|email|mac|bssid|uuid|color|colour|hex|"
    r"file|filename|path|directory|dir|handle|account|hashtag|ipv6|isbn)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_SOCIAL_HANDLE_RE = re.compile(
    r"\b((?:handle|account|user)\s+)at\s+"
    r"(.+?)(?=\s+(?:file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_SOCIAL_HASHTAG_RE = re.compile(
    r"\b(hashtag\s+)hash\s+"
    r"(.+?)(?=\s+(?:file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_PARAMETER_RE = re.compile(
    r"\b((?:parameter|param|query|field)\s+)"
    r"([A-Za-z][A-Za-z0-9_]*)\s+(?:equals?\s+sign|equals?|equal)\s+"
    r"(.+?)(?=\s+(?:parameter|param|query|field|code|ticket|order|case|file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_MAC_ADDRESS_RE = re.compile(
    r"\b((?:MAC(?:\s+address)?|BSSID)\s+)"
    r"(.+?)(?=\s+(?:UUID|color|colour|hex|file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_UUID_RE = re.compile(
    r"\b(UUID\s+)"
    r"(.+?)(?=\s+(?:MAC|BSSID|color|colour|hex|file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_HEX_COLOR_RE = re.compile(
    r"\b((?:color|colour|hex(?:\s+color)?|background(?:\s+color)?|foreground(?:\s+color)?)\s+)hash\s+"
    r"(.+?)(?=\s+(?:MAC|BSSID|UUID|file|filename|path|directory|dir|handle|account|hashtag)\s+|$|[,.])",
    re.IGNORECASE,
)

_EN_ITN_FAHRENHEIT_OUTPUT_RE = re.compile(r"\b(-?\d+(?:\.\d+)?)\s+degrees?\s+fahrenheit\b", re.IGNORECASE)

_EN_ITN_CELSIUS_OUTPUT_RE = re.compile(r"\b(-?\d+(?:\.\d+)?)\s+degrees?\s+celsius\b", re.IGNORECASE)

_EN_ITN_SPOKEN_NEGATIVE_TEMPERATURE_RE = re.compile(
    rf"\b(?:minus|negative)\s+({_EN_ITN_NUMBER_PHRASE})\s+(?:degrees?\s+)?(celsius|fahrenheit)\b",
    re.IGNORECASE,
)

_EN_ITN_AM_PM_OUTPUT_RE = re.compile(r"\b(\d{1,2}:\d{2})\s+([AP])\s*\.?\s*M\.?(?=\W|$)", re.IGNORECASE)

_EN_ITN_PHONE_PLUS_OUTPUT_RE = re.compile(r"\b(call|phone|tel|mobile|hotline)\+", re.IGNORECASE)

_EN_ITN_SPOKEN_PLUS_PHONE_OUTPUT_RE = re.compile(
    r"\b((?:call|phone|tel|mobile|hotline)\s+)plus\s+"
    r"((?:zero|oh|o|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:\s+(?:zero|oh|o|one|two|three|four|five|six|seven|eight|nine)){2,})\b",
    re.IGNORECASE,
)

_EN_ITN_AREA_CODE_PHONE_OUTPUT_RE = re.compile(
    r"\b((?:call|phone|tel|mobile|hotline)\s+)"
    r"(?:(?:\+(\d{1,3})|plus\s+(zero|oh|o|one|two|three|four|five|six|seven|eight|nine))\s+)?"
    r"area\s+code\s+"
    r"(\d{3})(\d{3})(\d{4})(?=\b)",
    re.IGNORECASE,
)

_EN_ITN_KELVIN_OUTPUT_RE = re.compile(r"\b(-?\d+(?:\.\d+)?)\s+kelvin\b", re.IGNORECASE)

_EN_ITN_PERCENT_POINT_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+percentage\s+points?\b",
    re.IGNORECASE,
)

_EN_ITN_SCIENTIFIC_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+times\s+ten\s+to\s+the\s+"
    rf"(?:(minus|negative|plus)\s+)?({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_COORDINATE_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+degrees?\s+(north|south|east|west)\b",
    re.IGNORECASE,
)

_EN_ITN_SEPARATED_DATE_RE = re.compile(
    rf"\b({_EN_ITN_INTEGER_PHRASE})\s+(dash|hyphen|slash)\s+"
    rf"({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+\2\s+({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_MONTH_NAME_DATE_RE = re.compile(
    rf"\b({_EN_ITN_MONTH_NAME})\s+(?:the\s+)?({_EN_ITN_ORDINAL_PHRASE}|{_EN_ITN_INTEGER_PHRASE_NO_AND})(?:,)?\s+"
    rf"({_EN_ITN_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_DAY_OF_MONTH_DATE_RE = re.compile(
    rf"\b(?:the\s+)?({_EN_ITN_ORDINAL_PHRASE}|{_EN_ITN_INTEGER_PHRASE_NO_AND})\s+of\s+"
    rf"({_EN_ITN_MONTH_NAME})\s+({_EN_ITN_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_TIMEZONE_RE = re.compile(
    rf"\b(UTC|GMT)\s+(plus|minus)\s+({_EN_ITN_INTEGER_PHRASE_NO_AND})(?:\s+({_EN_ITN_INTEGER_PHRASE_NO_AND}))?\b",
    re.IGNORECASE,
)

_EN_ITN_LITER_RE = re.compile(rf"\b({_EN_ITN_NUMBER_PHRASE})\s+liters?\b", re.IGNORECASE)

_EN_ITN_LITER_PER_MINUTE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+liters?\s+per\s+minutes?\b",
    re.IGNORECASE,
)

_EN_ITN_MILLISECOND_RE = re.compile(rf"\b({_EN_ITN_NUMBER_PHRASE})\s+milliseconds?\b", re.IGNORECASE)

_EN_ITN_ACCELERATION_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+meters?\s+per\s+second\s+squared\b",
    re.IGNORECASE,
)

_EN_ITN_MPS_SQUARED_OUTPUT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s+m/s\s+squared\b", re.IGNORECASE)

_EN_ITN_REVOLUTIONS_PER_MINUTE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+revolutions?\s+per\s+minutes?\b",
    re.IGNORECASE,
)

_EN_ITN_DIMENSION_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+by\s+({_EN_ITN_NUMBER_PHRASE})"
    r"(?:\s+(centimeters?|millimeters?|kilometers?|meters?|inches?|feet|pixels?|cm|mm|km|m|in|ft|px))?\b",
    re.IGNORECASE,
)

_EN_ITN_BINARY_BYTE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(gibibytes?|mebibytes?|kibibytes?)\b",
    re.IGNORECASE,
)

_EN_ITN_DATA_BYTE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(bytes?|kilobytes?|megabytes?|gigabytes?|terabytes?)\b",
    re.IGNORECASE,
)

_EN_ITN_POWER_UNIT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(square|cubic)\s+"
    r"(meters?|centimeters?|millimeters?|kilometers?|yards?)\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXT_NUMBER_RE = re.compile(
    rf"\b(chapters?|pages?|sections?|figures?|figs?|equations?|eqs?|episodes?|items?|numbers?)\s+({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_MONEY_WITH_SUBUNITS_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(dollars?|euros?|pounds?)\s+(?:and\s+)?"
    rf"({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+(cents?|pence)\b",
    re.IGNORECASE,
)

_EN_ITN_MONEY_CODE_SUFFIX_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(u\s*s\s*d|e\s*u\s*r|g\s*b\s*p|c\s*n\s*y|r\s*m\s*b|j\s*p\s*y|h\s*k\s*d|"
    r"usd|eur|gbp|cny|rmb|jpy|hkd)\b",
    re.IGNORECASE,
)

_EN_ITN_SYMBOL_MONEY_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+to\s+([$€£¥])\s*({_EN_ITN_NUMBER_PHRASE})(?!\w)",
    re.IGNORECASE,
)

_EN_ITN_UNIT_MONEY_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+to\s+({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(dollars?|euros?|pounds?|yen)\b",
    re.IGNORECASE,
)

_EN_ITN_MONEY_WHOLE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(dollars?|euros?|pounds?|yen)\b",
    re.IGNORECASE,
)

_EN_ITN_PERCENT_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+to\s+({_EN_ITN_NUMBER_PHRASE})(?:\s*%|\s+percent)(?!\w)",
    re.IGNORECASE,
)

_EN_ITN_UNIT_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+to\s+({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(kilograms?|grams?|milligrams?|kilometers?|meters?|centimeters?|millimeters?|"
    r"liters?|milliliters?|hours?|minutes?|seconds?|kg|mg|g|km|cm|mm|m|l|ml|h|min|s|ms)\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXTUAL_RATIO_RE = re.compile(
    rf"\b((?:ratio(?:\s+(?:is|of))?|score(?:\s+(?:is|was))?)\s+)"
    rf"({_EN_ITN_INTEGER_PHRASE})\s+to\s+({_EN_ITN_INTEGER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXTUAL_RANGE_RE = re.compile(
    rf"\b({_EN_ITN_INTEGER_PHRASE})\s+to\s+({_EN_ITN_INTEGER_PHRASE})\s+"
    r"(days?|weeks?|months?|years?|hours?|minutes?|seconds?|items?|people|pages?|times?|"
    r"meters?|kilometers?|centimeters?|millimeters?|grams?|kilograms?|liters?|dollars?|euros?|"
    r"pounds?|percent)\b",
    re.IGNORECASE,
)

_EN_ITN_FLOOR_NUMBER_RE = re.compile(
    rf"\b((?:floor|level)\s+)({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_FORMULA_EQUALS_RE = re.compile(
    rf"(\d+(?:\.\d+)?\s*(?:[+*/×÷-])\s*\d+(?:\.\d+)?)\s+equals\s+({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_WORD_OPERATOR_FORMULA_RE = re.compile(
    rf"\b({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+(plus|minus|times|divided by|divided)\s+"
    rf"({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+equals\s+({_EN_ITN_INTEGER_PHRASE_NO_AND})\b",
    re.IGNORECASE,
)

_EN_ITN_MULTIPLIER_RE = re.compile(
    rf"\b({_EN_ITN_INTEGER_PHRASE_NO_AND})\s+x"
    r"(?=\s+(?:growth|return|speed|zoom|increase|faster|multiplier))",
    re.IGNORECASE,
)

_EN_ITN_CONTEXTUAL_MULTIPLIER_RE = re.compile(
    rf"\b((?:growth|return|speed|zoom|increase|multiplier)\s+(?:is\s+)?)"
    rf"({_EN_ITN_NUMBER_PHRASE})\s+x\b",
    re.IGNORECASE,
)

_EN_ITN_COMPARISON_RE = re.compile(
    rf"\b([A-Za-z][A-Za-z0-9_]{{0,2}}|score|level|value|rate|temperature|temp|count|amount)\s+"
    r"(greater than or equal to|less than or equal to|not equal to|approximately equal to|greater than|less than|equals?|is equal to)\s+"
    rf"({_EN_ITN_NUMBER_PHRASE})\b",
    re.IGNORECASE,
)

_EN_ITN_CONTEXT_ABBREVIATED_NUMBER_RE = re.compile(
    rf"\b((?:users?|views?|followers?|downloads?|visits?|records?|rows?|items?|sales|"
    rf"revenue|profit|income|earnings|valuation|budget|market\s+cap)\s+)"
    rf"({_EN_ITN_NUMBER_PHRASE})\s+([kmb])\b",
    re.IGNORECASE,
)

_EN_ITN_BASIS_POINT_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+basis\s+points?\b",
    re.IGNORECASE,
)

_EN_ITN_SCIENCE_RATIO_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(millimoles?|moles?|micrograms?|nanograms?|milligrams?|grams?|international\s+units?|units?|"
    r"mmol|mol|ug|µg|μg|mcg|ng|mg|g|iu|u)\s+per\s+"
    r"(liters?|deciliters?|kilograms?|milliliters?|microliters?|l|dl|kg|ml|ul|µl|μl)\b",
    re.IGNORECASE,
)

_EN_ITN_MICRO_SIMPLE_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(micrograms?|nanograms?|microliters?)\b",
    re.IGNORECASE,
)

_EN_ITN_ENGINEERING_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(decibels?|decibel\s+milliwatts?|a\s+weighted\s+decibels?|watts?\s+per\s+square\s+meter|"
    r"newton\s+meters?|newtons?|milliampere\s+hours?)\b",
    re.IGNORECASE,
)

_EN_ITN_ELECTRICAL_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+"
    r"(megaohms?|kiloohms?|ohms?|kilovolts?|millivolts?|milliamperes?|amperes?|"
    r"milliwatts?|watts?|microfarads?|nanofarads?|picofarads?)\b",
    re.IGNORECASE,
)

_EN_ITN_PH_OUTPUT_RE = re.compile(r"\bp\s+h\b", re.IGNORECASE)

_EN_ITN_MERCURY_PRESSURE_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(?:millimeters?|mm)\s+(?:of\s+)?mercury\b",
    re.IGNORECASE,
)

_EN_ITN_KILOPASCAL_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+kilopascals?\b",
    re.IGNORECASE,
)

_EN_ITN_PASCAL_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+(pascals?|megapascals?)\b",
    re.IGNORECASE,
)

_EN_ITN_PARTS_PER_OUTPUT_RE = re.compile(
    rf"\b({_EN_ITN_NUMBER_PHRASE})\s+parts?\s+per\s+(million|billion)\b",
    re.IGNORECASE,
)

_EN_ITN_INTEGER_WORD_VALUES_FULL = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

_EN_ITN_INTEGER_SCALE_VALUES = {"hundred": 100, "thousand": 1000, "million": 1000000}

_EN_ITN_UNIT_CASE_OUTPUT_REPLACEMENTS = (
    (re.compile(r"\bhk\$(\d+(?:\.\d+)?)", re.IGNORECASE), r"HK$\1"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+ω\b"), r"\1 Ω"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+mω\b"), r"\1 MΩ"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+kω\b"), r"\1 kΩ"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+uf\b"), r"\1 µF"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+μf\b"), r"\1 µF"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+µf\b"), r"\1 µF"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+nf\b"), r"\1 nF"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+pf\b"), r"\1 pF"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+kv\b"), r"\1 kV"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+mv\b"), r"\1 mV"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+mw\b"), r"\1 mW"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+a\b"), r"\1 A"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+w\b"), r"\1 W"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+bps?\b"), r"\1 bps"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+w/m²\b"), r"\1 W/m²"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+n[·.]?m\b"), r"\1 N·m"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+mah\b"), r"\1 mAh"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+dba\b"), r"\1 dBA"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+dbm\b"), r"\1 dBm"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+db\b"), r"\1 dB"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+[uµμ]g/ml\b"), r"\1 µg/mL"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+ng/ml\b"), r"\1 ng/mL"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+iu/l\b"), r"\1 IU/L"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+u/l\b"), r"\1 U/L"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+[uµμ]l\b"), r"\1 µL"),
    (re.compile(r"(\d+(?:\.\d+)?)\s+[uµμ]g\b"), r"\1 µg"),
    (re.compile(r"(\d+(?:\.\d+)?) mbps\b"), r"\1 Mbps"),
    (re.compile(r"(\d+(?:\.\d+)?) kbps\b"), r"\1 kbps"),
    (re.compile(r"(\d+(?:\.\d+)?) mb\b"), r"\1 MB"),
    (re.compile(r"(\d+(?:\.\d+)?) kb\b"), r"\1 KB"),
    (re.compile(r"(\d+(?:\.\d+)?) gb\b"), r"\1 GB"),
    (re.compile(r"(\d+(?:\.\d+)?) tb\b"), r"\1 TB"),
    (re.compile(r"(\d+(?:\.\d+)?) ghz\b"), r"\1 GHz"),
    (re.compile(r"(\d+(?:\.\d+)?) mhz\b"), r"\1 MHz"),
    (re.compile(r"(\d+(?:\.\d+)?) khz\b"), r"\1 kHz"),
    (re.compile(r"(\d+(?:\.\d+)?) hz\b"), r"\1 Hz"),
    (re.compile(r"(\d+(?:\.\d+)?) kwh\b"), r"\1 kWh"),
    (re.compile(r"(\d+(?:\.\d+)?) kw\b"), r"\1 kW"),
    (re.compile(r"(\d+(?:\.\d+)?) mpa\b"), r"\1 MPa"),
    (re.compile(r"(\d+(?:\.\d+)?) pa\b"), r"\1 Pa"),
    (re.compile(r"(\d+(?:\.\d+)?) mmhg\b"), r"\1 mmHg"),
    (re.compile(r"(\d+(?:\.\d+)?) kpa\b"), r"\1 kPa"),
    (re.compile(r"(\d+(?:\.\d+)?) ml\b"), r"\1 mL"),
    (re.compile(r"(\d+(?:\.\d+)?) ma\b"), r"\1 mA"),
    (re.compile(r"(\d+(?:\.\d+)?) rpm\b"), r"\1 rpm"),
    (re.compile(r"(\d+(?:\.\d+)?) v\b"), r"\1 V"),
)

def _en_spoken_digit_to_ascii(token: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "o": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    return digit_values[token.lower()]

def _prepare_en_itn_input(text: str) -> str:
    prepared = normalize_spoken_money_with_subunits(
        remove_asr_fillers(text),
        parse_number=_parse_en_number_phrase,
        parse_integer=_parse_en_integer_phrase,
    )
    prepared = _normalize_en_itn_technical_tokens(prepared)
    prepared = _normalize_en_itn_shortcuts(prepared)
    prepared = normalize_data_units(prepared, parse_number=_parse_en_number_phrase)
    prepared = normalize_spoken_digit_multipliers(prepared, parse_number=_parse_en_number_phrase)
    prepared = normalize_spoken_dozens(prepared, parse_integer=_parse_en_integer_phrase)
    prepared = normalize_spoken_temperature_ranges(prepared, parse_number=_parse_en_number_phrase)
    prepared = _normalize_en_itn_file_tokens(prepared)
    prepared = _normalize_en_itn_context_decimal_versions(prepared)
    prepared = _normalize_en_itn_social_tokens(prepared)
    prepared = _normalize_en_itn_parameter_tokens(prepared)
    prepared = normalize_spoken_punctuation(prepared)
    prepared = _normalize_en_itn_zip_codes(prepared)
    prepared = _normalize_en_itn_room_codes(prepared)
    prepared = _normalize_en_itn_floor_numbers(prepared)
    prepared = _normalize_en_itn_context_year_codes(prepared)
    prepared = _normalize_en_itn_context_codes(prepared)
    prepared = _normalize_en_itn_extensions(prepared)
    prepared = _normalize_en_itn_last_four_digits(prepared)
    prepared = _normalize_en_itn_spoken_toll_free_phone_numbers(prepared)
    prepared = _normalize_en_itn_spoken_phone_numbers(prepared)
    prepared = _normalize_en_itn_quarters(prepared)
    prepared = _normalize_en_itn_fiscal_years(prepared)
    prepared = _normalize_en_itn_separated_dates(prepared)
    prepared = _normalize_en_itn_day_of_month_dates(prepared)
    prepared = normalize_spoken_month_name_dates(
        prepared,
        parse_integer=_parse_en_integer_phrase,
        parse_year=_parse_en_year_phrase,
    )
    prepared = normalize_spoken_dotted_dates(
        prepared,
        parse_integer=_parse_en_integer_phrase,
        parse_year=_parse_en_year_phrase,
    )
    prepared = _normalize_en_itn_month_name_dates(prepared)
    prepared = normalize_spoken_numeric_dates(
        prepared,
        parse_integer=_parse_en_integer_phrase,
        parse_year=_parse_en_year_phrase,
    )
    prepared = _normalize_en_itn_timezones(prepared)
    prepared = normalize_colloquial_time_prefixes(prepared)
    prepared = normalize_named_times(prepared)
    prepared = normalize_weekday_ranges(prepared)
    prepared = _normalize_en_itn_relative_clock_times(prepared)
    prepared = _normalize_en_itn_clock_time_ranges(prepared)
    prepared = _normalize_en_itn_clock_times(prepared)
    prepared = _normalize_en_itn_daypart_clock_times(prepared)
    prepared = _normalize_en_itn_time_oh(prepared)
    prepared = normalize_half_quantities(prepared, parse_integer=_parse_en_integer_phrase)
    prepared = normalize_spoken_ratings(prepared, parse_number=_parse_en_number_phrase)
    prepared = normalize_buy_get_promotions(prepared, parse_number=_parse_en_number_phrase)
    prepared = normalize_spoken_ordinal_ranges(prepared, parse_ordinal=_parse_en_ordinal_phrase)
    prepared = normalize_spoken_ordinals(prepared, parse_ordinal=_parse_en_ordinal_phrase)
    prepared = _EN_ITN_KILOWATT_HOURS_RE.sub("kilo watt hours", prepared)
    return _EN_ITN_MILLIAMPERES_RE.sub("milli amperes", prepared)

def _normalize_en_itn_separated_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year = _parse_en_year_phrase(match.group(1))
        month = _parse_en_integer_phrase(match.group(3))
        day = _parse_en_integer_phrase(match.group(4))
        if year is None or month is None or day is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        separator = "/" if match.group(2).lower() == "slash" else "-"
        return f"{year:04d}{separator}{month:02d}{separator}{day:02d}"

    return _EN_ITN_SEPARATED_DATE_RE.sub(replace, text)

def _normalize_en_itn_month_name_dates(text: str) -> str:
    month_values = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12,
    }

    def replace(match: re.Match[str]) -> str:
        month = month_values[match.group(1).lower().rstrip(".")]
        day = _parse_en_ordinal_phrase(match.group(2))
        if day is None:
            day = _parse_en_integer_phrase(match.group(2))
        year = _parse_en_year_phrase(match.group(3))
        if day is None or year is None or not 1 <= day <= 31:
            return match.group(0)
        return f"{year:04d}-{month:02d}-{day:02d}"

    return _EN_ITN_MONTH_NAME_DATE_RE.sub(replace, text)

def _normalize_en_itn_day_of_month_dates(text: str) -> str:
    month_values = {
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12,
    }

    def replace(match: re.Match[str]) -> str:
        day = _parse_en_ordinal_phrase(match.group(1))
        if day is None:
            day = _parse_en_integer_phrase(match.group(1))
        year = _parse_en_year_phrase(match.group(3))
        month = month_values[match.group(2).lower().rstrip(".")]
        if day is None or year is None or not 1 <= day <= 31:
            return match.group(0)
        return f"{year:04d}-{month:02d}-{day:02d}"

    return _EN_ITN_DAY_OF_MONTH_DATE_RE.sub(replace, text)

def _normalize_en_itn_timezones(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_en_integer_phrase(match.group(3))
        minute = _parse_en_integer_phrase(match.group(4)) if match.group(4) else None
        if hour is None or not 0 <= hour <= 14 or (minute is not None and not 0 <= minute <= 59):
            return match.group(0)
        suffix = f":{minute:02d}" if minute is not None else ""
        sign = "+" if match.group(2).lower() == "plus" else "-"
        return f"{match.group(1).upper()}{sign}{hour}{suffix}"

    return _EN_ITN_TIMEZONE_RE.sub(replace, text)

def _normalize_en_itn_time_oh(text: str) -> str:
    prepared = _EN_ITN_LEADING_ZERO_TIME_OH_RE.sub(r"\1 o \2", text)
    return _EN_ITN_TIME_OH_RE.sub(r"\1 o \2", prepared)

def _normalize_en_itn_clock_times(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_en_integer_phrase(match.group(2))
        minute = _parse_en_clock_minute_phrase(match.group(3))
        if hour is None or minute is None or not 0 <= hour <= 23 or not 0 <= minute <= 59:
            return match.group(0)
        return f"{match.group(1)}{hour:02d}:{minute:02d}"

    return _EN_ITN_CLOCK_TIME_RE.sub(replace, text)

def _normalize_en_itn_relative_clock_times(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_en_integer_phrase(match.group(5))
        if hour is None or not 1 <= hour <= 23:
            return match.group(0)
        if match.group(4):
            minute = 30
        elif match.group(3).lower() == "past":
            minute = 15
        else:
            minute = 45
            hour = hour - 1 if hour > 1 else 12
        return f"{match.group(1)}{hour:02d}:{minute:02d}"

    return _EN_ITN_RELATIVE_CLOCK_TIME_RE.sub(replace, text)

def _normalize_en_itn_daypart_clock_times(text: str) -> str:
    suffixes = {"morning": "AM", "afternoon": "PM", "evening": "PM"}

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {suffixes[match.group(2).lower()]}"

    return _EN_ITN_DAYPART_CLOCK_OUTPUT_RE.sub(replace, text)

def _normalize_en_itn_clock_time_ranges(text: str) -> str:
    def normalize_range(
        fallback: str,
        start_hour_text: str,
        start_minute_text: str | None,
        end_hour_text: str,
        end_minute_text: str,
        prefix: str = "",
    ) -> str:
        start_hour = _parse_en_integer_phrase(start_hour_text)
        start_minute = _parse_en_clock_minute_phrase(start_minute_text) if start_minute_text else 0
        end_hour = _parse_en_integer_phrase(end_hour_text)
        end_minute = _parse_en_clock_minute_phrase(end_minute_text)
        if (
            start_hour is None
            or start_minute is None
            or end_hour is None
            or end_minute is None
            or not 0 <= start_hour <= 23
            or not 0 <= start_minute <= 59
            or not 0 <= end_hour <= 23
            or not 0 <= end_minute <= 59
        ):
            return fallback
        if 1 <= start_hour <= 12 and 1 <= end_hour <= 12 and end_hour <= start_hour:
            end_hour += 12
        return f"{prefix}{start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

    prepared = _EN_ITN_CLOCK_TIME_RANGE_RE.sub(
        lambda match: normalize_range(
            match.group(0),
            match.group(2),
            match.group(3),
            match.group(4),
            match.group(5),
            match.group(1),
        ),
        text,
    )
    prepared = _EN_ITN_CONTEXT_HOUR_ONLY_CLOCK_TIME_RANGE_RE.sub(
        lambda match: normalize_range(match.group(0), match.group(2), None, match.group(3), "zero", match.group(1)),
        prepared,
    )
    return _EN_ITN_BARE_CLOCK_TIME_RANGE_RE.sub(
        lambda match: normalize_range(match.group(0), match.group(1), match.group(2), match.group(3), match.group(4)),
        prepared,
    )

def _parse_en_clock_minute_phrase(text: str) -> int | None:
    raw = text.strip().lower()
    if raw.startswith(("oh ", "o ", "zero ")):
        digit = _restore_en_spoken_electronic_token(raw.split(maxsplit=1)[1])
        return int(digit) if digit.isdigit() else None
    return _parse_en_integer_phrase(raw)

def _normalize_en_itn_file_tokens(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        if _EN_ITN_FILE_DATA_QUANTITY_PREFIX_RE.search(match.group(2)):
            return match.group(0)
        return f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2))}"

    return _EN_ITN_FILE_CONTEXT_RE.sub(replace, text)

def _normalize_en_itn_technical_tokens(text: str) -> str:
    prepared = _EN_ITN_ISO_DATETIME_RE.sub(
        lambda match: _restore_en_spoken_electronic_token(match.group(1), uppercase_letters=True),
        text,
    )
    prepared = _EN_ITN_SPACE_DATETIME_RE.sub(
        lambda match: (
            f"{_restore_en_spoken_electronic_token(match.group(1), uppercase_letters=True)} "
            f"{_restore_en_spoken_electronic_token(match.group(2), uppercase_letters=True)}"
        ),
        prepared,
    )
    prepared = _EN_ITN_HTTP_STATUS_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2))}",
        prepared,
    )
    prepared = _EN_ITN_PORT_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2))}",
        prepared,
    )
    prepared = _EN_ITN_URL_RE.sub(
        lambda match: _restore_en_spoken_electronic_token(match.group(1)).lower(),
        prepared,
    )
    prepared = _EN_ITN_SEMVER_RE.sub(_normalize_en_itn_semver_match, prepared)
    prepared = _EN_ITN_IPV4_PORT_RE.sub(
        lambda match: _restore_en_spoken_electronic_token(match.group(1)),
        prepared,
    )
    prepared = _EN_ITN_IPV6_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2)).lower()}",
        prepared,
    )
    prepared = _EN_ITN_ISBN_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2), uppercase_letters=True)}",
        prepared,
    )
    prepared = _EN_ITN_DOI_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2)).lower()}",
        prepared,
    )
    prepared = _EN_ITN_MAC_ADDRESS_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2), uppercase_letters=True)}",
        prepared,
    )
    prepared = _EN_ITN_UUID_RE.sub(
        lambda match: f"{match.group(1)}{_restore_en_spoken_electronic_token(match.group(2)).lower()}",
        prepared,
    )
    return _EN_ITN_HEX_COLOR_RE.sub(
        lambda match: f"{match.group(1)}#{_restore_en_spoken_electronic_token(match.group(2), uppercase_letters=True)}",
        prepared,
    )

def _normalize_en_itn_shortcuts(text: str) -> str:
    return _EN_ITN_SHORTCUT_RE.sub(lambda match: _restore_en_shortcut(match.group(1)), text)

def _restore_en_shortcut(shortcut: str) -> str:
    return "+".join(_restore_en_shortcut_token(token) for token in re.split(r"\s+plus\s+", shortcut, flags=re.IGNORECASE))

def _restore_en_shortcut_token(token: str) -> str:
    normalized = re.sub(r"\s+", " ", token.strip().lower())
    modifier_tokens = {
        "control": "Ctrl",
        "ctrl": "Ctrl",
        "command": "Cmd",
        "cmd": "Cmd",
        "shift": "Shift",
        "alt": "Alt",
        "option": "Option",
        "meta": "Meta",
        "windows": "Win",
        "win": "Win",
        "function": "Fn",
        "fn": "Fn",
        "escape": "Esc",
        "esc": "Esc",
        "tab": "Tab",
        "enter": "Enter",
        "return": "Return",
        "space": "Space",
        "delete": "Delete",
        "del": "Delete",
        "backspace": "Backspace",
    }
    if normalized in modifier_tokens:
        return modifier_tokens[normalized]
    if normalized.startswith("f "):
        digits = _restore_en_spoken_electronic_token(normalized[2:])
        return f"F{digits}" if digits.isdigit() else token
    if len(token.strip()) == 1 and token.strip().isalpha():
        return token.strip().upper()
    return _restore_en_spoken_electronic_token(token)

def _normalize_en_itn_semver_match(match: re.Match[str]) -> str:
    raw = match.group(2)
    if not re.search(r"\b(?:dash|hyphen|plus)\b", raw, re.IGNORECASE):
        return match.group(0)
    return f"{match.group(1)}{_restore_en_spoken_electronic_token(raw).lower()}"

def _normalize_en_itn_context_decimal_versions(text: str) -> str:
    token_values = {
        "zero": "0",
        "oh": "0",
        "o": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
    }

    def parse_component(raw: str, *, first: bool = False) -> str | None:
        normalized = raw.lower().strip()
        if first:
            year = _parse_en_year_phrase(normalized)
            if year is not None:
                return str(year)
            integer = _parse_en_integer_phrase(normalized)
            return str(integer) if integer is not None else None

        parts = []
        for token in normalized.split():
            if token.isdigit():
                parts.append(token)
            elif token in token_values:
                parts.append(token_values[token])
            else:
                return None
        return "".join(parts)

    def replace(match: re.Match[str]) -> str:
        raw_parts = re.split(r"\s+point\s+", match.group(2), flags=re.IGNORECASE)
        parts = [parse_component(raw_parts[0], first=True)]
        parts.extend(parse_component(raw_part) for raw_part in raw_parts[1:])
        if any(part is None for part in parts):
            return match.group(0)
        return f"{match.group(1)}{'.'.join(part for part in parts if part is not None)}"

    return _EN_ITN_CONTEXT_DECIMAL_VERSION_RE.sub(replace, text)

def _normalize_en_itn_social_tokens(text: str) -> str:
    prepared = _EN_ITN_SOCIAL_HANDLE_RE.sub(
        lambda match: f"{match.group(1)}@{_restore_en_spoken_electronic_token(match.group(2))}",
        text,
    )
    return _EN_ITN_SOCIAL_HASHTAG_RE.sub(
        lambda match: f"{match.group(1)}#{_restore_en_spoken_electronic_token(match.group(2), uppercase_letters=True)}",
        prepared,
    )

def _normalize_en_itn_parameter_tokens(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _restore_en_spoken_electronic_token(match.group(3))
        return f"{match.group(1)}{match.group(2)}={value}"

    return _EN_ITN_PARAMETER_RE.sub(replace, text)

def _restore_en_spoken_electronic_token(text: str, *, uppercase_letters: bool = False) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    prepared_text = re.sub(r"\bquestion\s+mark\b", "question_mark", text, flags=re.IGNORECASE)
    prepared_text = re.sub(r"\bequal\s+sign\b", "equal_sign", prepared_text, flags=re.IGNORECASE)
    symbol_values = {
        "slash": "/",
        "backslash": "\\",
        "dot": ".",
        "point": ".",
        "underscore": "_",
        "dash": "-",
        "hyphen": "-",
        "colon": ":",
        "tilde": "~",
        "question_mark": "?",
        "equals": "=",
        "equal": "=",
        "equal_sign": "=",
        "ampersand": "&",
        "hash": "#",
        "plus": "+",
    }
    output: list[str] = []
    extension_mode = False
    for token in prepared_text.split():
        normalized = token.lower()
        symbol = symbol_values.get(normalized)
        if symbol is not None:
            output.append(symbol)
            extension_mode = symbol == "."
            continue
        digit = digit_values.get(normalized)
        if digit is not None:
            output.append(digit)
            extension_mode = False
            continue
        if len(token) == 1 and token.isalpha():
            if extension_mode:
                output.append(token.lower())
            elif uppercase_letters:
                output.append(token.upper())
            else:
                output.append(token)
            continue
        output.append(token.upper() if uppercase_letters and token.isalpha() else token.lower())
        extension_mode = False
    return "".join(output)

def _normalize_en_itn_zip_codes(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def replace(match: re.Match[str]) -> str:
        parts = []
        for token in match.group(2).split():
            normalized = token.lower()
            if normalized in {"dash", "hyphen"}:
                parts.append("-")
            elif normalized in digit_values:
                parts.append(digit_values[normalized])
        return f"{match.group(1)}{''.join(parts)}"

    return _EN_ITN_ZIP_CODE_RE.sub(replace, text)

def _normalize_en_itn_room_codes(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "o": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    teen_values = {
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
        "thirteen": "13",
        "fourteen": "14",
        "fifteen": "15",
        "sixteen": "16",
        "seventeen": "17",
        "eighteen": "18",
        "nineteen": "19",
    }

    def replace(match: re.Match[str]) -> str:
        code_parts = []
        has_digit = False
        for token in match.group(2).split():
            normalized = token.lower()
            if normalized in {"dash", "hyphen"}:
                code_parts.append("-")
            elif normalized in digit_values:
                code_parts.append(digit_values[normalized])
                has_digit = True
            elif normalized in teen_values:
                code_parts.append(teen_values[normalized])
                has_digit = True
            elif len(token) == 1 and token.isalpha():
                code_parts.append(token.upper())
        if not has_digit:
            return match.group(0)
        return f"{match.group(1)}{''.join(code_parts)}"

    return _EN_ITN_ROOM_CODE_RE.sub(replace, text)

def _normalize_en_itn_context_year_codes(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def replace(match: re.Match[str]) -> str:
        letters = "".join(token.upper() for token in match.group(2).split())
        year = _parse_en_year_phrase(match.group(3))
        if year is None:
            return match.group(0)
        suffix = "".join(digit_values[token.lower()] for token in match.group(4).split())
        return f"{match.group(1)}{letters}-{year:04d}-{suffix}"

    return _EN_ITN_CONTEXT_YEAR_CODE_RE.sub(replace, text)

def _normalize_en_itn_floor_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_integer_phrase(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}"

    return _EN_ITN_FLOOR_NUMBER_RE.sub(replace, text)

def _normalize_en_itn_context_codes(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def replace(match: re.Match[str]) -> str:
        code_parts = []
        has_digit = False
        for token in match.group(2).split():
            normalized = token.lower()
            if normalized in {"dash", "hyphen"}:
                code_parts.append("-")
            elif normalized in digit_values:
                code_parts.append(digit_values[normalized])
                has_digit = True
            elif len(token) == 1 and token.isalpha():
                code_parts.append(token.upper())
        if not has_digit:
            return match.group(0)
        return f"{match.group(1)}{''.join(code_parts)}"

    return _EN_ITN_CONTEXT_CODE_RE.sub(replace, text)

def _normalize_en_itn_extensions(text: str) -> str:
    digit_values = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    return _EN_ITN_EXTENSION_RE.sub(
        lambda match: f"ext. {''.join(digit_values[token.lower()] for token in match.group(1).split())}",
        text,
    )

def _normalize_en_itn_last_four_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(_en_spoken_digit_to_ascii(match.group(index)) for index in range(2, 6))
        return f"{match.group(1)}{digits}"

    return _EN_ITN_LAST_FOUR_RE.sub(replace, text)

def _normalize_en_itn_spoken_phone_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(_en_spoken_digit_to_ascii(match.group(index)) for index in range(2, 12))
        return f"{match.group(1)}{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return _EN_ITN_SPOKEN_PHONE_NUMBER_RE.sub(replace, text)

def _normalize_en_itn_spoken_toll_free_phone_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        country = "1-" if match.group(2) else ""
        digits = "".join(_en_spoken_digit_to_ascii(match.group(index)) for index in range(3, 10))
        return f"{match.group(1)}{country}800-{digits[:3]}-{digits[3:]}"

    return _EN_ITN_SPOKEN_TOLL_FREE_PHONE_RE.sub(replace, text)

def _normalize_en_itn_quarters(text: str) -> str:
    quarter_values = {"one": 1, "two": 2, "three": 3, "four": 4, "1": 1, "2": 2, "3": 3, "4": 4}

    def replace(match: re.Match[str]) -> str:
        quarter = quarter_values[match.group(1).lower()]
        year = _parse_en_year_phrase(match.group(2))
        if year is None:
            return match.group(0)
        return f"Q{quarter} {year}"

    return _EN_ITN_QUARTER_RE.sub(replace, text)

def _normalize_en_itn_fiscal_years(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year = _parse_en_year_phrase(match.group(1))
        if year is None:
            return match.group(0)
        return f"FY{year}"

    return _EN_ITN_FISCAL_YEAR_RE.sub(replace, text)

def _restore_en_itn_layout_commands(text: str) -> str:
    heading_levels = {"one": 1, "two": 2, "three": 3, "1": 1, "2": 2, "3": 3}
    restored = _EN_ITN_HEADING_COMMAND_RE.sub(lambda match: f" __HEADING_{heading_levels[match.group(1).lower()]}__ ", text)
    restored = _EN_ITN_BULLET_COMMAND_RE.sub(" __BULLET__ ", restored)
    restored = _EN_ITN_TAB_COMMAND_RE.sub("\t", restored)
    restored = _EN_ITN_BLANK_LINE_COMMAND_RE.sub("\n\n", restored)
    restored = _EN_ITN_LINE_BREAK_COMMAND_RE.sub("\n", restored)
    restored = _EN_ITN_ORDERED_ITEM_COMMAND_RE.sub(_restore_en_itn_ordered_item_match, restored)
    restored = re.sub(r"[ \t]*__HEADING_([123])__[ \t]*", lambda match: f"{'#' * int(match.group(1))} ", restored)
    restored = re.sub(r"[ \t]*__BULLET__[ \t]*", "- ", restored)
    restored = _EN_ITN_BOLD_SPAN_RE.sub(lambda match: f"**{match.group(1).strip()}**", restored)
    restored = _EN_ITN_CODE_SPAN_RE.sub(lambda match: f"`{match.group(1).strip()}`", restored)
    restored = re.sub(r"[ ]*\t[ ]*", "\t", restored)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", restored)

def _restore_en_itn_ordered_item_match(match: re.Match[str]) -> str:
    number_values = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    raw_number = match.group(2).lower()
    value = int(raw_number) if raw_number.isdigit() else number_values[raw_number]
    return f"{match.group(1)}{value}. "

def _restore_en_itn_format_symbols(text: str) -> str:
    symbol_map = {
        "forward slash": "/",
        "slash": "/",
        "dash": "-",
        "hyphen": "-",
        "at sign": "@",
        "hash sign": "#",
        "pound sign": "#",
        "underscore": "_",
        "equal sign": "=",
        "equals sign": "=",
        "plus sign": "+",
        "minus sign": "-",
        "percent sign": "%",
        "asterisk": "*",
        "ampersand": "&",
        "check mark": "✓",
        "checkmark": "✓",
        "cross mark": "×",
        "x mark": "×",
        "open brace": "{",
        "open curly brace": "{",
        "left brace": "{",
        "left curly brace": "{",
        "close brace": "}",
        "close curly brace": "}",
        "right brace": "}",
        "right curly brace": "}",
        "left angle bracket": "<",
        "right angle bracket": ">",
        "backslash": "\\",
        "pipe": "|",
        "vertical bar": "|",
        "tilde": "~",
    }

    def replace(match: re.Match[str]) -> str:
        return f" __FMT_{ord(symbol_map[match.group(1).lower()]):X}__ "

    restored = _EN_ITN_FORMAT_SYMBOL_COMMAND_RE.sub(replace, text)
    if restored == text:
        return text
    return re.sub(r"\s*__FMT_([0-9A-F]+)__([ \t]*)", _restore_itn_format_symbol_match, restored)

def _compact_en_itn_spacing(text: str) -> str:
    compacted = _replace_en_itn_percent_ranges(text)
    compacted = _EN_ITN_SPOKEN_COLON_TIME_OUTPUT_RE.sub(r"\1:\2", compacted)
    compacted = _EN_ITN_EXT_OUTPUT_RE.sub(r"ext. \1", compacted)
    compacted = _EN_ITN_PERCENT_SPACE_RE.sub(r"\1%", compacted)
    compacted = _replace_en_itn_plus_minus(compacted)
    compacted = _EN_ITN_NEGATIVE_CURRENCY_RE.sub(r"-\1\2", compacted)
    compacted = _EN_ITN_NEGATIVE_MEASURE_RE.sub(r"-\1", compacted)
    compacted = _replace_en_itn_money_ranges(compacted)
    compacted = _replace_en_itn_money_code_suffixes(compacted)
    compacted = _replace_en_itn_spoken_money(compacted)
    compacted = compact_currency_per_units(compacted)
    compacted = _replace_en_itn_spoken_negative_temperatures(compacted)
    compacted = _EN_ITN_CELSIUS_OUTPUT_RE.sub(r"\1°C", compacted)
    compacted = _EN_ITN_FAHRENHEIT_OUTPUT_RE.sub(r"\1°F", compacted)
    compacted = _EN_ITN_KELVIN_OUTPUT_RE.sub(r"\1 K", compacted)
    compacted = _EN_ITN_POSITIVE_PERCENT_RE.sub(r"+\1%", compacted)
    compacted = _replace_en_itn_time_seconds(compacted)
    compacted = compact_duration_sequences(compacted)
    compacted = _replace_en_itn_percentage_points(compacted)
    compacted = _replace_en_itn_scientific_notation(compacted)
    compacted = _replace_en_itn_coordinates(compacted)
    compacted = _replace_en_itn_multipliers(compacted)
    compacted = _replace_en_itn_contextual_multipliers(compacted)
    compacted = _replace_en_itn_context_abbreviated_numbers(compacted)
    compacted = _replace_en_itn_unit_ranges(compacted)
    compacted = _replace_en_itn_basis_points(compacted)
    compacted = _replace_en_itn_science_units(compacted)
    compacted = _replace_en_itn_engineering_units(compacted)
    compacted = _replace_en_itn_electrical_units(compacted)
    compacted = _replace_en_itn_motion_and_rate_units(compacted)
    compacted = _replace_en_itn_per_mille(compacted)
    compacted = _EN_ITN_DOTTED_VERSION_SPACE_RE.sub(".", compacted)
    compacted = _restore_en_itn_ftp_urls(compacted)
    compacted = _restore_en_itn_explicit_emails(compacted)
    compacted = _restore_en_itn_spoken_domains(compacted)
    compacted = _replace_en_itn_common_fractions(compacted)
    compacted = compact_ordinal_digit_fractions(compacted, parse_integer=_parse_en_integer_phrase)
    compacted = compact_square_feet(compacted, parse_number=_parse_en_number_phrase)
    compacted = _replace_en_itn_dimensions(compacted)
    compacted = _replace_en_itn_contextual_ratios(compacted)
    compacted = _replace_en_itn_contextual_ranges(compacted)
    compacted = _replace_en_itn_liter_units(compacted)
    compacted = _replace_en_itn_milliseconds(compacted)
    compacted = _replace_en_itn_data_bytes(compacted)
    compacted = _replace_en_itn_binary_bytes(compacted)
    compacted = _replace_en_itn_power_units(compacted)
    compacted = _replace_en_itn_context_numbers(compacted)
    compacted = _replace_en_itn_formula_equals(compacted)
    compacted = _replace_en_itn_word_operator_formulas(compacted)
    compacted = _replace_en_itn_comparisons(compacted)
    compacted = _EN_ITN_FRAMES_PER_SECOND_OUTPUT_RE.sub(r"\1 fps", compacted)
    compacted = _EN_ITN_WEIGHT_POUNDS_OUTPUT_RE.sub(r"\1 \2 lb", compacted)
    compacted = _EN_ITN_INCH_QUOTE_OUTPUT_RE.sub(r"\1 in", compacted)
    compacted = _EN_ITN_AM_PM_OUTPUT_RE.sub(
        lambda match: f"{match.group(1)} {match.group(2).upper()}M",
        compacted,
    )
    compacted = _replace_en_itn_spoken_plus_phone_numbers(compacted)
    compacted = _EN_ITN_PHONE_PLUS_OUTPUT_RE.sub(lambda match: match.group(1) + " +", compacted)
    compacted = _replace_en_itn_area_code_phone_numbers(compacted)
    return _normalize_en_itn_unit_case(compacted)

def _replace_en_itn_time_seconds(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        second = _EN_ITN_INTEGER_WORD_VALUES_FULL[match.group(2).lower()]
        return f"{match.group(1)}:{second:02d}"

    return _EN_ITN_TIME_SECONDS_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_spoken_plus_phone_numbers(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "o": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def replace(match: re.Match[str]) -> str:
        digits = "".join(digit_values[token.lower()] for token in match.group(2).split())
        return f"{match.group(1)}+{digits}"

    return _EN_ITN_SPOKEN_PLUS_PHONE_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_area_code_phone_numbers(text: str) -> str:
    digit_values = {
        "zero": "0",
        "oh": "0",
        "o": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def replace(match: re.Match[str]) -> str:
        raw_country = match.group(2) or match.group(3)
        country = ""
        if raw_country:
            country_digits = digit_values.get(raw_country.lower(), raw_country)
            country = f"+{country_digits} "
        return f"{match.group(1)}{country}{match.group(4)}-{match.group(5)}-{match.group(6)}"

    return _EN_ITN_AREA_CODE_PHONE_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_plus_minus(text: str) -> str:
    unit_symbols = {
        None: "",
        "percent": "%",
        "degree celsius": "°C",
        "degrees celsius": "°C",
        "degree fahrenheit": "°F",
        "degrees fahrenheit": "°F",
        "millimeter": " mm",
        "millimeters": " mm",
        "centimeter": " cm",
        "centimeters": " cm",
        "meter": " m",
        "meters": " m",
        "kilometer": " km",
        "kilometers": " km",
        "gram": " g",
        "grams": " g",
        "kilogram": " kg",
        "kilograms": " kg",
        "mm": " mm",
        "cm": " cm",
        "m": " m",
        "km": " km",
        "g": " g",
        "kg": " kg",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower() if match.group(2) else None
        return f"±{value}{unit_symbols[unit]}"

    compacted = _EN_ITN_PLUS_MINUS_RE.sub(replace, text)
    return _EN_ITN_PLUS_OR_SIGNED_RE.sub(
        lambda match: f"±{match.group(1)}{unit_symbols[match.group(2).lower() if match.group(2) else None]}",
        compacted,
    )

def _replace_en_itn_spoken_money(text: str) -> str:
    currency_symbols = {
        "dollar": "$",
        "dollars": "$",
        "euro": "€",
        "euros": "€",
        "pound": "£",
        "pounds": "£",
        "yen": "¥",
    }

    def replace_with_subunits(match: re.Match[str]) -> str:
        major = _parse_en_number_phrase(match.group(1))
        minor = _parse_en_integer_phrase(match.group(3))
        if major is None or minor is None or not 0 <= minor <= 99:
            return match.group(0)
        symbol = currency_symbols[match.group(2).lower()]
        return f"{symbol}{major}.{minor:02d}"

    def replace_whole(match: re.Match[str]) -> str:
        major = _parse_en_number_phrase(match.group(1))
        if major is None:
            return match.group(0)
        symbol = currency_symbols[match.group(2).lower()]
        return f"{symbol}{major}"

    compacted = _EN_ITN_MONEY_WITH_SUBUNITS_RE.sub(replace_with_subunits, text)
    return _EN_ITN_MONEY_WHOLE_RE.sub(replace_whole, compacted)

def _replace_en_itn_spoken_negative_temperatures(text: str) -> str:
    symbols = {"celsius": "°C", "fahrenheit": "°F"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"-{value}{symbols[match.group(2).lower()]}"

    return _EN_ITN_SPOKEN_NEGATIVE_TEMPERATURE_RE.sub(replace, text)

def _replace_en_itn_money_code_suffixes(text: str) -> str:
    symbols = {
        "usd": "$",
        "eur": "€",
        "gbp": "£",
        "cny": "¥",
        "rmb": "¥",
        "jpy": "¥",
        "hkd": "HK$",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        code = re.sub(r"\s+", "", match.group(2).lower())
        return f"{symbols[code]}{value}"

    return _EN_ITN_MONEY_CODE_SUFFIX_RE.sub(replace, text)

def _replace_en_itn_money_ranges(text: str) -> str:
    symbols = {"dollar": "$", "euro": "€", "pound": "£", "yen": "¥"}

    def replace_symbol(match: re.Match[str]) -> str:
        start = _parse_en_number_phrase(match.group(1))
        end = _parse_en_number_phrase(match.group(3))
        if start is None or end is None:
            return match.group(0)
        return f"{match.group(2)}{start}-{match.group(2)}{end}"

    def replace_unit(match: re.Match[str]) -> str:
        start = _parse_en_number_phrase(match.group(1))
        end = _parse_en_number_phrase(match.group(2))
        if start is None or end is None:
            return match.group(0)
        symbol = symbols[match.group(3).lower().removesuffix("s")]
        return f"{symbol}{start}-{symbol}{end}"

    compacted = _EN_ITN_SYMBOL_MONEY_RANGE_RE.sub(replace_symbol, text)
    return _EN_ITN_UNIT_MONEY_RANGE_RE.sub(replace_unit, compacted)

def _replace_en_itn_percent_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _parse_en_number_phrase(match.group(1))
        end = _parse_en_number_phrase(match.group(2))
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end}%"

    return _EN_ITN_PERCENT_RANGE_RE.sub(replace, text)

def _replace_en_itn_unit_ranges(text: str) -> str:
    unit_symbols = {
        "kilogram": "kg",
        "kg": "kg",
        "gram": "g",
        "g": "g",
        "milligram": "mg",
        "mg": "mg",
        "kilometer": "km",
        "km": "km",
        "meter": "m",
        "m": "m",
        "centimeter": "cm",
        "cm": "cm",
        "millimeter": "mm",
        "mm": "mm",
        "liter": "L",
        "l": "L",
        "milliliter": "mL",
        "ml": "mL",
        "hour": "h",
        "h": "h",
        "minute": "min",
        "min": "min",
        "second": "s",
        "s": "s",
        "ms": "ms",
    }

    def replace(match: re.Match[str]) -> str:
        start = _parse_en_number_phrase(match.group(1))
        end = _parse_en_number_phrase(match.group(2))
        if start is None or end is None:
            return match.group(0)
        unit = unit_symbols[match.group(3).lower().removesuffix("s")]
        return f"{start}-{end} {unit}"

    return _EN_ITN_UNIT_RANGE_RE.sub(replace, text)

def _replace_en_itn_percentage_points(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value} pp"

    return _EN_ITN_PERCENT_POINT_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_scientific_notation(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        mantissa = _parse_en_number_phrase(match.group(1))
        exponent = _parse_en_integer_phrase(match.group(3))
        if mantissa is None or exponent is None:
            return match.group(0)
        sign = "-" if (match.group(2) or "").lower() in {"minus", "negative"} else ""
        return f"{mantissa}e{sign}{exponent}"

    return _EN_ITN_SCIENTIFIC_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_coordinates(text: str) -> str:
    direction_symbols = {"north": "N", "south": "S", "east": "E", "west": "W"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}°{direction_symbols[match.group(2).lower()]}"

    return _EN_ITN_COORDINATE_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_multipliers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_integer_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}x"

    return _EN_ITN_MULTIPLIER_RE.sub(replace, text)

def _replace_en_itn_contextual_multipliers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}x"

    return _EN_ITN_CONTEXTUAL_MULTIPLIER_RE.sub(replace, text)

def _replace_en_itn_context_abbreviated_numbers(text: str) -> str:
    suffixes = {"k": "K", "m": "M", "b": "B"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}{suffixes[match.group(3).lower()]}"

    return _EN_ITN_CONTEXT_ABBREVIATED_NUMBER_RE.sub(replace, text)

def _replace_en_itn_basis_points(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value} bps"

    return _EN_ITN_BASIS_POINT_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_science_units(text: str) -> str:
    numerator_units = {
        "millimole": "mmol",
        "mole": "mol",
        "microgram": "µg",
        "nanogram": "ng",
        "milligram": "mg",
        "gram": "g",
        "international unit": "IU",
        "unit": "U",
        "mmol": "mmol",
        "mol": "mol",
        "ug": "µg",
        "µg": "µg",
        "μg": "µg",
        "mcg": "µg",
        "ng": "ng",
        "mg": "mg",
        "g": "g",
        "iu": "IU",
        "u": "U",
    }
    denominator_units = {
        "liter": "L",
        "deciliter": "dL",
        "kilogram": "kg",
        "milliliter": "mL",
        "microliter": "µL",
        "l": "L",
        "dl": "dL",
        "kg": "kg",
        "ml": "mL",
        "ul": "µL",
        "µl": "µL",
        "μl": "µL",
    }
    compacted = _EN_ITN_PARTS_PER_OUTPUT_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} "
            f"{'ppm' if match.group(2).lower() == 'million' else 'ppb'}"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        text,
    )
    compacted = _EN_ITN_MERCURY_PRESSURE_OUTPUT_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} mmHg"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        compacted,
    )
    compacted = _EN_ITN_KILOPASCAL_OUTPUT_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} kPa"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        compacted,
    )
    compacted = _EN_ITN_PASCAL_OUTPUT_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} "
            f"{'MPa' if match.group(2).lower().startswith('mega') else 'Pa'}"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        compacted,
    )

    def replace_ratio(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        numerator = match.group(2).lower().removesuffix("s")
        denominator = match.group(3).lower().removesuffix("s")
        return f"{value} {numerator_units[numerator]}/{denominator_units[denominator]}"

    compacted = _EN_ITN_SCIENCE_RATIO_OUTPUT_RE.sub(replace_ratio, compacted)

    def replace_simple(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        unit_symbols = {"microgram": "µg", "nanogram": "ng", "microliter": "µL"}
        return f"{value} {unit_symbols[unit]}"

    return _EN_ITN_MICRO_SIMPLE_OUTPUT_RE.sub(replace_simple, compacted)

def _replace_en_itn_electrical_units(text: str) -> str:
    unit_symbols = {
        "megaohm": "MΩ",
        "kiloohm": "kΩ",
        "ohm": "Ω",
        "kilovolt": "kV",
        "millivolt": "mV",
        "milliampere": "mA",
        "ampere": "A",
        "milliwatt": "mW",
        "watt": "W",
        "microfarad": "µF",
        "nanofarad": "nF",
        "picofarad": "pF",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {unit_symbols[unit]}"

    return _EN_ITN_ELECTRICAL_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_motion_and_rate_units(text: str) -> str:
    compacted = _EN_ITN_ACCELERATION_OUTPUT_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} m/s²"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        text,
    )
    compacted = _EN_ITN_MPS_SQUARED_OUTPUT_RE.sub(r"\1 m/s²", compacted)
    compacted = _EN_ITN_LITER_PER_MINUTE_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} L/min"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        compacted,
    )
    return _EN_ITN_REVOLUTIONS_PER_MINUTE_RE.sub(
        lambda match: (
            f"{_parse_en_number_phrase(match.group(1))} rpm"
            if _parse_en_number_phrase(match.group(1)) is not None
            else match.group(0)
        ),
        compacted,
    )

def _replace_en_itn_engineering_units(text: str) -> str:
    compacted = _EN_ITN_PH_OUTPUT_RE.sub("pH", text)
    unit_symbols = {
        "decibel": "dB",
        "decibel milliwatt": "dBm",
        "a weighted decibel": "dBA",
        "watt per square meter": "W/m²",
        "newton meter": "N·m",
        "newton": "N",
        "milliampere hour": "mAh",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = re.sub(r"\s+", " ", match.group(2).lower().removesuffix("s"))
        if unit.startswith("watts "):
            unit = unit.replace("watts ", "watt ", 1)
        return f"{value} {unit_symbols[unit]}"

    return _EN_ITN_ENGINEERING_OUTPUT_RE.sub(replace, compacted)

def _replace_en_itn_comparisons(text: str) -> str:
    operator_symbols = {
        "greater than or equal to": ">=",
        "less than or equal to": "<=",
        "not equal to": "!=",
        "approximately equal to": "≈",
        "greater than": ">",
        "less than": "<",
        "equals": "=",
        "equal": "=",
        "is equal to": "=",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(3))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{operator_symbols[match.group(2).lower()]}{value}"

    return _EN_ITN_COMPARISON_RE.sub(replace, text)

def _restore_en_itn_ftp_urls(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        body = match.group(1).strip()
        body = re.sub(r"\s+dot\s+", ".", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+slash\s+", "/", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+underscore\s+", "_", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+(dash|hyphen)\s+", "-", body, flags=re.IGNORECASE)
        return f"ftp://{body.replace(' ', '')}"

    return _EN_ITN_FTP_URL_RE.sub(replace, text)

def _restore_en_itn_spoken_domains(text: str) -> str:
    partially_restored = _EN_ITN_PARTIAL_WWW_DOMAIN_RE.sub(r"www.\1", text)

    def replace(match: re.Match[str]) -> str:
        first = re.sub(r"\s+", "", match.group(1).lower())
        body = f"{first} dot {match.group(2)}"
        body = re.sub(r"\s+dot\s+", ".", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+slash\s+", "/", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+underscore\s+", "_", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+(dash|hyphen)\s+", "-", body, flags=re.IGNORECASE)
        return body.replace(" ", "")

    return _EN_ITN_SPOKEN_DOMAIN_RE.sub(replace, partially_restored)

def _normalize_en_itn_unit_case(text: str) -> str:
    output = text
    for pattern, replacement in _EN_ITN_UNIT_CASE_OUTPUT_REPLACEMENTS:
        output = pattern.sub(replacement, output)
    return output

def _replace_en_itn_per_mille(text: str) -> str:
    compacted = _EN_ITN_DIGIT_PER_MILLE_RE.sub(r"\1‰", text)
    return _EN_ITN_WORD_PER_MILLE_RE.sub(
        lambda match: f"{_EN_ITN_NUMBER_WORD_VALUES[match.group(1).lower()]}‰",
        compacted,
    )

def _restore_en_itn_explicit_emails(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        local = _restore_en_itn_email_local_part(match.group(2))
        domain = _restore_en_itn_email_domain_part(match.group(3))
        return f"{match.group(1)}{local}@{domain}"

    return _EN_ITN_EXPLICIT_EMAIL_RE.sub(replace, text)

def _restore_en_itn_email_local_part(text: str) -> str:
    symbol_map = {"dot": ".", "plus": "+", "dash": "-", "hyphen": "-", "underscore": "_"}
    return "".join(symbol_map.get(token.lower(), token) for token in text.split())

def _restore_en_itn_email_domain_part(text: str) -> str:
    return re.sub(r"\s+dot\s+", ".", text, flags=re.IGNORECASE)

def _replace_en_itn_common_fractions(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        numerator = _EN_ITN_NUMBER_WORD_VALUES[match.group(1).lower()]
        denominator = _EN_ITN_DENOMINATOR_WORD_VALUES[match.group(2).lower()]
        return f"{numerator}/{denominator}"

    return _EN_ITN_COMMON_FRACTION_RE.sub(replace, text)

def _replace_en_itn_dimensions(text: str) -> str:
    unit_symbols = {
        "centimeter": "cm",
        "millimeter": "mm",
        "kilometer": "km",
        "meter": "m",
        "inch": "in",
        "foot": "ft",
        "feet": "ft",
        "pixel": "px",
        "cm": "cm",
        "mm": "mm",
        "km": "km",
        "m": "m",
        "in": "in",
        "ft": "ft",
        "px": "px",
    }

    def replace(match: re.Match[str]) -> str:
        left = _parse_en_number_phrase(match.group(1))
        right = _parse_en_number_phrase(match.group(2))
        if left is None or right is None:
            return match.group(0)
        raw_unit = (match.group(3) or "").lower()
        unit = unit_symbols.get(raw_unit, unit_symbols.get(raw_unit.removesuffix("s"), ""))
        return f"{left}x{right}{unit}"

    return _EN_ITN_DIMENSION_OUTPUT_RE.sub(replace, text)

def _replace_en_itn_contextual_ratios(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        left = _parse_en_integer_phrase(match.group(2))
        right = _parse_en_integer_phrase(match.group(3))
        if left is None or right is None:
            return match.group(0)
        return f"{match.group(1)}{left}:{right}"

    return _EN_ITN_CONTEXTUAL_RATIO_RE.sub(replace, text)

def _replace_en_itn_contextual_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _parse_en_integer_phrase(match.group(1))
        end = _parse_en_integer_phrase(match.group(2))
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end} {match.group(3)}"

    return _EN_ITN_CONTEXTUAL_RANGE_RE.sub(replace, text)

def _replace_en_itn_liter_units(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value} L"

    return _EN_ITN_LITER_RE.sub(replace, text)

def _replace_en_itn_milliseconds(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value} ms"

    return _EN_ITN_MILLISECOND_RE.sub(replace, text)

def _replace_en_itn_data_bytes(text: str) -> str:
    unit_symbols = {
        "byte": "B",
        "kilobyte": "KB",
        "megabyte": "MB",
        "gigabyte": "GB",
        "terabyte": "TB",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {unit_symbols[unit]}"

    return _EN_ITN_DATA_BYTE_RE.sub(replace, text)

def _replace_en_itn_binary_bytes(text: str) -> str:
    unit_symbols = {"gibibyte": "GiB", "mebibyte": "MiB", "kibibyte": "KiB"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(2).lower().removesuffix("s")
        return f"{value} {unit_symbols[unit]}"

    return _EN_ITN_BINARY_BYTE_RE.sub(replace, text)

def _replace_en_itn_power_units(text: str) -> str:
    unit_symbols = {
        ("square", "meter"): "m²",
        ("square", "centimeter"): "cm²",
        ("square", "millimeter"): "mm²",
        ("square", "kilometer"): "km²",
        ("square", "yard"): "yd²",
        ("cubic", "meter"): "m³",
        ("cubic", "centimeter"): "cm³",
        ("cubic", "millimeter"): "mm³",
        ("cubic", "kilometer"): "km³",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_en_number_phrase(match.group(1))
        if value is None:
            return match.group(0)
        unit = match.group(3).lower().removesuffix("s")
        return f"{value} {unit_symbols[(match.group(2).lower(), unit)]}"

    return _EN_ITN_POWER_UNIT_RE.sub(replace, text)

def _replace_en_itn_context_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_integer_phrase(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)} {value}"

    return _EN_ITN_CONTEXT_NUMBER_RE.sub(replace, text)

def _replace_en_itn_formula_equals(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_en_integer_phrase(match.group(2))
        if value is None:
            return match.group(0)
        formula = re.sub(r"\s+", "", match.group(1))
        return f"{formula}={value}"

    return _EN_ITN_FORMULA_EQUALS_RE.sub(replace, text)

def _replace_en_itn_word_operator_formulas(text: str) -> str:
    operator_symbols = {"plus": "+", "minus": "-", "times": "*", "divided": "/", "divided by": "/"}

    def replace(match: re.Match[str]) -> str:
        left = _parse_en_integer_phrase(match.group(1))
        right = _parse_en_integer_phrase(match.group(3))
        result = _parse_en_integer_phrase(match.group(4))
        if left is None or right is None or result is None:
            return match.group(0)
        return f"{left}{operator_symbols[match.group(2).lower()]}{right}={result}"

    return _EN_ITN_WORD_OPERATOR_FORMULA_RE.sub(replace, text)

def _parse_en_integer_phrase(text: str) -> int | None:
    raw = text.strip().lower().replace("-", " ")
    if not raw:
        return None
    if raw.isdigit():
        return int(raw)

    total = 0
    current = 0
    seen_number = False
    for token in raw.split():
        if token == "and":
            continue
        value = _EN_ITN_INTEGER_WORD_VALUES_FULL.get(token)
        if value is not None:
            current += value
            seen_number = True
            continue
        scale = _EN_ITN_INTEGER_SCALE_VALUES.get(token)
        if scale is None:
            return None
        if current == 0:
            current = 1
        current *= scale
        if scale >= 1000:
            total += current
            current = 0
        seen_number = True
    if not seen_number:
        return None
    return total + current

def _parse_en_year_phrase(text: str) -> int | None:
    raw = text.strip().lower().replace("-", " ")
    words = raw.split()
    if not words:
        return None
    if words[0] == "twenty" and len(words) >= 2:
        suffix = _parse_en_integer_phrase(" ".join(words[1:]))
        if suffix is not None and 0 <= suffix <= 99:
            return 2000 + suffix
    value = _parse_en_integer_phrase(raw)
    if value is not None and 1000 <= value <= 2999:
        return value
    return None

def _parse_en_ordinal_phrase(text: str) -> int | None:
    raw = text.strip().lower().replace("-", " ")
    ordinal_values = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10,
        "eleventh": 11,
        "twelfth": 12,
        "thirteenth": 13,
        "fourteenth": 14,
        "fifteenth": 15,
        "sixteenth": 16,
        "seventeenth": 17,
        "eighteenth": 18,
        "nineteenth": 19,
        "twentieth": 20,
        "thirtieth": 30,
    }
    if raw in ordinal_values:
        return ordinal_values[raw]
    parts = raw.split()
    if len(parts) == 2 and parts[0] in {"twenty", "thirty"} and parts[1] in ordinal_values:
        base = 20 if parts[0] == "twenty" else 30
        suffix = ordinal_values[parts[1]]
        if 1 <= suffix <= 9:
            return base + suffix
    return None

def _parse_en_number_phrase(text: str) -> str | None:
    raw = text.strip().lower()
    if re.fullmatch(r"\d+(?:\.\d+)?", raw):
        return raw
    if " point " in raw:
        integer_text, fractional_text = raw.split(" point ", 1)
        integer = _parse_en_integer_phrase(integer_text)
        if integer is None:
            return None
        digits = []
        for token in fractional_text.split():
            digit = _EN_ITN_INTEGER_WORD_VALUES_FULL.get(token)
            if digit is None or digit > 9:
                return None
            digits.append(str(digit))
        if not digits:
            return None
        return f"{integer}.{''.join(digits)}"
    value = _parse_en_integer_phrase(raw)
    return str(value) if value is not None else None

def prepare_input(text: str) -> str:
    return _prepare_en_itn_input(text)

def finalize_outputs(texts: list[str]) -> list[str]:
    return [_restore_en_itn_layout_commands(_restore_en_itn_format_symbols(_compact_en_itn_spacing(text))) for text in texts]
