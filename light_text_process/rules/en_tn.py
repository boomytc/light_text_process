from __future__ import annotations
import re
from decimal import Decimal, InvalidOperation
from collections.abc import Callable
from light_text_process.rules.en_dates import (
    verbalize_digit_month_name_dates,
    verbalize_dotted_numeric_dates,
    verbalize_iso_date_ranges,
    verbalize_numeric_ordinal_ranges,
    verbalize_numeric_ordinals,
)


_AMPM = r"(?:a\.?m\.?|p\.?m\.?)"

_AMPM_RANGE_RE = re.compile(
    rf"\b(\d{{1,2}})(?::([0-5]\d))?\s*({_AMPM})\s*[-~～–—]\s*"
    rf"(\d{{1,2}})(?::([0-5]\d))?\s*({_AMPM})\b",
    re.IGNORECASE,
)

_CONTEXT_TEMPERATURE_RE = re.compile(
    r"\b((?:temperature|temp|feels\s+like|feels|room\s+temperature|body\s+temperature)"
    r"(?:\s+(?:is|was))?\s+)([-+]?\d+(?:\.\d+)?)\s*(?:degrees?\s*)?(°C|℃|C|°F|℉|F)(?=$|[^A-Za-z])",
    re.IGNORECASE,
)

_CONTEXT_TEMPERATURE_RANGE_RE = re.compile(
    r"\b((?:temperature|temp|feels\s+like|feels|room\s+temperature|body\s+temperature)"
    r"(?:\s+(?:is|was))?\s+)([-+]?\d+(?:\.\d+)?)\s*[-~～–—]\s*"
    r"([-+]?\d+(?:\.\d+)?)\s*(?:degrees?\s*)?(°C|℃|C|°F|℉|F)(?=$|[^A-Za-z])",
    re.IGNORECASE,
)

_WEEKDAY = r"mon(?:day)?|tue(?:sday)?|wed(?:nesday)?|thu(?:rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?"

_WEEKDAY_RANGE_RE = re.compile(rf"\b({_WEEKDAY})\s*[-–—]\s*({_WEEKDAY})\b", re.IGNORECASE)

_NUMERIC_RATING_RE = re.compile(
    r"\b((?:rating|score|rated|stars?|NPS)(?:\s+(?:is|was))?\s+)(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)

_PAGE_RANGE_ABBREVIATION_RE = re.compile(r"\bpp\.\s*(\d+)\s*[-~～–—]\s*(\d+)\b", re.IGNORECASE)

_PAGE_ABBREVIATION_RE = re.compile(r"\bp\.\s*(\d+)\b", re.IGNORECASE)

_COMPACT_HOUR_MINUTE_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hours?)\s*(\d+(?:\.\d+)?)\s*(?:m|min|mins|minutes?)\b",
    re.IGNORECASE,
)

_COMPACT_MINUTE_SECOND_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(?:m|min|mins|minutes?)\s*(\d+(?:\.\d+)?)\s*(?:s|sec|secs|seconds?)\b",
    re.IGNORECASE,
)

_CURRENCY_PER_UNIT_RE = re.compile(
    r"(?<!\w)([$€£¥])\s*(\d[\d,]*(?:\.\d+)?)\s*/\s*"
    r"(kg|kilograms?|g|grams?|lb|pounds?|oz|ounces?|h|hr|hours?|day|days|month|months|year|years|"
    r"m²|㎡|square\s+meters?|m|meters?|km|kilometers?)(?![A-Za-z])",
    re.IGNORECASE,
)

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

def verbalize_ampm_time_ranges(
    text: str,
    *,
    format_clock_time: Callable[[int, int, str], str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        start_hour = int(match.group(1))
        start_minute = int(match.group(2) or "0")
        end_hour = int(match.group(4))
        end_minute = int(match.group(5) or "0")
        if start_hour > 12 or end_hour > 12:
            return match.group(0)
        start_suffix = f" {match.group(3).replace('.', '').upper()}"
        end_suffix = f" {match.group(6).replace('.', '').upper()}"
        return (
            f"{format_clock_time(start_hour, start_minute, start_suffix)} to "
            f"{format_clock_time(end_hour, end_minute, end_suffix)}"
        )

    return _AMPM_RANGE_RE.sub(replace, text)

def verbalize_weekday_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _WEEKDAY_NAMES[match.group(1).lower()]
        end = _WEEKDAY_NAMES[match.group(2).lower()]
        return f"{start} to {end}"

    return _WEEKDAY_RANGE_RE.sub(replace, text)

def verbalize_numeric_ratings(text: str) -> str:
    return _NUMERIC_RATING_RE.sub(r"\1\2 out of \3", text)

def verbalize_page_abbreviations(text: str) -> str:
    prepared = _PAGE_RANGE_ABBREVIATION_RE.sub(r"pages \1 to \2", text)
    return _PAGE_ABBREVIATION_RE.sub(r"page \1", prepared)

def verbalize_compact_duration_sequences(text: str) -> str:
    def unit(value: str, singular: str) -> str:
        normalized = value.rstrip("0").rstrip(".") if "." in value else value
        return singular if normalized == "1" else f"{singular}s"

    def replace_hour_minute(match: re.Match[str]) -> str:
        return f"{match.group(1)} {unit(match.group(1), 'hour')} {match.group(2)} {unit(match.group(2), 'minute')}"

    def replace_minute_second(match: re.Match[str]) -> str:
        return f"{match.group(1)} {unit(match.group(1), 'minute')} {match.group(2)} {unit(match.group(2), 'second')}"

    prepared = _COMPACT_HOUR_MINUTE_RE.sub(replace_hour_minute, text)
    return _COMPACT_MINUTE_SECOND_RE.sub(replace_minute_second, prepared)

def verbalize_currency_per_units(text: str) -> str:
    unit_words = {
        "kg": "kilogram",
        "kilogram": "kilogram",
        "kilograms": "kilogram",
        "g": "gram",
        "gram": "gram",
        "grams": "gram",
        "lb": "pound",
        "pound": "pound",
        "pounds": "pound",
        "oz": "ounce",
        "ounce": "ounce",
        "ounces": "ounce",
        "h": "hour",
        "hr": "hour",
        "hour": "hour",
        "hours": "hour",
        "day": "day",
        "days": "day",
        "month": "month",
        "months": "month",
        "year": "year",
        "years": "year",
        "m²": "square meter",
        "㎡": "square meter",
        "square meter": "square meter",
        "square meters": "square meter",
        "m": "meter",
        "meter": "meter",
        "meters": "meter",
        "km": "kilometer",
        "kilometer": "kilometer",
        "kilometers": "kilometer",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)} per {unit_words[match.group(3).lower()]}"

    return _CURRENCY_PER_UNIT_RE.sub(replace, text)

def verbalize_context_temperatures(text: str) -> str:
    unit_words = {
        "°c": "degrees Celsius",
        "℃": "degrees Celsius",
        "c": "degrees Celsius",
        "°f": "degrees Fahrenheit",
        "℉": "degrees Fahrenheit",
        "f": "degrees Fahrenheit",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)} {unit_words[match.group(3).lower()]}"

    return _CONTEXT_TEMPERATURE_RE.sub(replace, text)

def verbalize_context_temperature_ranges(text: str) -> str:
    unit_words = {
        "°c": "degrees Celsius",
        "℃": "degrees Celsius",
        "c": "degrees Celsius",
        "°f": "degrees Fahrenheit",
        "℉": "degrees Fahrenheit",
        "f": "degrees Fahrenheit",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)} to {match.group(3)} {unit_words[match.group(4).lower()]}"

    return _CONTEXT_TEMPERATURE_RANGE_RE.sub(replace, text)

_EN_TN_LETTER_DECIMAL_VERSION_RE = re.compile(r"\b([A-Za-z])(\d+\.\d+)\b")

_ASCII_DOMAIN_RE = re.compile(
    r"(?<!://)(?<![@A-Za-z0-9_./-])(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}"
    r"(?:/[A-Za-z0-9._~!$&'()*+,;=%-]+)?(?![A-Za-z0-9_-])"
)

_EN_TN_LETTER_DOTTED_VERSION_RE = re.compile(r"\b([A-Za-z])(\d+(?:\.\d+){2,})\b")

_EN_TN_SEMVER_RE = re.compile(
    r"(?<![A-Za-z0-9.])([Vv]?\d+\.\d+\.\d+(?:-[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)?(?:\+[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)?)(?![A-Za-z0-9:]|\.\d)"
)

_EN_TN_CONTEXT_DOTTED_VERSION_RE = re.compile(
    r"\b([Vv]ersion|[Bb]uild|[Rr]elease)\s+(\d+(?:\.\d+){2,})\b"
)

_EN_TN_CONTEXT_CODE_RE = re.compile(
    r"\b((?:order|invoice|tracking|ticket|sku|serial|case|shipment|code|id|"
    r"license\s+plate|plate|vin|passport|driver'?s?\s+license|driver\s+license|model)"
    r"(?:\s+(?:number|no\.?|id))?\s+)"
    r"([A-Z0-9][A-Z0-9-]{2,})\b",
    re.IGNORECASE,
)

def _normalize_decimal_text(value: str) -> str:
    if "." not in value:
        return value
    integer_text, fractional_text = value.split(".", 1)
    trimmed_fraction = fractional_text.rstrip("0")
    if not trimmed_fraction:
        return integer_text
    return f"{integer_text}.{trimmed_fraction}"

_EN_TN_ZIP_CODE_RE = re.compile(r"\b(ZIP(?:\s+code)?\s+)(\d{5})(?:-(\d{4}))?\b", re.IGNORECASE)

_EN_TN_ROOM_CODE_RE = re.compile(
    r"\b((?:room|suite|ste\.?|apt\.?|apartment|unit)\s+)([A-Za-z]?-?\d{1,6}[A-Za-z]?)\b(?!\s+(?:sq\.?|square)\b)",
    re.IGNORECASE,
)

_EN_TN_ADDRESS_ABBREVIATION_REPLACEMENTS = (
    (re.compile(r"\bApt\.\s*", re.IGNORECASE), "apartment "),
    (re.compile(r"\bSte\.\s*", re.IGNORECASE), "suite "),
)

_EN_TN_PREFIX_CURRENCY_RE = re.compile(
    r"\b(USD|EUR|GBP|CNY|RMB|JPY|HKD)\s+(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)\b",
    re.IGNORECASE,
)

_EN_TN_SUFFIX_CURRENCY_RE = re.compile(
    r"\b(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)\s*(USD|EUR|GBP|CNY|RMB|JPY|HKD)\b",
    re.IGNORECASE,
)

_EN_TN_SUFFIX_MONEY_UNIT_RE = re.compile(
    r"\b(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)\s+(dollars?|euros?|pounds?|yen)\b",
    re.IGNORECASE,
)

_EN_TN_SYMBOL_CURRENCY_RANGE_RE = re.compile(
    r"(?<!\w)(HK\$|[$€£¥])\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)"
    r"\s*[-~～–—]\s*(?:\1\s*)?(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)"
)

_EN_TN_SYMBOL_CURRENCY_COMMA_RE = re.compile(
    r"(?<!\w)(HK\$|[$€£¥])\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)"
)

_EN_TN_NUMERIC_DATE_RE = re.compile(
    r"\b(?:(\d{4})/(\d{1,2})/(\d{1,2})|(\d{1,2})/(\d{1,2})/(\d{2,4}))\b"
)

_EN_TN_CONTEXT_NUMBER_LABEL_RE = re.compile(
    r"\b(Ch|Chap|Chapter|Sec|Section|Fig|Figure|Eq|Equation|No)\.\s*(\d+)\b",
    re.IGNORECASE,
)

_EN_TN_TIMEZONE_RE = re.compile(r"\b(UTC|GMT)([+-])(\d{1,2})(?::?(\d{2}))?\b", re.IGNORECASE)

_EN_TN_QUARTER_RE = re.compile(r"\b(?:Q([1-4])\s+(\d{4})|(\d{4})\s+Q([1-4]))\b", re.IGNORECASE)

_EN_TN_FISCAL_YEAR_RE = re.compile(r"\bFY\s*(\d{4})\b", re.IGNORECASE)

_EN_TN_HTTP_STATUS_RE = re.compile(r"\b((?:HTTP|HTTPS)\s+)([1-5]\d{2})\b", re.IGNORECASE)

_EN_TN_PORT_RE = re.compile(r"\b(port\s+)(\d{2,5})\b", re.IGNORECASE)

_EN_TN_ISO_DATETIME_RE = re.compile(
    r"\b(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)\b"
)

_EN_TN_SPACE_DATETIME_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}(?::\d{2})?)\b")

_EN_TN_CLOCK_TIME_RANGE_RE = re.compile(
    r"(?<![\d.:])(\d{1,2}):([0-5]\d)\s*[-~～–—]\s*(\d{1,2}):([0-5]\d)(?![:\d])"
)

_EN_TN_CLOCK_TIME_RE = re.compile(r"(?<![\d.:])(\d{1,2}):([0-5]\d)(?:\s*([AaPp]\.[Mm]\.|[AaPp][Mm]))?(?![:\d])")

_EN_TN_CONTEXT_TEMPERATURE_RE = re.compile(
    r"\b((?:temperature|temp)(?:\s+(?:is|was))?\s+)([-+]?\d+(?:\.\d+)?)\s*([CF])\b",
    re.IGNORECASE,
)

_EN_TN_PLUS_MINUS_TEMPERATURE_RE = re.compile(r"±\s*(\d+(?:\.\d+)?)\s*(°C|℃|C|°F|℉|F)(?=$|[^A-Za-z])")

_EN_TN_PLUS_MINUS_RE = re.compile(r"±\s*(\d+(?:\.\d+)?)")

_EN_SHORTCUT_MODIFIER = (
    r"(?:Ctrl|Control|Cmd|Command|Shift|Alt|Option|Meta|Win|Windows|Fn|Esc|Tab|Enter|Return|"
    r"Space|Delete|Del|Backspace)"
)

_EN_SHORTCUT_KEY = (
    r"(?:Ctrl|Control|Cmd|Command|Shift|Alt|Option|Meta|Win|Windows|Fn|Esc|Tab|Enter|Return|"
    r"Space|Delete|Del|Backspace|F\d{1,2}|[A-Z0-9])"
)

_EN_TN_SHORTCUT_RE = re.compile(rf"\b({_EN_SHORTCUT_MODIFIER}(?:\+{_EN_SHORTCUT_KEY}){{1,5}})\b")

_EN_TN_COMPLEX_URL_RE = re.compile(
    r"\b(?:https?|ftp)://[A-Za-z0-9._~:/?#@!$&'()*+,;=%-]*[?#&=][A-Za-z0-9._~:/?#@!$&'()*+,;=%-]*[A-Za-z0-9)]"
)

_EN_TN_FILE_CONTEXT_RE = re.compile(
    r"\b((?:file|filename|path|directory|dir)\s+)([A-Za-z0-9_./~:\\-]+)",
    re.IGNORECASE,
)

_EN_TN_MAC_ADDRESS_RE = re.compile(
    r"\b((?:MAC(?:\s+address)?|BSSID)\s+)((?:[A-F0-9]{2}:){5}[A-F0-9]{2})\b",
    re.IGNORECASE,
)

_EN_TN_UUID_RE = re.compile(
    r"\b(UUID\s+)([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})\b",
    re.IGNORECASE,
)

_EN_TN_HEX_COLOR_RE = re.compile(
    r"\b((?:color|colour|hex(?:\s+color)?|background(?:\s+color)?|foreground(?:\s+color)?)\s+)#([A-F0-9]{3,8})\b",
    re.IGNORECASE,
)

_EN_TN_IPV4_PORT_RE = re.compile(r"\b((?:\d{1,3}\.){3}\d{1,3}):(\d{1,5})\b")

_EN_TN_IPV6_RE = re.compile(
    r"\b(IPv6\s+)([0-9A-F]{1,4}(?::[0-9A-F]{0,4}){2,7})\b",
    re.IGNORECASE,
)

_EN_TN_ISBN_RE = re.compile(r"\b(ISBN(?:-1[03])?\s+)([0-9X][0-9X-]{8,20})\b", re.IGNORECASE)

_EN_TN_DOI_RE = re.compile(
    r"\b(DOI\s+)(10\.\d{4,9}/[A-Za-z0-9._;()/:+-]*[A-Za-z0-9)])",
    re.IGNORECASE,
)

_EN_TN_SOCIAL_HANDLE_RE = re.compile(r"(?<![\w.])@([A-Za-z][A-Za-z0-9_]{1,50})")

_EN_TN_SOCIAL_HASHTAG_RE = re.compile(r"(?<![\w.])#([A-Za-z][A-Za-z0-9_]{1,60})")

_EN_TN_NEGATIVE_CURRENCY_RE = re.compile(r"(?<!\w)-\s*([$€£])(\d+(?:\.\d+)?)")

_EN_TN_POSITIVE_PERCENT_RE = re.compile(r"(?<!\w)\+\s*(\d+(?:\.\d+)?)\s*%")

_EN_TN_PERCENT_RANGE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*%\s*[-~～–—]\s*(\d+(?:\.\d+)?)\s*%")

_EN_TN_PER_MILLE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*‰")

_EN_TN_PERCENT_POINT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*pp\b", re.IGNORECASE)

_EN_TN_SCIENTIFIC_E_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*[eE]\s*([+-]?\d+)\b")

_EN_TN_SCIENTIFIC_POWER_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*[xX×]\s*10\^([+-]?\d+)(m/s)?\b",
    re.IGNORECASE,
)

_EN_TN_COORDINATE_RE = re.compile(
    r"\b(-?\d+(?:\.\d+)?)\s*[°º]\s*([NSEW])\b",
    re.IGNORECASE,
)

_EN_TN_CONTEXT_HASH_NUMBER_RE = re.compile(
    r"\b((?:item|order|ticket|case|invoice|ref(?:erence)?|number|no\.?)\s+)#\s*(\d+)\b",
    re.IGNORECASE,
)

_EN_TN_BYTES_PER_SECOND_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(GiB|MiB|KiB|TB|GB|MB|KB)/s\b",
    re.IGNORECASE,
)

_EN_TN_FRAMES_PER_SECOND_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*fps\b", re.IGNORECASE)

_EN_TN_COMPACT_DURATION_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)(h|min|s)\b", re.IGNORECASE)

_EN_TN_DEGREE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*deg\b", re.IGNORECASE)

_EN_TN_KILOMETER_PER_HOUR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*km/h\b", re.IGNORECASE)

_EN_TN_METER_PER_SECOND_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*m/s\b", re.IGNORECASE)

_EN_TN_ACCELERATION_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*m/s(?:\^?2|²)\b", re.IGNORECASE)

_EN_TN_LITER_PER_MINUTE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*l/min\b", re.IGNORECASE)

_EN_TN_REVOLUTIONS_PER_MINUTE_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*rpm\b", re.IGNORECASE)

_EN_TN_MILES_PER_HOUR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*mph\b", re.IGNORECASE)

_EN_TN_COMPACT_IMPERIAL_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)(ft|in|lb|oz|mi|yd)\b", re.IGNORECASE)

_EN_TN_COMPACT_UNIT_RANGE_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*[-~～–—]\s*(\d+(?:\.\d+)?)\s*"
    r"(kg|mg|g|km|cm|mm|m|L|l|mL|ml|h|min|s|ms|ft|in|lb|oz|mi|yd)\b",
    re.IGNORECASE,
)

_EN_TN_PER_POWER_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(kg|g|lb|W)/m([²³23])\b", re.IGNORECASE)

_EN_TN_SQUARE_METER_SYMBOL_RE = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(?:㎡|m²)(?![A-Za-z])")

_EN_TN_POWER_SYMBOL_UNIT_RE = re.compile(
    r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(m|cm|mm|km|yd|ft|in)([²³23])\b",
    re.IGNORECASE,
)

_EN_TN_SQUARE_UNIT_WORD_RE = re.compile(
    r"\b(\d[\d,]*(?:\.\d+)?)\s*"
    r"(?:sq\.?\s*(m|meter|meters|km|kilometer|kilometers|cm|centimeter|centimeters|"
    r"mm|millimeter|millimeters|ft|foot|feet|in|inch|inches|yd|yard|yards)|"
    r"square\s+(m|meter|meters|km|kilometer|kilometers|cm|centimeter|centimeters|"
    r"mm|millimeter|millimeters|ft|foot|feet|in|inch|inches|yd|yard|yards))\b",
    re.IGNORECASE,
)

_EN_TN_DECIBEL_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(dBA|dBm|dB)\b", re.IGNORECASE)

_EN_TN_TORQUE_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*N[·.]?m\b", re.IGNORECASE)

_EN_TN_MAH_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*mAh\b", re.IGNORECASE)

_EN_TN_NEWTON_UNIT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*N(?![A-Za-z·.])")

_EN_TN_BASIS_POINT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*bps?\b", re.IGNORECASE)

_EN_TN_DIMENSION_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+(?:\.\d+)?)"
    r"\s*(cm|mm|km|m|in|ft|px)?(?=$|[,.;:!?\s])",
    re.IGNORECASE,
)

_EN_TN_ELECTRICAL_UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*(MΩ|kΩ|Ω|kV|mV|mA|mW|A|W|µF|μF|uF|nF|pF)(?![A-Za-z])",
    re.IGNORECASE,
)

_EN_TN_SCIENCE_RATIO_UNIT_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(mmol|mol|ug|µg|μg|mcg|ng|mg|g|IU|U)/(L|dL|kg|mL|uL|µL|μL)\b",
    re.IGNORECASE,
)

_EN_TN_MICRO_SIMPLE_UNIT_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(uL|µL|μL|ug|µg|μg|mcg|ng)\b",
    re.IGNORECASE,
)

_EN_TN_CONTEXT_ABBREVIATED_NUMBER_RE = re.compile(
    r"\b((?:users?|views?|followers?|downloads?|visits?|records?|rows?|items?|sales|"
    r"revenue|profit|income|earnings|valuation|budget|market\s+cap)\s+)"
    r"(\d+(?:\.\d+)?)\s*([KMB])\b",
    re.IGNORECASE,
)

_EN_TN_SIMPLE_UNIT_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(GiB|gib|MiB|mib|KiB|kib|kWh|KWh|kW|KW|GHz|MHz|kHz|KHz|Hz|GB|gb|TB|tb|MB|mb|KB|kb|"
    r"MPa|mpa|Pa|pa|"
    r"mmHg|MMHG|mmhg|kPa|KPA|kpa|ppm|ppb|mL|ml|mA|ms|cm|mm|km|kg|mg|g|L|l|V|v|K|yd|m)\b"
)

_EN_TN_NUMERIC_RANGE_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*[-~～—–]\s*(\d+(?:\.\d+)?)"
    r"(?=\s+(?:days?|weeks?|months?|years?|hours?|minutes?|seconds?|items?|people|pages?|times?|"
    r"meters?|kilometers?|centimeters?|millimeters?|grams?|kilograms?|liters?|dollars?|euros?|"
    r"pounds?|percent|%))",
    re.IGNORECASE,
)

_EN_TN_NUMERIC_RATIO_RE = re.compile(
    r"\b((?:[Rr]atio(?:\s+(?:is|of))?|[Ss]core(?:\s+(?:is|was))?)\s+)"
    r"(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\b"
)

_EN_TN_COMPARISON_RE = re.compile(
    r"\b([A-Za-z][A-Za-z0-9_]*)\s*(!=|≠|>=|≥|≤|<=|>|<|=|≈)\s*(-?\d+(?:\.\d+)?|[A-Za-z][A-Za-z0-9_]*)\b"
)

_EN_TN_MATH_EXPR_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*([+＋\-−×xX*÷/])\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)(?!\w)"
)

_EN_TN_CONTEXT_LONG_DIGITS_RE = re.compile(
    r"\b((?:account|card(?:\s+number)?|card\s+no\.?|id)\s+)(\d[\d -]{7,}\d)\b",
    re.IGNORECASE,
)

_EN_TN_CONTEXT_PHONE_RE = re.compile(
    r"\b((?:call|phone|tel|mobile|hotline|support)\s+)(\+?1[\s-])?(\d{3})-(\d{3})-(\d{4})\b",
    re.IGNORECASE,
)

_EN_TN_EXTENSION_RE = re.compile(r"\b(?:ext\.?|extension)\s*(\d{1,6})\b", re.IGNORECASE)

_EN_TN_NUMBER_ABBREVIATION_RE = re.compile(r"\bNo\.\s*(\d+)\b")

_EN_TN_SIMPLE_URL_RE = re.compile(r"\b(?:https?|ftp)://[A-Za-z0-9._~:/?#@!$&'()*+,;=%-]+")

_EN_TN_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

_EN_TN_IPV4_RE = re.compile(r"(?<![A-Za-z0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![A-Za-z0-9])")

_EN_TN_AIRLINE_CODE_RE = re.compile(r"\b([A-Z]{2})(\d{2,4})\b")

_EN_TN_SYMBOL_MONEY_AMOUNT_RE = re.compile(
    r"(?<!\w)(-)?(HK\$|[$€£¥])\s*((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)"
)

_EN_TN_NEGATIVE_PERCENT_RE = re.compile(r"(?<!\w)-\s*(\d+(?:\.\d+)?)\s*%")

_EN_TN_UNSIGNED_PERCENT_RE = re.compile(r"(?<!\w)(\d+(?:\.\d+)?)\s*%")

_EN_TN_SYMBOL_TEMPERATURE_RE = re.compile(r"(?<![\w.])([-+]?\d+(?:\.\d+)?)\s*(°C|℃|C|°F|℉|F)(?![A-Za-z])")

_EN_TN_FRACTION_RE = re.compile(r"\b(\d+)\s*/\s*(\d+)\b")

_EN_TN_PHONE_PLUS_RE = re.compile(r"\b((?:call|phone|tel|mobile|hotline|support)\s+)\+(\d{1,3})\s+(\d{7,})\b", re.IGNORECASE)

_EN_TN_ISO_DATE_RE = re.compile(r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b")

_EN_TN_MONTH_DATE_YEAR_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December|"
    r"january|february|march|april|may|june|july|august|september|october|november|december)\s+"
    r"(\d{1,2}|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|"
    r"twentieth|twenty first|twenty second|twenty third|twenty fourth|twenty fifth|twenty sixth|"
    r"twenty seventh|twenty eighth|twenty ninth|thirtieth|thirty first)\s+(\d{4})\b"
)

_EN_TN_REMAINING_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9])([+-]?)((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(?![A-Za-z0-9])"
)

def _expand_en_tn_address_abbreviations(text: str) -> str:
    expanded = text
    for pattern, replacement in _EN_TN_ADDRESS_ABBREVIATION_REPLACEMENTS:
        expanded = pattern.sub(replacement, expanded)
    return expanded

def _prepare_en_tn_input(text: str) -> str:
    prepared = _replace_en_tn_prefix_currency_codes(text)
    prepared = _replace_en_tn_suffix_currency_codes(prepared)
    prepared = _replace_en_tn_suffix_money_units(prepared)
    prepared = _verbalize_en_tn_symbol_currency_ranges(prepared)
    prepared = _normalize_en_tn_symbol_currency_commas(prepared)
    prepared = verbalize_currency_per_units(prepared)
    prepared = verbalize_iso_date_ranges(prepared)
    prepared = verbalize_digit_month_name_dates(prepared, format_ordinal=_format_en_ordinal_value)
    prepared = verbalize_dotted_numeric_dates(prepared, format_ordinal=_format_en_ordinal_value)
    prepared = _replace_en_tn_numeric_dates(prepared)
    prepared = verbalize_context_temperature_ranges(prepared)
    prepared = _verbalize_en_tn_context_temperatures(prepared)
    prepared = verbalize_context_temperatures(prepared)
    prepared = verbalize_numeric_ratings(prepared)
    prepared = verbalize_weekday_ranges(prepared)
    prepared = _verbalize_en_tn_timezones(prepared)
    prepared = _verbalize_en_tn_quarters(prepared)
    prepared = _verbalize_en_tn_fiscal_years(prepared)
    prepared = _verbalize_en_tn_structured_tokens(prepared)
    prepared = _verbalize_en_tn_clock_time_ranges(prepared)
    prepared = verbalize_ampm_time_ranges(prepared, format_clock_time=_format_en_tn_clock_time)
    prepared = _verbalize_en_tn_clock_times(prepared)
    prepared = _verbalize_en_tn_shortcuts(prepared)
    prepared = _verbalize_en_tn_complex_urls(prepared)
    prepared = _verbalize_en_tn_simple_urls(prepared)
    prepared = _verbalize_en_tn_emails(prepared)
    prepared = _verbalize_en_tn_technical_tokens(prepared)
    prepared = _verbalize_en_tn_ipv4_addresses(prepared)
    prepared = _verbalize_en_tn_file_tokens(prepared)
    prepared = _verbalize_en_tn_social_tokens(prepared)
    prepared = _expand_en_tn_address_abbreviations(prepared)
    prepared = _verbalize_en_tn_zip_codes(prepared)
    prepared = _verbalize_en_tn_room_codes(prepared)
    prepared = _verbalize_en_tn_context_phone_numbers(prepared)
    prepared = _verbalize_en_ascii_domains(prepared)
    prepared = _verbalize_en_tn_context_codes(prepared)
    prepared = _verbalize_en_tn_context_long_digits(prepared)
    prepared = _verbalize_en_tn_extensions(prepared)
    prepared = _verbalize_en_tn_negative_currency(prepared)
    prepared = _verbalize_en_tn_percent_ranges(prepared)
    prepared = _verbalize_en_tn_positive_percent(prepared)
    prepared = _verbalize_en_tn_per_mille(prepared)
    prepared = _verbalize_en_tn_percentage_points(prepared)
    prepared = _verbalize_en_tn_scientific_notation(prepared)
    prepared = _verbalize_en_tn_coordinates(prepared)
    prepared = _verbalize_en_tn_context_hash_numbers(prepared)
    prepared = _verbalize_en_tn_context_number_labels(prepared)
    prepared = _verbalize_en_tn_number_abbreviations(prepared)
    prepared = _verbalize_en_tn_airline_codes(prepared)
    prepared = verbalize_page_abbreviations(prepared)
    prepared = verbalize_numeric_ordinal_ranges(prepared, format_ordinal=_format_en_ordinal_value)
    prepared = verbalize_numeric_ordinals(prepared, format_ordinal=_format_en_ordinal_value)
    prepared = _verbalize_en_tn_comparisons(prepared)
    prepared = _verbalize_en_tn_plus_minus(prepared)
    prepared = _verbalize_en_tn_math_expressions(prepared)
    prepared = _verbalize_en_tn_numeric_ranges(prepared)
    prepared = _verbalize_en_tn_numeric_ratios(prepared)
    prepared = _verbalize_en_tn_semver_tokens(prepared)
    prepared = _verbalize_en_tn_dotted_versions(prepared)
    prepared = _verbalize_en_tn_dimensions(prepared)
    prepared = verbalize_compact_duration_sequences(prepared)
    prepared = _verbalize_en_tn_measure_units(prepared)
    prepared = _space_en_tn_letter_decimal_versions(prepared)
    return _verbalize_en_tn_remaining_numbers(prepared)

def _replace_en_tn_prefix_currency_codes(text: str) -> str:
    symbol_map = {"usd": "$", "eur": "€", "gbp": "£", "cny": "¥", "rmb": "¥", "jpy": "¥", "hkd": "HK$"}

    def replace(match: re.Match[str]) -> str:
        symbol = symbol_map[match.group(1).lower()]
        amount = match.group(2).replace(",", "")
        if amount.startswith("-"):
            return f"-{symbol}{amount[1:]}"
        return f"{symbol}{amount}"

    return _EN_TN_PREFIX_CURRENCY_RE.sub(replace, text)

def _replace_en_tn_suffix_currency_codes(text: str) -> str:
    symbol_map = {"usd": "$", "eur": "€", "gbp": "£", "cny": "¥", "rmb": "¥", "jpy": "¥", "hkd": "HK$"}

    def replace(match: re.Match[str]) -> str:
        amount = match.group(1).replace(",", "")
        symbol = symbol_map[match.group(2).lower()]
        if amount.startswith("-"):
            return f"-{symbol}{amount[1:]}"
        return f"{symbol}{amount}"

    return _EN_TN_SUFFIX_CURRENCY_RE.sub(replace, text)

def _replace_en_tn_suffix_money_units(text: str) -> str:
    symbol_map = {
        "dollar": "$",
        "dollars": "$",
        "euro": "€",
        "euros": "€",
        "pound": "£",
        "pounds": "£",
        "yen": "¥",
    }

    def replace(match: re.Match[str]) -> str:
        amount = match.group(1).replace(",", "")
        symbol = symbol_map[match.group(2).lower()]
        if amount.startswith("-"):
            return f"-{symbol}{amount[1:]}"
        return f"{symbol}{amount}"

    return _EN_TN_SUFFIX_MONEY_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_symbol_currency_ranges(text: str) -> str:
    unit_words = {"$": "dollars", "€": "euros", "£": "pounds", "¥": "yen", "HK$": "Hong Kong dollars"}

    def replace(match: re.Match[str]) -> str:
        start = _normalize_decimal_text(match.group(2).replace(",", ""))
        end = _normalize_decimal_text(match.group(3).replace(",", ""))
        return f"{start} to {end} {unit_words[match.group(1)]}"

    return _EN_TN_SYMBOL_CURRENCY_RANGE_RE.sub(replace, text)

def _normalize_en_tn_symbol_currency_commas(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        amount = match.group(2).replace(",", "")
        if match.group(1).lower() == "hk$":
            return f"{_normalize_decimal_text(amount)} Hong Kong dollars"
        return f"{match.group(1)}{amount}"

    return _EN_TN_SYMBOL_CURRENCY_COMMA_RE.sub(
        replace,
        text,
    )

def _replace_en_tn_numeric_dates(text: str) -> str:
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    def normalize_year(raw_year: str) -> int:
        if len(raw_year) == 2:
            value = int(raw_year)
            return 2000 + value if value <= 68 else 1900 + value
        return int(raw_year)

    def replace(match: re.Match[str]) -> str:
        if match.group(1):
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
        else:
            month = int(match.group(4))
            day = int(match.group(5))
            year = normalize_year(match.group(6))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{month_names[month].lower()} {day} {year}"

    return _EN_TN_NUMERIC_DATE_RE.sub(replace, text)

def _verbalize_en_tn_context_temperatures(text: str) -> str:
    unit_words = {"c": "degrees Celsius", "f": "degrees Fahrenheit"}
    return _EN_TN_CONTEXT_TEMPERATURE_RE.sub(
        lambda match: f"{match.group(1)}{match.group(2)} {unit_words[match.group(3).lower()]}",
        text,
    )

def _verbalize_en_tn_timezones(text: str) -> str:
    sign_words = {"+": "plus", "-": "minus"}

    def replace(match: re.Match[str]) -> str:
        minute = f" {match.group(4)}" if match.group(4) else ""
        return f"{match.group(1).upper()} {sign_words[match.group(2)]} {match.group(3)}{minute}"

    return _EN_TN_TIMEZONE_RE.sub(replace, text)

def _verbalize_en_tn_quarters(text: str) -> str:
    ordinal_words = {"1": "first", "2": "second", "3": "third", "4": "fourth"}

    def replace(match: re.Match[str]) -> str:
        quarter = match.group(1) or match.group(4)
        year = match.group(2) or match.group(3)
        return f"{ordinal_words[quarter]} quarter {_format_en_year_value(int(year))}"

    return _EN_TN_QUARTER_RE.sub(replace, text)

def _verbalize_en_tn_fiscal_years(text: str) -> str:
    return _EN_TN_FISCAL_YEAR_RE.sub(
        lambda match: f"fiscal year {_format_en_year_value(int(match.group(1)))}",
        text,
    )

def _verbalize_en_tn_file_tokens(text: str) -> str:
    return _EN_TN_FILE_CONTEXT_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2))}",
        text,
    )

def _verbalize_en_tn_complex_urls(text: str) -> str:
    return _EN_TN_COMPLEX_URL_RE.sub(lambda match: _verbalize_en_url_token(match.group(0)), text)

def _verbalize_en_tn_simple_urls(text: str) -> str:
    return _EN_TN_SIMPLE_URL_RE.sub(lambda match: _verbalize_en_url_token(match.group(0)), text)

def _verbalize_en_tn_emails(text: str) -> str:
    return _EN_TN_EMAIL_RE.sub(lambda match: _verbalize_en_email_token(match.group(0)), text)

def _verbalize_en_tn_structured_tokens(text: str) -> str:
    prepared = _EN_TN_ISO_DATETIME_RE.sub(lambda match: _verbalize_en_electronic_token(match.group(1)), text)
    prepared = _EN_TN_SPACE_DATETIME_RE.sub(
        lambda match: (
            f"{_verbalize_en_electronic_token(match.group(1))} "
            f"{_verbalize_en_electronic_token(match.group(2))}"
        ),
        prepared,
    )
    prepared = _EN_TN_HTTP_STATUS_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2))}",
        prepared,
    )
    return _EN_TN_PORT_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2))}",
        prepared,
    )

def _verbalize_en_tn_shortcuts(text: str) -> str:
    return _EN_TN_SHORTCUT_RE.sub(lambda match: _verbalize_en_shortcut(match.group(1)), text)

def _verbalize_en_tn_clock_time_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start_hour = int(match.group(1))
        start_minute = int(match.group(2))
        end_hour = int(match.group(3))
        end_minute = int(match.group(4))
        if start_hour > 23 or end_hour > 23:
            return match.group(0)
        return (
            f"{_format_en_tn_clock_time(start_hour, start_minute)} to "
            f"{_format_en_tn_clock_time(end_hour, end_minute)}"
        )

    return _EN_TN_CLOCK_TIME_RANGE_RE.sub(replace, text)

def _verbalize_en_tn_clock_times(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = int(match.group(1))
        minute = int(match.group(2))
        if hour > 23:
            return match.group(0)
        suffix = f" {match.group(3).replace('.', '').upper()}" if match.group(3) else ""
        sentence_period = ""
        if match.group(3) and match.group(3).endswith("."):
            following = text[match.end() :]
            if not following or re.match(r"\s+[A-Z]", following):
                sentence_period = "."
        return f"{_format_en_tn_clock_time(hour, minute, suffix)}{sentence_period}"

    return _EN_TN_CLOCK_TIME_RE.sub(replace, text)

def _format_en_tn_clock_time(hour: int, minute: int, suffix: str = "") -> str:
    hour_text = _format_en_under_100(hour)
    if minute == 0:
        return f"{hour_text}{suffix}" if suffix else f"{hour_text} o'clock"
    minute_text = f"oh {_format_en_under_100(minute)}" if minute < 10 else _format_en_under_100(minute)
    return f"{hour_text} {minute_text}{suffix}"

def _verbalize_en_shortcut(shortcut: str) -> str:
    return " plus ".join(_verbalize_en_shortcut_token(token) for token in shortcut.split("+"))

def _verbalize_en_shortcut_token(token: str) -> str:
    normalized = token.lower()
    modifier_words = {
        "ctrl": "control",
        "control": "control",
        "cmd": "command",
        "command": "command",
        "shift": "shift",
        "alt": "alt",
        "option": "option",
        "meta": "meta",
        "win": "windows",
        "windows": "windows",
        "fn": "function",
        "esc": "escape",
        "tab": "tab",
        "enter": "enter",
        "return": "return",
        "space": "space",
        "delete": "delete",
        "del": "delete",
        "backspace": "backspace",
    }
    if normalized in modifier_words:
        return modifier_words[normalized]
    if re.fullmatch(r"f\d{1,2}", token, re.IGNORECASE):
        return f"F {_verbalize_en_electronic_token(token[1:])}"
    if len(token) == 1 and token.isdigit():
        return _verbalize_en_electronic_token(token)
    return token.upper()

def _verbalize_en_url_token(token: str) -> str:
    trailing = ""
    while token and token[-1] in ".,;:!?":
        trailing = token[-1] + trailing
        token = token[:-1]
    match = re.match(r"^(https?|ftp)://(.+)$", token, re.IGNORECASE)
    if not match:
        return _verbalize_en_electronic_token(token) + trailing
    return f"{match.group(1).upper()} colon slash slash {_verbalize_en_url_remainder(match.group(2))}{trailing}"

def _verbalize_en_url_remainder(token: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    symbol_words = {
        "/": "slash",
        "\\": "backslash",
        ".": "dot",
        "_": "underscore",
        "-": "dash",
        ":": "colon",
        "~": "tilde",
        "?": "question mark",
        "=": "equals",
        "&": "ampersand",
        "#": "hash",
        "+": "plus",
    }
    parts: list[str] = []
    index = 0
    while index < len(token):
        char = token[index]
        if char.isdigit():
            parts.append(digit_words[char])
            index += 1
            continue
        if char.isalpha():
            start = index
            while index < len(token) and token[index].isalpha():
                index += 1
            run = token[start:index]
            in_path = "/" in token[:start] and "?" not in token and "#" not in token
            if in_path and len(run) <= 2:
                parts.append(run.upper())
            else:
                parts.append(run)
            continue
        word = symbol_words.get(char)
        if word is not None:
            parts.append(word)
        index += 1
    return " ".join(parts)

def _verbalize_en_email_token(token: str) -> str:
    local, domain = token.split("@", 1)
    return f"{_verbalize_en_email_part(local)} at {_verbalize_en_email_part(domain)}"

def _verbalize_en_email_part(token: str) -> str:
    output = token
    for source, target in ((".", " dot "), ("_", " underscore "), ("-", " dash "), ("+", " plus ")):
        output = output.replace(source, target)
    return re.sub(r"\s+", " ", output).strip()

def _verbalize_en_tn_semver_tokens(text: str) -> str:
    return _EN_TN_SEMVER_RE.sub(lambda match: _verbalize_en_version_token(match.group(1)), text)

def _verbalize_en_version_token(token: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    symbol_words = {
        ".": "point",
        "-": "dash",
        "+": "plus",
    }
    parts: list[str] = []
    index = 0
    while index < len(token):
        char = token[index]
        if char.isdigit():
            parts.append(digit_words[char])
            index += 1
            continue
        if char.isalpha():
            start = index
            while index < len(token) and token[index].isalpha():
                index += 1
            run = token[start:index]
            parts.append(run if len(run) > 1 else run.lower())
            continue
        word = symbol_words.get(char)
        if word is not None:
            parts.append(word)
        index += 1
    return " ".join(parts)

def _verbalize_en_tn_technical_tokens(text: str) -> str:
    prepared = _EN_TN_IPV4_PORT_RE.sub(
        lambda match: _verbalize_en_ipv4_port(match.group(0)),
        text,
    )
    prepared = _EN_TN_IPV6_RE.sub(
        lambda match: f"{match.group(1).replace('6', ' six')}{_verbalize_en_electronic_token(match.group(2).upper())}",
        prepared,
    )
    prepared = _EN_TN_ISBN_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2).upper())}",
        prepared,
    )
    prepared = _EN_TN_DOI_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2).upper())}",
        prepared,
    )
    prepared = _EN_TN_MAC_ADDRESS_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2).upper())}",
        prepared,
    )
    prepared = _EN_TN_UUID_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_en_electronic_token(match.group(2))}",
        prepared,
    )
    return _EN_TN_HEX_COLOR_RE.sub(
        lambda match: f"{match.group(1)}hash {_verbalize_en_electronic_token(match.group(2).upper())}",
        prepared,
    )

def _verbalize_en_tn_social_tokens(text: str) -> str:
    prepared = _EN_TN_SOCIAL_HANDLE_RE.sub(
        lambda match: f"at {_verbalize_en_electronic_token(match.group(1))}",
        text,
    )
    return _EN_TN_SOCIAL_HASHTAG_RE.sub(
        lambda match: f"hash {_verbalize_en_electronic_token(match.group(1))}",
        prepared,
    )

def _verbalize_en_electronic_token(token: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    symbol_words = {
        "/": "slash",
        "\\": "backslash",
        ".": "dot",
        "_": "underscore",
        "-": "dash",
        ":": "colon",
        "~": "tilde",
        "?": "question mark",
        "=": "equals",
        "&": "ampersand",
        "#": "hash",
        "+": "plus",
    }
    parts: list[str] = []
    index = 0
    while index < len(token):
        char = token[index]
        if char.isdigit():
            parts.append(digit_words[char])
            index += 1
            continue
        if char.isalpha():
            start = index
            while index < len(token) and token[index].isalpha():
                index += 1
            run = token[start:index]
            after_extension_dot = start > 0 and token[start - 1] == "."
            if len(run) == 1 or run.isupper() or (after_extension_dot and len(run) <= 4):
                parts.extend(run)
            else:
                parts.append(run)
            continue
        if char == "." and index > 0 and index + 1 < len(token) and token[index - 1].isdigit() and token[index + 1].isdigit():
            parts.append("point")
        elif char in symbol_words:
            parts.append(symbol_words[char])
        index += 1
    return " ".join(parts)

def _verbalize_en_ipv4_port(endpoint: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    address, port = endpoint.split(":", 1)
    address_words = " dot ".join(" ".join(digit_words[char] for char in octet) for octet in address.split("."))
    port_words = " ".join(digit_words[char] for char in port)
    return f"{address_words} colon {port_words}"

def _verbalize_en_tn_ipv4_addresses(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def replace(match: re.Match[str]) -> str:
        return " dot ".join(" ".join(digit_words[char] for char in octet) for octet in match.group(0).split("."))

    return _EN_TN_IPV4_RE.sub(replace, text)

def _verbalize_en_tn_zip_codes(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def replace(match: re.Match[str]) -> str:
        primary = " ".join(digit_words[char] for char in match.group(2))
        suffix = f" dash {' '.join(digit_words[char] for char in match.group(3))}" if match.group(3) else ""
        return f"{match.group(1).lower()}{primary}{suffix}"

    return _EN_TN_ZIP_CODE_RE.sub(replace, text)

def _verbalize_en_tn_room_codes(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def replace(match: re.Match[str]) -> str:
        parts = []
        for char in match.group(2):
            if char.isdigit():
                parts.append(digit_words[char])
            elif char.isalpha():
                parts.append(char.upper())
            elif char == "-":
                parts.append("dash")
        return f"{match.group(1)}{' '.join(parts)}"

    return _EN_TN_ROOM_CODE_RE.sub(replace, text)

def _verbalize_en_ascii_domains(text: str) -> str:
    return _ASCII_DOMAIN_RE.sub(lambda match: _verbalize_en_ascii_domain_token(match.group(0)), text)

def _verbalize_en_tn_context_codes(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def replace(match: re.Match[str]) -> str:
        parts = []
        for char in match.group(2):
            if char.isalpha():
                parts.append(char.upper())
            elif char.isdigit():
                parts.append(digit_words[char])
            elif char == "-":
                parts.append("dash")
        return f"{match.group(1)}{' '.join(parts)}"

    return _EN_TN_CONTEXT_CODE_RE.sub(replace, text)

def _verbalize_en_ascii_domain_token(token: str) -> str:
    trailing = ""
    while token and token[-1] in ".,;:!?":
        trailing = token[-1] + trailing
        token = token[:-1]
    output = token
    replacements = (
        (".", " dot "),
        ("/", " slash "),
        ("-", " dash "),
        ("_", " underscore "),
    )
    for source, target in replacements:
        output = output.replace(source, target)
    return re.sub(r"\s+", " ", output).strip() + trailing

def _verbalize_en_tn_negative_currency(text: str) -> str:
    return _EN_TN_NEGATIVE_CURRENCY_RE.sub(r"minus \1\2", text)

def _verbalize_en_tn_positive_percent(text: str) -> str:
    return _EN_TN_POSITIVE_PERCENT_RE.sub(r"plus \1 percent", text)

def _verbalize_en_tn_percent_ranges(text: str) -> str:
    return _EN_TN_PERCENT_RANGE_RE.sub(r"\1 to \2 percent", text)

def _verbalize_en_tn_per_mille(text: str) -> str:
    return _EN_TN_PER_MILLE_RE.sub(r"\1 per mille", text)

def _verbalize_en_tn_percentage_points(text: str) -> str:
    return _EN_TN_PERCENT_POINT_RE.sub(r"\1 percentage points", text)

def _verbalize_en_tn_scientific_notation(text: str) -> str:
    def exponent_words(exponent: str) -> str:
        if exponent.startswith("-"):
            return f"minus {exponent[1:]}"
        if exponent.startswith("+"):
            return exponent[1:]
        return exponent

    def replace_power(match: re.Match[str]) -> str:
        unit = " meters per second" if match.group(3) else ""
        return f"{match.group(1)} times 10 to the {exponent_words(match.group(2))}{unit}"

    prepared = _EN_TN_SCIENTIFIC_POWER_RE.sub(replace_power, text)
    return _EN_TN_SCIENTIFIC_E_RE.sub(
        lambda match: f"{match.group(1)} times 10 to the {exponent_words(match.group(2))}",
        prepared,
    )

def _verbalize_en_tn_coordinates(text: str) -> str:
    direction_words = {"n": "north", "s": "south", "e": "east", "w": "west"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_en_coordinate_value(match.group(1))} degrees {direction_words[match.group(2).lower()]}"

    return _EN_TN_COORDINATE_RE.sub(replace, text)

def _verbalize_en_tn_context_hash_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = match.group(2)
        if len(value) >= 4:
            return f"{match.group(1)}number {_verbalize_en_digit_sequence(value)}"
        return f"{match.group(1)}number {value}"

    return _EN_TN_CONTEXT_HASH_NUMBER_RE.sub(replace, text)

def _verbalize_en_tn_context_number_labels(text: str) -> str:
    label_words = {
        "ch": "chapter",
        "chap": "chapter",
        "chapter": "chapter",
        "sec": "section",
        "section": "section",
        "fig": "figure",
        "figure": "figure",
        "eq": "equation",
        "equation": "equation",
        "no": "number",
    }

    return _EN_TN_CONTEXT_NUMBER_LABEL_RE.sub(
        lambda match: f"{label_words[match.group(1).lower()]} {match.group(2)}",
        text,
    )

def _verbalize_en_tn_context_long_digits(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def replace(match: re.Match[str]) -> str:
        digits = [digit_words[char] for char in match.group(2) if char.isdigit()]
        return f"{match.group(1)}{' '.join(digits)}"

    return _EN_TN_CONTEXT_LONG_DIGITS_RE.sub(replace, text)

def _verbalize_en_tn_context_phone_numbers(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    def verbalize_group(value: str) -> str:
        if value == "800":
            return "eight hundred"
        return " ".join(digit_words[char] for char in value)

    def replace(match: re.Match[str]) -> str:
        country = match.group(2) or ""
        country_words = ""
        if country:
            country_words = "plus one " if country.strip().startswith("+") else "one "
        return (
            f"{match.group(1)}{country_words}{verbalize_group(match.group(3))} "
            f"{' '.join(digit_words[char] for char in match.group(4))} "
            f"{' '.join(digit_words[char] for char in match.group(5))}"
        )

    return _EN_TN_CONTEXT_PHONE_RE.sub(replace, text)

def _verbalize_en_tn_extensions(text: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }

    return _EN_TN_EXTENSION_RE.sub(
        lambda match: f"extension {' '.join(digit_words[char] for char in match.group(1))}",
        text,
    )

def _verbalize_en_tn_number_abbreviations(text: str) -> str:
    return _EN_TN_NUMBER_ABBREVIATION_RE.sub(r"number \1", text)

def _verbalize_en_tn_airline_codes(text: str) -> str:
    return _EN_TN_AIRLINE_CODE_RE.sub(lambda match: f"{match.group(1)} {_format_en_code_number_value(match.group(2))}", text)

def _verbalize_en_tn_comparisons(text: str) -> str:
    operator_words = {
        "!=": "not equal to",
        "≠": "not equal to",
        ">=": "greater than or equal to",
        "≥": "greater than or equal to",
        "≤": "less than or equal to",
        "<=": "less than or equal to",
        "≈": "approximately equal to",
        ">": "greater than",
        "<": "less than",
        "=": "equals",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {operator_words[match.group(2)]} {match.group(3)}"

    return _EN_TN_COMPARISON_RE.sub(replace, text)

def _verbalize_en_tn_plus_minus(text: str) -> str:
    temperature_units = {
        "°C": "degrees Celsius",
        "℃": "degrees Celsius",
        "C": "degrees Celsius",
        "°F": "degrees Fahrenheit",
        "℉": "degrees Fahrenheit",
        "F": "degrees Fahrenheit",
    }
    prepared = _EN_TN_PLUS_MINUS_TEMPERATURE_RE.sub(
        lambda match: f"plus or minus {match.group(1)} {temperature_units[match.group(2)]}",
        text,
    )
    return _EN_TN_PLUS_MINUS_RE.sub(r"plus or minus \1", prepared)

def _verbalize_en_tn_math_expressions(text: str) -> str:
    operator_words = {
        "+": "plus",
        "＋": "plus",
        "-": "minus",
        "−": "minus",
        "×": "times",
        "x": "times",
        "X": "times",
        "*": "times",
        "÷": "divided by",
        "/": "divided by",
    }

    def replace(match: re.Match[str]) -> str:
        return (
            f"{match.group(1)} {operator_words[match.group(2)]} "
            f"{match.group(3)} equals {match.group(4)}"
        )

    return _EN_TN_MATH_EXPR_RE.sub(replace, text)

def _verbalize_en_tn_numeric_ranges(text: str) -> str:
    return _EN_TN_NUMERIC_RANGE_RE.sub(r"\1 to \2", text)

def _verbalize_en_tn_numeric_ratios(text: str) -> str:
    return _EN_TN_NUMERIC_RATIO_RE.sub(r"\1\2 to \3", text)

def _verbalize_en_tn_dimensions(text: str) -> str:
    return _EN_TN_DIMENSION_RE.sub(
        lambda match: (
            f"{_format_en_dimension_value(match.group(1))} by {_format_en_dimension_value(match.group(2))}"
            f"{f' {_en_tn_unit_label(match.group(2), match.group(3))}' if match.group(3) else ''}"
        ),
        text,
    )

def _verbalize_en_tn_dotted_versions(text: str) -> str:
    prepared = _EN_TN_CONTEXT_DOTTED_VERSION_RE.sub(
        lambda match: f"{match.group(1)} {_verbalize_en_dotted_version(match.group(2))}",
        text,
    )
    return _EN_TN_LETTER_DOTTED_VERSION_RE.sub(
        lambda match: f"{match.group(1)} {_verbalize_en_dotted_version(match.group(2))}",
        prepared,
    )

def _verbalize_en_dotted_version(version: str) -> str:
    return " point ".join(version.split("."))

def _verbalize_en_tn_measure_units(text: str) -> str:
    prepared = _verbalize_en_tn_compact_unit_ranges(text)
    prepared = _verbalize_en_tn_context_abbreviated_numbers(prepared)
    prepared = _verbalize_en_tn_square_unit_words(prepared)
    prepared = _verbalize_en_tn_square_meter_symbols(prepared)
    prepared = _verbalize_en_tn_power_symbol_units(prepared)
    prepared = _verbalize_en_tn_basis_points(prepared)
    prepared = _verbalize_en_tn_science_ratio_units(prepared)
    prepared = _verbalize_en_tn_micro_simple_units(prepared)
    prepared = _verbalize_en_tn_engineering_units(prepared)
    prepared = _verbalize_en_tn_per_power_units(prepared)
    prepared = _verbalize_en_tn_electrical_units(prepared)
    prepared = _verbalize_en_tn_acceleration_units(prepared)
    prepared = _verbalize_en_tn_liter_per_minute(prepared)
    prepared = _verbalize_en_tn_revolutions_per_minute(prepared)
    prepared = _verbalize_en_tn_bytes_per_second(prepared)
    prepared = _EN_TN_FRAMES_PER_SECOND_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'frame')} per second",
        prepared,
    )
    prepared = _EN_TN_COMPACT_DURATION_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_tn_unit_label(match.group(1), match.group(2))}",
        prepared,
    )
    prepared = _EN_TN_DEGREE_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'degree')}",
        prepared,
    )
    prepared = _EN_TN_MILES_PER_HOUR_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'mile')} per hour",
        prepared,
    )
    prepared = _verbalize_en_tn_compact_imperial_units(prepared)
    prepared = _EN_TN_KILOMETER_PER_HOUR_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'kilometer')} per hour",
        prepared,
    )
    prepared = _EN_TN_METER_PER_SECOND_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'meter')} per second",
        prepared,
    )
    return _EN_TN_SIMPLE_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_tn_unit_label(match.group(1), match.group(2))}",
        prepared,
    )

def _verbalize_en_tn_square_meter_symbols(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _normalize_decimal_text(match.group(1).replace(",", ""))
        return f"{value} {_en_unit_word(value, 'square meter')}"

    return _EN_TN_SQUARE_METER_SYMBOL_RE.sub(replace, text)

def _verbalize_en_tn_power_symbol_units(text: str) -> str:
    unit_words = {
        "m": "meter",
        "cm": "centimeter",
        "mm": "millimeter",
        "km": "kilometer",
        "yd": "yard",
        "ft": "foot",
        "in": "inch",
    }
    power_words = {"2": "square", "²": "square", "3": "cubic", "³": "cubic"}

    def replace(match: re.Match[str]) -> str:
        value = _normalize_decimal_text(match.group(1).replace(",", ""))
        unit = f"{power_words[match.group(3)]} {unit_words[match.group(2).lower()]}"
        return f"{value} {_en_unit_word(value, unit)}"

    return _EN_TN_POWER_SYMBOL_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_square_unit_words(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _normalize_decimal_text(match.group(1).replace(",", ""))
        unit = match.group(2) or match.group(3)
        return f"{value} {_en_square_unit_word(value, unit)}"

    return _EN_TN_SQUARE_UNIT_WORD_RE.sub(replace, text)

def _en_square_unit_word(value: str, unit: str) -> str:
    normalized = unit.lower()
    labels = {
        "m": ("square meter", "square meters"),
        "meter": ("square meter", "square meters"),
        "meters": ("square meter", "square meters"),
        "km": ("square kilometer", "square kilometers"),
        "kilometer": ("square kilometer", "square kilometers"),
        "kilometers": ("square kilometer", "square kilometers"),
        "cm": ("square centimeter", "square centimeters"),
        "centimeter": ("square centimeter", "square centimeters"),
        "centimeters": ("square centimeter", "square centimeters"),
        "mm": ("square millimeter", "square millimeters"),
        "millimeter": ("square millimeter", "square millimeters"),
        "millimeters": ("square millimeter", "square millimeters"),
        "ft": ("square foot", "square feet"),
        "foot": ("square foot", "square feet"),
        "feet": ("square foot", "square feet"),
        "in": ("square inch", "square inches"),
        "inch": ("square inch", "square inches"),
        "inches": ("square inch", "square inches"),
        "yd": ("square yard", "square yards"),
        "yard": ("square yard", "square yards"),
        "yards": ("square yard", "square yards"),
    }
    singular, plural = labels[normalized]
    try:
        return singular if Decimal(value) == 1 else plural
    except InvalidOperation:
        return plural

def _verbalize_en_tn_compact_unit_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        unit = _en_tn_unit_label(match.group(2), match.group(3))
        return f"{match.group(1)} to {match.group(2)} {unit}"

    return _EN_TN_COMPACT_UNIT_RANGE_RE.sub(replace, text)

def _verbalize_en_tn_context_abbreviated_numbers(text: str) -> str:
    scale_words = {"k": "thousand", "m": "million", "b": "billion"}

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)} {scale_words[match.group(3).lower()]}"

    return _EN_TN_CONTEXT_ABBREVIATED_NUMBER_RE.sub(replace, text)

def _verbalize_en_tn_basis_points(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {_en_unit_word(match.group(1), 'basis point')}"

    return _EN_TN_BASIS_POINT_RE.sub(replace, text)

def _verbalize_en_tn_science_ratio_units(text: str) -> str:
    numerator_units = {
        "mmol": "millimole",
        "mol": "mole",
        "ug": "microgram",
        "µg": "microgram",
        "μg": "microgram",
        "mcg": "microgram",
        "ng": "nanogram",
        "mg": "milligram",
        "g": "gram",
        "iu": "international unit",
        "u": "unit",
    }
    denominator_units = {
        "l": "liter",
        "dl": "deciliter",
        "kg": "kilogram",
        "ml": "milliliter",
        "ul": "microliter",
        "µl": "microliter",
        "μl": "microliter",
    }

    def replace(match: re.Match[str]) -> str:
        numerator = _en_unit_word(match.group(1), numerator_units[match.group(2).lower()])
        denominator = denominator_units[match.group(3).lower()]
        return f"{match.group(1)} {numerator} per {denominator}"

    return _EN_TN_SCIENCE_RATIO_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_micro_simple_units(text: str) -> str:
    unit_words = {
        "ul": "microliter",
        "µl": "microliter",
        "μl": "microliter",
        "ug": "microgram",
        "µg": "microgram",
        "μg": "microgram",
        "mcg": "microgram",
        "ng": "nanogram",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {_en_unit_word(match.group(1), unit_words[match.group(2).lower()])}"

    return _EN_TN_MICRO_SIMPLE_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_electrical_units(text: str) -> str:
    unit_words = {
        "mω": "megaohm",
        "kω": "kiloohm",
        "ω": "ohm",
        "kv": "kilovolt",
        "mv": "millivolt",
        "ma": "milliampere",
        "mw": "milliwatt",
        "a": "ampere",
        "w": "watt",
        "µf": "microfarad",
        "μf": "microfarad",
        "uf": "microfarad",
        "nf": "nanofarad",
        "pf": "picofarad",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {_en_unit_word(match.group(1), unit_words[match.group(2).lower()])}"

    return _EN_TN_ELECTRICAL_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_acceleration_units(text: str) -> str:
    return _EN_TN_ACCELERATION_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'meter')} per second squared",
        text,
    )

def _verbalize_en_tn_liter_per_minute(text: str) -> str:
    return _EN_TN_LITER_PER_MINUTE_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'liter')} per minute",
        text,
    )

def _verbalize_en_tn_revolutions_per_minute(text: str) -> str:
    return _EN_TN_REVOLUTIONS_PER_MINUTE_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'revolution')} per minute",
        text,
    )

def _verbalize_en_tn_engineering_units(text: str) -> str:
    prepared = _EN_TN_DECIBEL_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_tn_engineering_unit_label(match.group(1), match.group(2))}",
        text,
    )
    prepared = _EN_TN_TORQUE_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'newton meter')}",
        prepared,
    )
    prepared = _EN_TN_NEWTON_UNIT_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'newton')}",
        prepared,
    )
    return _EN_TN_MAH_RE.sub(
        lambda match: f"{match.group(1)} {_en_unit_word(match.group(1), 'milliampere hour')}",
        prepared,
    )

def _en_tn_engineering_unit_label(value: str, unit: str) -> str:
    normalized = unit.lower()
    if normalized == "dba":
        return "A-weighted decibel" if Decimal(value) == 1 else "A-weighted decibels"
    if normalized == "dbm":
        return "decibel milliwatt" if Decimal(value) == 1 else "decibel milliwatts"
    return _en_unit_word(value, "decibel")

def _verbalize_en_tn_per_power_units(text: str) -> str:
    unit_words = {"kg": "kilogram", "g": "gram", "lb": "pound", "w": "watt"}
    power_words = {"2": "square meter", "²": "square meter", "3": "cubic meter", "³": "cubic meter"}

    def replace(match: re.Match[str]) -> str:
        unit = _en_unit_word(match.group(1), unit_words[match.group(2).lower()])
        return f"{match.group(1)} {unit} per {power_words[match.group(3)]}"

    return _EN_TN_PER_POWER_UNIT_RE.sub(replace, text)

def _verbalize_en_tn_bytes_per_second(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {_en_tn_unit_label(match.group(1), match.group(2))} per second"

    return _EN_TN_BYTES_PER_SECOND_RE.sub(replace, text)

def _verbalize_en_tn_compact_imperial_units(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {_en_tn_unit_label(match.group(1), match.group(2))}"

    return _EN_TN_COMPACT_IMPERIAL_UNIT_RE.sub(replace, text)

def _en_tn_unit_label(value: str, unit: str) -> str:
    normalized = unit.lower()
    if normalized == "gib":
        return _en_unit_word(value, "gibibyte")
    if normalized == "mib":
        return _en_unit_word(value, "mebibyte")
    if normalized == "kib":
        return _en_unit_word(value, "kibibyte")
    if normalized == "kwh":
        return _en_unit_word(value, "kilowatt hour")
    if normalized == "kw":
        return _en_unit_word(value, "kilowatt")
    if normalized == "ppm":
        return "part per million" if Decimal(value) == 1 else "parts per million"
    if normalized == "ppb":
        return "part per billion" if Decimal(value) == 1 else "parts per billion"
    if normalized == "mmhg":
        return "millimeter of mercury" if Decimal(value) == 1 else "millimeters of mercury"
    if normalized == "kpa":
        return _en_unit_word(value, "kilopascal")
    if normalized == "mpa":
        return _en_unit_word(value, "megapascal")
    if normalized == "pa":
        return _en_unit_word(value, "pascal")
    if normalized == "ghz":
        return "gigahertz"
    if normalized == "mhz":
        return "megahertz"
    if normalized == "khz":
        return "kilohertz"
    if normalized == "hz":
        return "hertz"
    if normalized == "gb":
        return _en_unit_word(value, "gigabyte")
    if normalized == "tb":
        return _en_unit_word(value, "terabyte")
    if normalized == "mb":
        return _en_unit_word(value, "megabyte")
    if normalized == "kb":
        return _en_unit_word(value, "kilobyte")
    if normalized == "ml":
        return _en_unit_word(value, "milliliter")
    if normalized == "ma":
        return _en_unit_word(value, "milliampere")
    if normalized == "ms":
        return _en_unit_word(value, "millisecond")
    if normalized == "cm":
        return _en_unit_word(value, "centimeter")
    if normalized == "mm":
        return _en_unit_word(value, "millimeter")
    if normalized == "km":
        return _en_unit_word(value, "kilometer")
    if normalized == "kg":
        return _en_unit_word(value, "kilogram")
    if normalized == "mg":
        return _en_unit_word(value, "milligram")
    if normalized == "g":
        return _en_unit_word(value, "gram")
    if normalized == "h":
        return _en_unit_word(value, "hour")
    if normalized == "min":
        return _en_unit_word(value, "minute")
    if normalized == "s":
        return _en_unit_word(value, "second")
    if normalized == "ft":
        return _en_unit_word(value, "foot")
    if normalized == "in":
        return _en_unit_word(value, "inch")
    if normalized == "lb":
        return _en_unit_word(value, "pound")
    if normalized == "oz":
        return _en_unit_word(value, "ounce")
    if normalized == "mi":
        return _en_unit_word(value, "mile")
    if normalized == "yd":
        return _en_unit_word(value, "yard")
    if normalized == "l":
        return _en_unit_word(value, "liter")
    if normalized == "v":
        return _en_unit_word(value, "volt")
    if normalized == "k":
        return "kelvin"
    return _en_unit_word(value, "meter")

def _en_unit_word(value: str, singular: str) -> str:
    try:
        number = Decimal(value)
    except InvalidOperation:
        number = Decimal(0)
    if number == 1:
        return singular
    irregular_plurals = {"foot": "feet", "inch": "inches"}
    return irregular_plurals.get(singular, f"{singular}s")

def _verbalize_en_tn_remaining_numbers(text: str) -> str:
    prepared = _verbalize_en_tn_phone_plus_numbers(text)
    prepared = _verbalize_en_tn_iso_dates(prepared)
    prepared = _verbalize_en_tn_month_date_years(prepared)
    prepared = _verbalize_en_tn_symbol_money_amounts(prepared)
    prepared = _verbalize_en_tn_symbol_temperatures(prepared)
    prepared = _verbalize_en_tn_fractions(prepared)
    prepared = _EN_TN_NEGATIVE_PERCENT_RE.sub(
        lambda match: f"minus {_format_en_number_value(match.group(1))} percent",
        prepared,
    )
    prepared = _EN_TN_UNSIGNED_PERCENT_RE.sub(
        lambda match: f"{_format_en_number_value(match.group(1))} percent",
        prepared,
    )
    return _EN_TN_REMAINING_NUMBER_RE.sub(_replace_en_tn_remaining_number, prepared)

def _verbalize_en_tn_phone_plus_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        country = _format_en_integer_value(int(match.group(2)))
        number = _verbalize_en_digit_sequence(match.group(3))
        return f"{match.group(1)}plus {country} {number}"

    return _EN_TN_PHONE_PLUS_RE.sub(replace, text)

def _verbalize_en_tn_iso_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{_en_month_name(month).lower()} {_format_en_ordinal_value(day)} {_format_en_year_value(year)}"

    return _EN_TN_ISO_DATE_RE.sub(replace, text)

def _verbalize_en_tn_month_date_years(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        raw_day = match.group(2)
        day = _format_en_ordinal_value(int(raw_day)) if raw_day.isdigit() else raw_day
        if day is None:
            return match.group(0)
        return f"{match.group(1)} {day} {_format_en_year_value(int(match.group(3)))}"

    return _EN_TN_MONTH_DATE_YEAR_RE.sub(replace, text)

def _verbalize_en_tn_symbol_money_amounts(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        sign = "minus " if match.group(1) else ""
        return sign + _format_en_money_amount(match.group(2), match.group(3))

    return _EN_TN_SYMBOL_MONEY_AMOUNT_RE.sub(replace, text)

def _verbalize_en_tn_symbol_temperatures(text: str) -> str:
    unit_words = {
        "°c": "degrees Celsius",
        "℃": "degrees Celsius",
        "c": "degrees Celsius",
        "°f": "degrees Fahrenheit",
        "℉": "degrees Fahrenheit",
        "f": "degrees Fahrenheit",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{_format_en_number_value(match.group(1))} {unit_words[match.group(2).lower()]}"

    return _EN_TN_SYMBOL_TEMPERATURE_RE.sub(replace, text)

def _verbalize_en_tn_fractions(text: str) -> str:
    denominator_words = {
        2: ("half", "halves"),
        3: ("third", "thirds"),
        4: ("quarter", "quarters"),
        5: ("fifth", "fifths"),
        6: ("sixth", "sixths"),
        7: ("seventh", "sevenths"),
        8: ("eighth", "eighths"),
        9: ("ninth", "ninths"),
        10: ("tenth", "tenths"),
    }

    def replace(match: re.Match[str]) -> str:
        numerator = int(match.group(1))
        denominator = int(match.group(2))
        words = denominator_words.get(denominator)
        if words is None:
            return match.group(0)
        unit = words[0] if numerator == 1 else words[1]
        return f"{_format_en_integer_value(numerator)} {unit}"

    return _EN_TN_FRACTION_RE.sub(replace, text)

def _replace_en_tn_remaining_number(match: re.Match[str]) -> str:
    sign = match.group(1)
    value = match.group(2)
    prefix = "minus " if sign == "-" else "plus " if sign == "+" else ""
    return prefix + _format_en_number_value(value)

def _format_en_money_amount(symbol: str, amount: str) -> str:
    currency_words = {
        "$": ("dollar", "cent"),
        "€": ("euro", "cent"),
        "£": ("pound", "pence"),
        "¥": ("yen", ""),
        "HK$": ("Hong Kong dollar", "cent"),
    }
    major_unit, minor_unit = currency_words[symbol]
    normalized = amount.replace(",", "")
    integer_text, _, fraction_text = normalized.partition(".")
    major = int(integer_text or "0")
    major_words = f"{_format_en_integer_value(major)} {_plural_en_currency_unit(major, major_unit)}"
    if not fraction_text or not minor_unit:
        return major_words
    fraction = (fraction_text + "00")[:2]
    minor = int(fraction)
    if minor == 0:
        return major_words
    return f"{major_words} {_format_en_integer_value(minor)} {_plural_en_currency_unit(minor, minor_unit)}"

def _plural_en_currency_unit(value: int, singular: str) -> str:
    if singular == "yen":
        return "yen"
    if value == 1:
        return singular
    if singular == "pence":
        return "pence"
    return f"{singular}s"

def _format_en_number_value(value: str) -> str:
    normalized = value.replace(",", "")
    if "." not in normalized:
        return _format_en_integer_value(int(normalized))
    integer_text, fraction_text = normalized.split(".", 1)
    integer = _format_en_integer_value(int(integer_text or "0"))
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    fraction = " ".join(digit_words[char] for char in fraction_text)
    return f"{integer} point {fraction}"

def _verbalize_en_digit_sequence(value: str) -> str:
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    return " ".join(digit_words[char] for char in value)

def _format_en_coordinate_value(value: str) -> str:
    normalized = value.replace(",", "")
    integer_text, dot, fraction_text = normalized.partition(".")
    integer = int(integer_text)
    if 100 <= integer <= 199:
        integer_words = f"one {_format_en_under_100(integer - 100)}"
    else:
        integer_words = _format_en_integer_value(integer)
    if not dot:
        return integer_words
    digit_words = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    return f"{integer_words} point {' '.join(digit_words[char] for char in fraction_text)}"

def _format_en_dimension_value(value: str) -> str:
    normalized = value.replace(",", "")
    if "." in normalized:
        return _format_en_number_value(normalized)
    integer = int(normalized)
    if 1000 <= integer <= 9999:
        high, low = divmod(integer, 100)
        if low == 0:
            return f"{_format_en_under_100(high)} hundred"
        return f"{_format_en_under_100(high)} {_format_en_under_100(low)}"
    return _format_en_integer_value(integer)

def _format_en_year_value(value: int) -> str:
    if 1900 <= value <= 2099:
        high, low = divmod(value, 100)
        if low == 0:
            return f"{_format_en_under_100(high)} hundred"
        return f"{_format_en_under_100(high)} {_format_en_under_100(low)}"
    return _format_en_integer_value(value)

def _format_en_integer_value(value: int) -> str:
    if value < 0:
        return f"minus {_format_en_integer_value(-value)}"
    if value < 100:
        return _format_en_under_100(value)
    if value < 1000:
        hundreds, remainder = divmod(value, 100)
        output = f"{_format_en_under_100(hundreds)} hundred"
        if remainder:
            output += f" and {_format_en_under_100(remainder)}"
        return output
    if value < 1_000_000:
        thousands, remainder = divmod(value, 1000)
        output = f"{_format_en_integer_value(thousands)} thousand"
        if remainder:
            output += f" {_format_en_integer_value(remainder)}"
        return output
    millions, remainder = divmod(value, 1_000_000)
    output = f"{_format_en_integer_value(millions)} million"
    if remainder:
        output += f" {_format_en_integer_value(remainder)}"
    return output

def _format_en_code_number_value(value: str) -> str:
    number = int(value)
    if 100 <= number <= 999:
        hundreds, remainder = divmod(number, 100)
        if remainder:
            return f"{_format_en_under_100(hundreds)} hundred {_format_en_under_100(remainder)}"
    return _format_en_integer_value(number)

def _en_month_name(month: int) -> str:
    return {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }[month]

def _format_en_under_100(value: int) -> str:
    ones = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
    }
    tens = {
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }
    if value < 20:
        return ones[value]
    ten, one = divmod(value, 10)
    if one == 0:
        return tens[ten * 10]
    return f"{tens[ten * 10]} {ones[one]}"

def _format_en_ordinal_value(value: int) -> str | None:
    if not 1 <= value <= 99:
        return None
    direct = {
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "sixth",
        7: "seventh",
        8: "eighth",
        9: "ninth",
        10: "tenth",
        11: "eleventh",
        12: "twelfth",
        13: "thirteenth",
        14: "fourteenth",
        15: "fifteenth",
        16: "sixteenth",
        17: "seventeenth",
        18: "eighteenth",
        19: "nineteenth",
        20: "twentieth",
        30: "thirtieth",
        40: "fortieth",
        50: "fiftieth",
        60: "sixtieth",
        70: "seventieth",
        80: "eightieth",
        90: "ninetieth",
    }
    if value in direct:
        return direct[value]
    ten, one = divmod(value, 10)
    return f"{_format_en_under_100(ten * 10)} {direct[one]}"

def _space_en_tn_letter_decimal_versions(text: str) -> str:
    return _EN_TN_LETTER_DECIMAL_VERSION_RE.sub(r"\1 \2", text)

def prepare_input(text: str) -> str:
    return _prepare_en_tn_input(text)
