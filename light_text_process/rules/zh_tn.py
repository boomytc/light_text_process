from __future__ import annotations
import re
from collections.abc import Callable


_TN_PROMOTION_MINUS_RE = re.compile(r"(满)(\d+(?:\.\d+)?)(减)(\d+(?:\.\d+)?)")

_MONEY_CONTEXT = r"(?:金额|余额|价格|售价|费用|花费|成本|预算|收入|营收|押金|定金|工资|薪资|月薪|年薪|零钱|找零|我有|还有)"

_TN_DECIMAL_YUAN_MONEY_RE = re.compile(
    rf"((?:{_MONEY_CONTEXT}|人民币)?\s*)(\d[\d,]*\.\d{{1,2}})\s*(元|块)"
)

_SIGNED_DIGIT_TEMPERATURE_RE = re.compile(
    r"(?<![A-Za-z0-9.])([+-])\s*(\d+(?:\.\d+)?)\s*(摄氏度|华氏度|℃|°C|℉|°F|度)"
)

_TN_PERCENT_RANGE_RE = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*%\s*[-~～–—]\s*(\d+(?:\.\d+)?)\s*%")

_TN_TEMPERATURE_RANGE_RE = re.compile(
    r"((?:温度|气温|室温|体温|体感|水温|油温)\s*)"
    r"([-+]?\d+(?:\.\d+)?)\s*[-~～–—]\s*([-+]?\d+(?:\.\d+)?)\s*"
    r"(摄氏度|华氏度|℃|°C|℉|°F|度)"
)

_TN_DEGREE_VALUE_RE = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*度")

_TN_CONTEXT_NO_NUMBER_RE = re.compile(r"((?:编号|序号|单号|号码)\s*)No\.\s*(\d+)", re.IGNORECASE)

_TN_NUMERIC_RATING_RE = re.compile(r"((?:评分|得分|分数|打分))\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)")

_TN_YUAN_PER_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*元\s*/\s*(斤|公斤|千克|kg|KG|克|g)")

_TN_SPEED_PER_HOUR_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(公里|千米|km|KM)\s*/\s*(小时|时|h)")

_WEEKDAY_RANGE_RE = re.compile(
    r"((周|星期|礼拜)[一二三四五六日天])\s*[-~～–—]\s*((?:(周|星期|礼拜))?[一二三四五六日天])"
)

_DATE_RANGE_SEPARATOR_RE = re.compile(
    r"(\d{4}年\d{1,2}月\d{1,2}[日号])\s*[-~～–—]\s*(\d{4}年\d{1,2}月\d{1,2}[日号])"
)

def verbalize_decimal_yuan_money(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{format_decimal_yuan_amount(match.group(2), match.group(3), format_number=format_number)}"

    return _TN_DECIMAL_YUAN_MONEY_RE.sub(replace, text)

def format_decimal_yuan_amount(
    amount: str,
    unit: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    normalized = amount.replace(",", "")
    if "." not in normalized:
        return f"{format_number(normalized)}{unit}"
    major, raw_fraction = normalized.split(".", 1)
    fraction = raw_fraction.ljust(2, "0")[:2]
    major_text = format_number(major)
    if fraction == "00":
        return f"{major_text}{unit}"

    jiao, fen = fraction
    major_is_zero = int(major or "0") == 0
    parts = [] if major_is_zero else [f"{major_text}{unit}"]
    if jiao != "0":
        parts.append(f"{format_number(jiao)}角")
    if fen != "0":
        parts.append(f"{format_number(fen)}分")
    return "".join(parts)

def verbalize_signed_digit_temperatures(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    sign_words = {"+": "正", "-": "负"}
    unit_words = {
        "摄氏度": "摄氏度",
        "℃": "摄氏度",
        "°C": "摄氏度",
        "华氏度": "华氏度",
        "℉": "华氏度",
        "°F": "华氏度",
        "度": "度",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{sign_words[match.group(1)]}{format_number(match.group(2))}{unit_words[match.group(3)]}"

    return _SIGNED_DIGIT_TEMPERATURE_RE.sub(replace, text)

def verbalize_percent_ranges(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    return _TN_PERCENT_RANGE_RE.sub(
        lambda match: f"百分之{format_number(match.group(1))}到百分之{format_number(match.group(2))}",
        text,
    )

def verbalize_temperature_ranges(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    unit_words = {
        "摄氏度": "摄氏度",
        "℃": "摄氏度",
        "°C": "摄氏度",
        "华氏度": "华氏度",
        "℉": "华氏度",
        "°F": "华氏度",
        "度": "度",
    }

    def replace(match: re.Match[str]) -> str:
        return (
            f"{match.group(1)}{format_number(match.group(2))}到"
            f"{format_number(match.group(3))}{unit_words[match.group(4)]}"
        )

    return _TN_TEMPERATURE_RANGE_RE.sub(replace, text)

def verbalize_degree_values(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    return _TN_DEGREE_VALUE_RE.sub(lambda match: f"{format_number(match.group(1))}度", text)

def verbalize_context_no_numbers(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    return _TN_CONTEXT_NO_NUMBER_RE.sub(lambda match: f"{match.group(1)}{format_number(match.group(2))}", text)

def verbalize_numeric_ratings(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    return _TN_NUMERIC_RATING_RE.sub(
        lambda match: f"{match.group(1)}{format_number(match.group(2))}分满分{format_number(match.group(3))}分",
        text,
    )

def verbalize_yuan_per_units(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    unit_words = {"斤": "斤", "公斤": "公斤", "千克": "千克", "kg": "千克", "克": "克", "g": "克"}

    def replace(match: re.Match[str]) -> str:
        return f"{format_number(match.group(1))}元每{unit_words[match.group(2).lower()]}"

    return _TN_YUAN_PER_UNIT_RE.sub(replace, text)

def verbalize_speed_per_hour(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    unit_words = {"公里": "公里", "千米": "千米", "km": "千米"}

    def replace(match: re.Match[str]) -> str:
        return f"{format_number(match.group(1))}{unit_words[match.group(2).lower()]}每小时"

    return _TN_SPEED_PER_HOUR_RE.sub(replace, text)

def verbalize_weekday_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        prefix = match.group(2)
        end = match.group(3) if match.group(4) else f"{prefix}{match.group(3)}"
        return f"{match.group(1)}到{end}"

    return _WEEKDAY_RANGE_RE.sub(replace, text)

def verbalize_date_range_separators(text: str) -> str:
    return _DATE_RANGE_SEPARATOR_RE.sub(r"\1到\2", text)

def verbalize_promotion_minus(
    text: str,
    *,
    format_number: Callable[[str], str],
) -> str:
    return _TN_PROMOTION_MINUS_RE.sub(
        lambda match: f"{match.group(1)}{format_number(match.group(2))}{match.group(3)}{format_number(match.group(4))}",
        text,
    )

_ASCII_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

_ASCII_URL_RE = re.compile(r"\b(?:https?|ftp)://[A-Za-z0-9._~:/?#@!$&'()*+,;=%-]+")

_ASCII_IPV4_RE = re.compile(r"(?<![A-Za-z0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![A-Za-z0-9.])")

_ASCII_DOMAIN_RE = re.compile(
    r"(?<!://)(?<![@A-Za-z0-9_./-])(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}"
    r"(?:/[A-Za-z0-9._~!$&'()*+,;=%-]+)?(?![A-Za-z0-9_-])"
)

_ZH_TN_NUMERIC_DATE_RE = re.compile(r"(?<!\d)(\d{4})([-/.])(\d{1,2})\2(\d{1,2})(?!\d)")

_ZH_TN_DOT_NUMERIC_DATE_RE = re.compile(r"(?<![\d.])(\d{4})\.(\d{1,2})\.(\d{1,2})(?![A-Za-z0-9.])")

_ZH_TN_NUMERIC_YEAR_MONTH_RE = re.compile(r"(?<!\d)(\d{4})([-/.])(\d{1,2})(?!\2\d|[-/.]\d|\d)")

_ZH_TN_YEAR_MONTH_DAY_RE = re.compile(r"(?<!\d)(\d{4})年(\d{1,2})月(\d{1,2})([日号])(?!\d)")

def _normalize_decimal_text(value: str) -> str:
    if "." not in value:
        return value
    integer_text, fractional_text = value.split(".", 1)
    trimmed_fraction = fractional_text.rstrip("0")
    if not trimmed_fraction:
        return integer_text
    return f"{integer_text}.{trimmed_fraction}"

_ZH_TN_YEAR_MONTH_RE = re.compile(r"(?<!\d)(\d{4})年(\d{1,2})月(?!\d|[0-9一二两三四五六七八九十]{1,3}[日号])")

_ZH_TN_CONTEXT_COMPACT_DATE_RE = re.compile(
    r"((?:日期|时间|今天|当天|生日|截止|截至)\s*)(\d{4})(\d{2})(\d{2})(?!\d)"
)

_ZH_TN_PREFIX_CURRENCY_RE = re.compile(
    r"\b(USD|EUR|GBP|CNY|RMB|JPY|HKD)\s+(-?\d[\d,]*(?:\.\d+)?)\b",
    re.IGNORECASE,
)

_ZH_TN_YUAN_SYMBOL_MONEY_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(-?)([¥￥])\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)"
)

_ZH_TN_SYMBOL_FOREIGN_MONEY_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(-?)(HK\$|[$€£])\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)",
    re.IGNORECASE,
)

_ZH_TN_PHONE_PLUS_RE = re.compile(r"((?:电话|手机|手机号|热线)\s*)\+(\d{1,3})\s+(\d{7,})")

_ZH_TN_BLOOD_PRESSURE_RE = re.compile(r"((?:血压)\s*)(\d{2,3})/(\d{2,3})\s*mmHg\b", re.IGNORECASE)

_ZH_TN_TIMEZONE_RE = re.compile(r"\b(UTC|GMT)([+-])(\d{1,2})(?::?(\d{2}))?\b", re.IGNORECASE)

_ZH_TN_QUARTER_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:Q([1-4])\s+(\d{4})|(\d{4})\s+Q([1-4]))(?![A-Za-z0-9])",
    re.IGNORECASE,
)

_ZH_TN_FISCAL_YEAR_RE = re.compile(r"(?<![A-Za-z0-9])FY\s*(\d{4})(?![A-Za-z0-9])", re.IGNORECASE)

_ZH_TN_HTTP_STATUS_RE = re.compile(r"((?:HTTP|HTTPS)\s*)([1-5]\d{2})", re.IGNORECASE)

_ZH_TN_PORT_RE = re.compile(r"((?:端口号|端口|port)\s*)(\d{2,5})(?!\d)", re.IGNORECASE)

_ZH_TN_ISO_DATETIME_RE = re.compile(
    r"(?<![A-Za-z0-9])(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)(?![A-Za-z0-9])"
)

_ZH_TN_SPACE_DATETIME_RE = re.compile(
    r"(?<![A-Za-z0-9])(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}(?::\d{2})?)(?![A-Za-z0-9])"
)

_ZH_TN_CLOCK_TIME_RANGE_RE = re.compile(
    r"(?<![\d.:])(\d{1,2}):([0-5]\d)\s*[-~～–—]\s*(\d{1,2}):([0-5]\d)(?![:\d])"
)

_ZH_TN_CLOCK_TIME_RE = re.compile(r"(?<![\d.:])(\d{1,2}):([0-5]\d)(?![:\d])")

_ZH_SHORTCUT_MODIFIER = (
    r"(?:Ctrl|Control|Cmd|Command|Shift|Alt|Option|Meta|Win|Windows|Fn|Esc|Tab|Enter|Return|"
    r"Space|Delete|Del|Backspace)"
)

_ZH_SHORTCUT_KEY = (
    r"(?:Ctrl|Control|Cmd|Command|Shift|Alt|Option|Meta|Win|Windows|Fn|Esc|Tab|Enter|Return|"
    r"Space|Delete|Del|Backspace|F\d{1,2}|[A-Z0-9])"
)

_ZH_TN_SHORTCUT_RE = re.compile(rf"(?<![A-Za-z0-9])({_ZH_SHORTCUT_MODIFIER}(?:\+{_ZH_SHORTCUT_KEY}){{1,5}})(?![A-Za-z0-9])")

_ZH_TN_FILE_CONTEXT_RE = re.compile(r"((?:文件|文件名|路径|目录)\s*)([A-Za-z0-9_./~:\\-]+)")

_ZH_TN_SEMVER_RE = re.compile(
    r"(?<![A-Za-z0-9.])([Vv]?\d+\.\d+\.\d+(?:-[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)?(?:\+[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)?)(?![A-Za-z0-9:]|\.\d)"
)

_ZH_TN_MAC_ADDRESS_RE = re.compile(
    r"((?:MAC地址|MAC|mac地址|mac|BSSID)\s*)((?:[A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})"
)

_ZH_TN_UUID_RE = re.compile(
    r"((?:UUID|uuid)\s*)([0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12})"
)

_ZH_TN_HEX_COLOR_RE = re.compile(r"((?:颜色|色值|十六进制|背景色|前景色)\s*)#([A-Fa-f0-9]{3,8})")

_ZH_TN_IPV4_PORT_RE = re.compile(r"(?<![\w.])((?:\d{1,3}\.){3}\d{1,3}):(\d{1,5})(?![\w.])")

_ZH_TN_IPV6_RE = re.compile(r"((?:IPv6|ipv6)\s*)([0-9A-Fa-f]{1,4}(?::[0-9A-Fa-f]{0,4}){2,7})")

_ZH_TN_ISBN_RE = re.compile(r"((?:ISBN(?:-1[03])?)\s*)([0-9Xx][0-9Xx-]{8,20})")

_ZH_TN_DOI_RE = re.compile(r"((?:DOI|doi)\s*)(10\.\d{4,9}/[A-Za-z0-9._;()/:+-]*[A-Za-z0-9)])")

_ZH_TN_SOCIAL_HANDLE_RE = re.compile(r"(?<![A-Za-z0-9_.])@([A-Za-z][A-Za-z0-9_]{1,50})")

_ZH_TN_SOCIAL_HASHTAG_RE = re.compile(r"(?<![A-Za-z0-9_.])#([A-Za-z][A-Za-z0-9_]{1,60})")

_ZH_TN_SIGNED_NUMBER_RE = re.compile(r"(?<![\w.])([+-])\s*(\d+(?:\.\d+)?)(?![\w.])")

_ZH_TN_SIGNED_PERCENT_RE = re.compile(r"(?<![\w.])([+-])\s*(\d+(?:\.\d+)?)\s*%")

_ZH_TN_PLUS_MINUS_UNIT_RE = re.compile(r"±\s*(\d+(?:\.\d+)?)(°C|℃|°F|℉|mm|cm|km|m|kg|mg|g|%)", re.IGNORECASE)

_ZH_TN_PLUS_MINUS_RE = re.compile(r"±\s*(\d+(?:\.\d+)?)")

_ZH_TN_PER_MILLE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*‰")

_ZH_TN_DISCOUNT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*折")

_ZH_TN_PERCENT_POINT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(pp|ppts?)\b", re.IGNORECASE)

_ZH_TN_SCIENTIFIC_E_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)[eE]([+-]?\d+)(?![\w.])")

_ZH_TN_SCIENTIFIC_POWER_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)[xX×]10\^([+-]?\d+)(m/s)?\b",
    re.IGNORECASE,
)

_ZH_TN_COLON_DURATION_RE = re.compile(r"((?:时长|用时|耗时|持续)\s*)(\d{1,2}):(\d{2}):(\d{2})")

_ZH_TN_COMPARISON_RE = re.compile(
    r"([A-Za-z][A-Za-z0-9_]*|[\u4e00-\u9fff]{1,8})\s*(!=|≠|>=|≥|≤|<=|>|<|=|≈)\s*(-?\d+(?:\.\d+)?|[A-Za-z][A-Za-z0-9_]*)"
)

_ZH_TN_MATH_EXPR_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*([+＋\-−×xX*÷/])\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)(?!\w)"
)

_ZH_TN_HYPHENATED_DIGIT_SEQUENCE_RE = re.compile(r"(?<!\d)(\d{3,4}(?:-\d{3,4}){1,3})(?!\d)")

_ZH_TN_CONTEXT_LANDLINE_RE = re.compile(r"((?:客服电话|客服热线|电话|热线|座机)\s*)(\d{3,4})-(\d{7,8})(?!\d)")

_ZH_TN_CONTEXT_SHORT_HYPHEN_CODE_RE = re.compile(
    r"((?:车位|门牌|房号|座位)\s*)([A-Za-z]?\d+[A-Za-z]?)-(\d+(?:-\d+)*)",
    re.IGNORECASE,
)

_ZH_TN_CONTEXT_LONG_DIGITS_RE = re.compile(
    r"((?:账号|卡号|银行卡|身份证|号码|手机号|手机|客服电话|客服热线|电话|热线|座机)\s*)"
    r"((?:\d{2,4}\s+){1,}\d{2,4}|\d{8,})"
)

_ZH_TN_CONTEXT_CODE_RE = re.compile(
    r"((?:订单号|订单|发票号|发票|快递单号|单号|编号|工单|序列号|SKU)\s*)"
    r"([A-Za-z]{1,8}[A-Za-z0-9-]{2,})",
    re.IGNORECASE,
)

_ZH_TN_LICENSE_PLATE_RE = re.compile(
    r"((?:车牌号|车牌|牌照|车号)\s*)([\u4e00-\u9fff][A-Za-z][A-Za-z0-9]{4,7})",
    re.IGNORECASE,
)

_ZH_TN_ID_CODE_RE = re.compile(
    r"((?:护照号|护照|驾驶证|驾照|证件号|证件|身份证号|身份证)\s*)([A-Za-z0-9]{6,20})",
    re.IGNORECASE,
)

_ZH_TN_EXTENSION_RE = re.compile(r"(转|分机|内线)\s*(\d{1,6})")

_ZH_TN_POSTAL_CODE_RE = re.compile(r"((?:邮编|邮政编码)\s*)(\d{6})(?!\d)")

_ZH_TN_ADDRESS_CARDINAL_RE = re.compile(r"(?<!\d)(\d{1,4})(号|栋|幢|楼|层|单元)")

_ZH_TN_ROOM_NUMBER_RE = re.compile(r"(?<!\d)(\d{2,6})(室|房间|房|户)")

_ZH_TN_GENERAL_QUANTITY_RE = re.compile(
    r"(?<![A-Za-z0-9_.\-~～—–])(\d+(?:\.\d+)?)"
    r"(岁|人|个|件|次|名|位|台|辆|本|张|条|份|套|家|只|双|瓶|盒|包|颗|粒|间|门|类|组|批|项|页|行|天|周)"
)

_ZH_TN_SQUARE_METER_RE = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*(?:㎡|m²)(?![A-Za-z])")

_ZH_TN_BYTES_PER_SECOND_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(GiB|MiB|KiB|TB|GB|MB|KB)/s\b",
    re.IGNORECASE,
)

_ZH_TN_FPS_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)fps\b", re.IGNORECASE)

_ZH_TN_COMPACT_DURATION_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(h|min|s)(?![A-Za-z])", re.IGNORECASE)

_ZH_TN_DEGREE_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)deg\b", re.IGNORECASE)

_ZH_TN_SYMBOL_TEMPERATURE_RE = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*(°C|℃|°F|℉)(?![A-Za-z])")

_ZH_TN_PREFIX_TEMPERATURE_RE = re.compile(r"(摄氏|华氏)\s*(-?\d+(?:\.\d+)?)\s*度")

_ZH_TN_YUAN_PER_AREA_RE = re.compile(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*元\s*/\s*(?:㎡|m²|平方米|平米)")

_ZH_TN_KELVIN_RE = re.compile(r"((?:温度|温差|气温|体温|色温)\s*)(\d+(?:\.\d+)?)\s*K(?![A-Za-z])")

_ZH_TN_KILOHERTZ_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)kHz\b")

_ZH_TN_ACCELERATION_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)m/s(?:\^?2|²)\b", re.IGNORECASE)

_ZH_TN_LITER_PER_MINUTE_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)L/min\b", re.IGNORECASE)

_ZH_TN_REVOLUTIONS_PER_MINUTE_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)rpm\b", re.IGNORECASE)

_ZH_TN_MPH_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)mph\b", re.IGNORECASE)

_ZH_TN_IMPERIAL_UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(ft|in|lb|oz|mi)(?![A-Za-z])",
    re.IGNORECASE,
)

_ZH_TN_PER_POWER_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)(kg|g|lb|W)/m([²³23])(?![A-Za-z])",
    re.IGNORECASE,
)

_ZH_TN_DECIBEL_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(dBA|dBm|dB)\b", re.IGNORECASE)

_ZH_TN_TORQUE_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)N[·.]?m\b", re.IGNORECASE)

_ZH_TN_MAH_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)mAh\b", re.IGNORECASE)

_ZH_TN_NEWTON_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)N(?![A-Za-z·.])")

_ZH_TN_BASIS_POINT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(bp|bps)\b", re.IGNORECASE)

_ZH_TN_DIMENSION_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)[xX×](\d+(?:\.\d+)?)(cm|mm|km|m|in|ft|px)?"
    r"(?=\s*(?:cm|mm|km|m|in|ft|px|[，,。；;、\s]|$))",
    re.IGNORECASE,
)

_ZH_TN_ELECTRICAL_UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(MΩ|kΩ|Ω|kV|mV|mA|mW|A|W|µF|μF|uF|nF|pF)(?![A-Za-z])",
    re.IGNORECASE,
)

_ZH_TN_SCIENCE_RATIO_UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(mmol|mol|ug|µg|μg|mcg|ng|mg|g|IU|U)/(L|dL|kg|mL|uL|µL|μL)\b",
    re.IGNORECASE,
)

_ZH_TN_MICRO_SIMPLE_UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(uL|µL|μL|ug|µg|μg|mcg|ng)\b",
    re.IGNORECASE,
)

_ZH_TN_CONCENTRATION_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(ppm|ppb)\b", re.IGNORECASE)

_ZH_TN_PRESSURE_UNIT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(mmHg|MPa|kPa|Pa)\b", re.IGNORECASE)

_ZH_TN_NUMERIC_RANGE_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)[-~～—–](\d+(?:\.\d+)?)(?=[\u4e00-\u9fffA-Za-z])")

_ZH_TN_ALNUM_HYPHEN_CODE_RE = re.compile(r"\b([A-Za-z]+)-(\d+(?:-\d+)*)\b")

_ZH_TN_CASED_UNIT_RE = re.compile(
    r"(?<=\d)(KWh|kWh|Mbps|Kbps|GHz|MHz|kHz|KHz|Hz|GB|TB|mL|mmHg|kPa|V|MV|mV|kV|KV)(?![A-Za-z])"
)

_ZH_TN_POWER_SYMBOL_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)(m|cm|mm|km)([²³23])(?![A-Za-z])",
    re.IGNORECASE,
)

_ZH_TN_SPOKEN_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)(Mbps|Kbps|GiB|MiB|KiB|GB|TB|MB|KB|kWh|KWh|kW|KW|mL|ml|mA|ms|cm|mm|km|kg|mg|g|L|l|V|v)(?![A-Za-z])"
)

_ZH_TN_METER_PER_SECOND_RE = re.compile(r"(?<=\d)m/s\b", re.IGNORECASE)

_ZH_TN_ORDINAL_DIGIT_RE = re.compile(r"第\s*(\d{1,8})\s*(世纪|[名届次章节条段课页期])")

_ZH_TN_STANDALONE_ORDINAL_DIGIT_RE = re.compile(r"第\s*(\d{1,8})(?=[,，。；;、\s]|$)")

_ZH_TN_SPACED_YEAR_MONTH_DAY_RE = re.compile(
    r"(?<!\d)(\d{4})\s+年\s+(\d{1,2})\s+月\s+(\d{1,2})\s+([日号])"
)

_ZH_TN_COMPACT_WRITTEN_DATE_RE = re.compile(r"(?<!\d)(\d{4})年(\d{1,2})月(\d{1,2})([日号])")

_ZH_TN_UNSIGNED_PERCENT_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*%")

_ZH_TN_COORDINATE_DEGREE_RE = re.compile(r"(北纬|南纬|东经|西经)(\d+(?:\.\d+)?)°")

_ZH_TN_FRACTION_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)(?![\w.])")

_ZH_TN_CONTEXT_RATIO_RE = re.compile(r"((?:比例|比分|分数|score|Score)\s*)(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)")

_ZH_TN_CONTEXT_CLOCK_TIME_WITH_SECONDS_RE = re.compile(
    r"((?:时间|会议时间|回访时间|预约时间|通话时间)\s*)(\d{1,2}):([0-5]\d):([0-5]\d)"
)

_ZH_TN_CONTEXT_WAN_YI_RE = re.compile(
    r"((?:金额|预算|收入|营收|增长|用户|人数|播放|浏览|下载|销量)\s*)"
    r"(\d+(?:\.\d+)?)\s*(万|亿)"
)

_ZH_TN_FOREIGN_CURRENCY_SUFFIX_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(美元|欧元|英镑|日元|港元)")

_ZH_TN_WHOLE_YUAN_RE = re.compile(r"(?<![\w.])([+-]?\d+)\s*(元|块)")

_ZH_TN_REMAINING_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])([+-]?)(\d+(?:\.\d+)?)(?![A-Za-z0-9])")

def _format_zh_number_value(value: str) -> str:
    if "." not in value:
        return _format_zh_integer(int(value))
    integer_text, fractional_text = value.split(".", 1)
    digits = "零一二三四五六七八九"
    integer = _format_zh_integer(int(integer_text)) if integer_text else digits[0]
    fractional = "".join(digits[int(char)] for char in fractional_text)
    return f"{integer}点{fractional}"

def _format_zh_digit_sequence(value: str) -> str:
    digits = "零一二三四五六七八九"
    return "".join(digits[int(char)] for char in value)

def _format_zh_integer(value: int) -> str:
    if value < 0:
        return f"负{_format_zh_integer(-value)}"
    if value < 10000:
        return _format_zh_under_10000(value)
    if value < 100000000:
        return _format_zh_large_integer(value, 10000, "万")
    return _format_zh_large_integer(value, 100000000, "亿")

def _format_zh_large_integer(value: int, unit_value: int, unit_label: str) -> str:
    high, low = divmod(value, unit_value)
    output = f"{_format_zh_integer(high)}{unit_label}"
    if low:
        if low < unit_value // 10:
            output += "零"
        output += _format_zh_integer(low)
    return output

def _format_zh_under_10000(value: int) -> str:
    digits = "零一二三四五六七八九"
    if value == 0:
        return digits[0]

    parts: list[str] = []
    pending_zero = False
    remainder = value
    for unit_value, unit_label in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        digit, remainder = divmod(remainder, unit_value)
        if digit:
            if pending_zero and parts:
                parts.append(digits[0])
            pending_zero = False
            if unit_value == 10 and digit == 1 and not parts:
                parts.append(unit_label)
            else:
                parts.append(f"{digits[digit]}{unit_label}")
        elif parts and remainder:
            pending_zero = True
    return "".join(parts)

def _prepare_zh_tn_input(text: str) -> str:
    prepared = _replace_zh_tn_spaced_year_month_days(text)
    prepared = _replace_zh_tn_dot_numeric_dates(prepared)
    prepared = _verbalize_zh_ascii_electronic(prepared)
    prepared = _verbalize_zh_tn_structured_tokens(prepared)
    prepared = _replace_zh_tn_clock_time_ranges(prepared)
    prepared = _replace_zh_tn_clock_times(prepared)
    prepared = _verbalize_zh_tn_shortcuts(prepared)
    prepared = _verbalize_zh_tn_semver_tokens(prepared)
    prepared = _verbalize_zh_tn_technical_tokens(prepared)
    prepared = _verbalize_zh_tn_file_social_tokens(prepared)
    prepared = _verbalize_zh_ipv4_addresses(prepared)
    prepared = _verbalize_zh_ascii_domains(prepared)
    prepared = _replace_zh_tn_timezones(prepared)
    prepared = _replace_zh_tn_quarters(prepared)
    prepared = _replace_zh_tn_fiscal_years(prepared)
    prepared = _replace_zh_tn_identity_codes(prepared)
    prepared = _replace_zh_tn_context_codes(prepared)
    prepared = _replace_zh_tn_phone_plus_numbers(prepared)
    prepared = _replace_zh_tn_prefix_currency_codes(prepared)
    prepared = _replace_zh_tn_symbol_foreign_money(prepared)
    prepared = _replace_zh_tn_yuan_symbol_money(prepared)
    prepared = _replace_zh_tn_context_compact_dates(prepared)
    prepared = verbalize_date_range_separators(prepared)
    prepared = verbalize_weekday_ranges(prepared)
    prepared = verbalize_promotion_minus(prepared, format_number=_format_zh_number_value)
    prepared = verbalize_numeric_ratings(prepared, format_number=_format_zh_number_value)
    prepared = verbalize_yuan_per_units(prepared, format_number=_format_zh_number_value)
    prepared = verbalize_speed_per_hour(prepared, format_number=_format_zh_number_value)
    prepared = verbalize_context_no_numbers(prepared, format_number=_format_zh_number_value)
    prepared = _replace_zh_tn_context_landline_numbers(prepared)
    prepared = _replace_zh_tn_hyphenated_digit_sequences(prepared)
    prepared = _replace_zh_tn_context_long_digits(prepared)
    prepared = _replace_zh_tn_extensions(prepared)
    prepared = _replace_zh_tn_year_months(prepared)
    prepared = _replace_zh_tn_numeric_dates(prepared)
    prepared = _replace_zh_tn_address_numbers(prepared)
    prepared = _replace_zh_tn_general_quantities(prepared)
    prepared = verbalize_temperature_ranges(prepared, format_number=_format_zh_number_value)
    prepared = verbalize_percent_ranges(prepared, format_number=_format_zh_number_value)
    prepared = _replace_zh_tn_signed_percent(prepared)
    prepared = verbalize_signed_digit_temperatures(prepared, format_number=_format_zh_number_value)
    prepared = _replace_zh_tn_plus_minus(prepared)
    prepared = verbalize_degree_values(prepared, format_number=_format_zh_number_value)
    prepared = _replace_zh_tn_signed_numbers(prepared)
    prepared = _replace_zh_tn_discounts(prepared)
    prepared = _replace_zh_tn_per_mille(prepared)
    prepared = _replace_zh_tn_percentage_points(prepared)
    prepared = _replace_zh_tn_scientific_notation(prepared)
    prepared = _replace_zh_tn_colon_durations(prepared)
    prepared = _replace_zh_tn_comparisons(prepared)
    prepared = _replace_zh_tn_math_expressions(prepared)
    prepared = _replace_zh_tn_dimensions(prepared)
    prepared = _replace_zh_tn_blood_pressure(prepared)
    prepared = _normalize_zh_tn_measure_units(prepared)
    prepared = verbalize_decimal_yuan_money(prepared, format_number=_format_zh_number_value)
    prepared = _replace_zh_tn_context_short_hyphen_codes(prepared)
    prepared = _replace_zh_tn_alnum_hyphen_codes(prepared)
    prepared = _replace_zh_tn_numeric_ranges(prepared)
    prepared = _replace_zh_tn_digit_ordinals(prepared)
    return _finalize_zh_tn_native_output(prepared)

def _replace_zh_tn_spaced_year_month_days(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month = int(match.group(2))
        day = int(match.group(3))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return (
            f"{_format_zh_digit_sequence(match.group(1))} 年 "
            f"{_format_zh_integer(month)} 月 {_format_zh_digit_sequence(match.group(3))} {match.group(4)}"
        )

    return _ZH_TN_SPACED_YEAR_MONTH_DAY_RE.sub(replace, text)

def _finalize_zh_tn_native_output(text: str) -> str:
    finalized = _replace_zh_tn_compact_written_dates(text)
    finalized = _replace_zh_tn_context_clock_time_with_seconds(finalized)
    finalized = _replace_zh_tn_coordinate_degrees(finalized)
    finalized = _replace_zh_tn_context_wan_yi(finalized)
    finalized = _replace_zh_tn_foreign_currency_suffixes(finalized)
    finalized = _replace_zh_tn_whole_yuan(finalized)
    finalized = _replace_zh_tn_unsigned_percents(finalized)
    finalized = _replace_zh_tn_context_ratios(finalized)
    finalized = _replace_zh_tn_fractions(finalized)
    finalized = _replace_zh_tn_remaining_numbers(finalized)
    return finalized.replace("，", ",").replace("；", ";")

def _replace_zh_tn_compact_written_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month = int(match.group(2))
        day = int(match.group(3))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return (
            f"{_format_zh_digit_sequence(match.group(1))}年"
            f"{_format_zh_integer(month)}月{_format_zh_integer(day)}{match.group(4)}"
        )

    return _ZH_TN_COMPACT_WRITTEN_DATE_RE.sub(replace, text)

def _replace_zh_tn_context_clock_time_with_seconds(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = int(match.group(2))
        minute = int(match.group(3))
        second = int(match.group(4))
        if hour > 23:
            return match.group(0)
        return (
            f"{match.group(1)}{_format_zh_integer(hour)}点"
            f"{'零' if minute < 10 else ''}{_format_zh_integer(minute)}分"
            f"{'零' if second < 10 else ''}{_format_zh_integer(second)}秒"
        )

    return _ZH_TN_CONTEXT_CLOCK_TIME_WITH_SECONDS_RE.sub(replace, text)

def _replace_zh_tn_coordinate_degrees(text: str) -> str:
    return _ZH_TN_COORDINATE_DEGREE_RE.sub(
        lambda match: f"{match.group(1)}{_format_zh_number_value(match.group(2))}度",
        text,
    )

def _replace_zh_tn_context_wan_yi(text: str) -> str:
    return _ZH_TN_CONTEXT_WAN_YI_RE.sub(
        lambda match: f"{match.group(1)}{_format_zh_number_value(match.group(2))}{match.group(3)}",
        text,
    )

def _replace_zh_tn_foreign_currency_suffixes(text: str) -> str:
    return _ZH_TN_FOREIGN_CURRENCY_SUFFIX_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}{match.group(2)}",
        text,
    )

def _replace_zh_tn_whole_yuan(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = match.group(1)
        sign = "负" if value.startswith("-") else "正" if value.startswith("+") else ""
        return f"{sign}{_format_zh_number_value(value.lstrip('+-'))}{match.group(2)}"

    return _ZH_TN_WHOLE_YUAN_RE.sub(replace, text)

def _replace_zh_tn_unsigned_percents(text: str) -> str:
    return _ZH_TN_UNSIGNED_PERCENT_RE.sub(
        lambda match: f"百分之{_format_zh_number_value(match.group(1))}",
        text,
    )

def _replace_zh_tn_context_ratios(text: str) -> str:
    return _ZH_TN_CONTEXT_RATIO_RE.sub(
        lambda match: f"{match.group(1)}{_format_zh_number_value(match.group(2))}比{_format_zh_number_value(match.group(3))}",
        text,
    )

def _replace_zh_tn_fractions(text: str) -> str:
    return _ZH_TN_FRACTION_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(2))}分之{_format_zh_number_value(match.group(1))}",
        text,
    )

def _replace_zh_tn_remaining_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        sign = "负" if match.group(1) == "-" else "正" if match.group(1) == "+" else ""
        value = match.group(2)
        if "." not in value and len(value) >= 6:
            return sign + _format_zh_digit_sequence(value)
        return sign + _format_zh_number_value(value)

    return _ZH_TN_REMAINING_NUMBER_RE.sub(replace, text)

def _replace_zh_tn_timezones(text: str) -> str:
    sign_words = {"+": "加", "-": "减"}

    def replace(match: re.Match[str]) -> str:
        minute = f"点{match.group(4)}" if match.group(4) else ""
        return f"{match.group(1).upper()}{sign_words[match.group(2)]}{match.group(3)}{minute}"

    return _ZH_TN_TIMEZONE_RE.sub(replace, text)

def _replace_zh_tn_signed_numbers(text: str) -> str:
    sign_words = {"+": "正", "-": "负"}

    def replace(match: re.Match[str]) -> str:
        return f"{sign_words[match.group(1)]}{_format_zh_number_value(match.group(2))}"

    return _ZH_TN_SIGNED_NUMBER_RE.sub(replace, text)

def _replace_zh_tn_clock_time_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start_hour = int(match.group(1))
        start_minute = int(match.group(2))
        end_hour = int(match.group(3))
        end_minute = int(match.group(4))
        if start_hour > 23 or end_hour > 23:
            return match.group(0)
        return f"{_format_zh_tn_clock_time(start_hour, start_minute)}到{_format_zh_tn_clock_time(end_hour, end_minute)}"

    return _ZH_TN_CLOCK_TIME_RANGE_RE.sub(replace, text)

def _replace_zh_tn_clock_times(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = int(match.group(1))
        minute = int(match.group(2))
        if hour > 23:
            return match.group(0)
        return _format_zh_tn_clock_time(hour, minute)

    return _ZH_TN_CLOCK_TIME_RE.sub(replace, text)

def _format_zh_tn_clock_time(hour: int, minute: int) -> str:
    hour_text = _format_zh_integer(hour)
    if minute == 0:
        return f"{hour_text}点整"
    minute_text = f"零{_format_zh_integer(minute)}" if 0 < minute < 10 else _format_zh_integer(minute)
    return f"{hour_text}点{minute_text}分"

def _replace_zh_tn_quarters(text: str) -> str:
    quarter_words = {"1": "一", "2": "二", "3": "三", "4": "四"}

    def replace(match: re.Match[str]) -> str:
        quarter = match.group(1) or match.group(4)
        year = match.group(2) or match.group(3)
        return f"{_format_zh_digit_sequence(year)}年第{quarter_words[quarter]}季度"

    return _ZH_TN_QUARTER_RE.sub(replace, text)

def _replace_zh_tn_fiscal_years(text: str) -> str:
    return _ZH_TN_FISCAL_YEAR_RE.sub(lambda match: f"{_format_zh_digit_sequence(match.group(1))}财年", text)

def _verbalize_zh_tn_file_social_tokens(text: str) -> str:
    verbalized = _ZH_TN_FILE_CONTEXT_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2))}",
        text,
    )
    verbalized = _ZH_TN_SOCIAL_HANDLE_RE.sub(
        lambda match: f"艾特{_verbalize_zh_file_token(match.group(1))}",
        verbalized,
    )
    return _ZH_TN_SOCIAL_HASHTAG_RE.sub(
        lambda match: f"井号{_verbalize_zh_file_token(match.group(1))}",
        verbalized,
    )

def _verbalize_zh_tn_technical_tokens(text: str) -> str:
    verbalized = _ZH_TN_IPV4_PORT_RE.sub(
        lambda match: _verbalize_zh_file_token(match.group(0)),
        text,
    )
    verbalized = _ZH_TN_IPV6_RE.sub(
        lambda match: f"{match.group(1).replace('6', '六')}{_verbalize_zh_file_token(match.group(2).upper())}",
        verbalized,
    )
    verbalized = _ZH_TN_ISBN_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2).upper())}",
        verbalized,
    )
    verbalized = _ZH_TN_DOI_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2).upper())}",
        verbalized,
    )
    verbalized = _ZH_TN_MAC_ADDRESS_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2).upper())}",
        verbalized,
    )
    verbalized = _ZH_TN_UUID_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2))}",
        verbalized,
    )
    return _ZH_TN_HEX_COLOR_RE.sub(
        lambda match: f"{match.group(1)}井号{_verbalize_zh_file_token(match.group(2).upper())}",
        verbalized,
    )

def _verbalize_zh_tn_structured_tokens(text: str) -> str:
    structured = _ZH_TN_ISO_DATETIME_RE.sub(lambda match: _verbalize_zh_file_token(match.group(1)), text)
    structured = _ZH_TN_SPACE_DATETIME_RE.sub(
        lambda match: f"{_verbalize_zh_file_token(match.group(1))} {_verbalize_zh_file_token(match.group(2))}",
        structured,
    )
    structured = _ZH_TN_HTTP_STATUS_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2))}",
        structured,
    )
    return _ZH_TN_PORT_RE.sub(
        lambda match: f"{match.group(1)}{_verbalize_zh_file_token(match.group(2))}",
        structured,
    )

def _verbalize_zh_tn_shortcuts(text: str) -> str:
    return _ZH_TN_SHORTCUT_RE.sub(lambda match: _verbalize_zh_shortcut(match.group(1)), text)

def _verbalize_zh_shortcut(shortcut: str) -> str:
    return "加".join(_verbalize_zh_shortcut_token(token) for token in shortcut.split("+"))

def _verbalize_zh_shortcut_token(token: str) -> str:
    if re.fullmatch(r"F\d{1,2}", token, re.IGNORECASE):
        return f"F{_format_zh_digit_sequence(token[1:])}"
    if len(token) == 1 and token.isdigit():
        return _format_zh_digit_sequence(token)
    return token

def _verbalize_zh_tn_semver_tokens(text: str) -> str:
    return _ZH_TN_SEMVER_RE.sub(lambda match: _verbalize_zh_file_token(match.group(1)), text)

def _verbalize_zh_file_token(token: str) -> str:
    symbol_words = {
        "/": "斜杠",
        "\\": "反斜杠",
        ".": "点",
        "_": "下划线",
        "-": "杠",
        ":": "冒号",
        "~": "波浪号",
    }
    parts = []
    for char in token:
        if char.isdigit():
            parts.append(_format_zh_digit_sequence(char))
        else:
            parts.append(symbol_words.get(char, char))
    return "".join(parts)

def _replace_zh_tn_address_numbers(text: str) -> str:
    digit_map = str.maketrans("0123456789", "零一二三四五六七八九")

    def replace_postal_code(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2).translate(digit_map)}"

    def replace_room(match: re.Match[str]) -> str:
        return f"{match.group(1).translate(digit_map)}{match.group(2)}"

    def replace_cardinal(match: re.Match[str]) -> str:
        return f"{_format_zh_integer(int(match.group(1)))}{match.group(2)}"

    prepared = _ZH_TN_POSTAL_CODE_RE.sub(replace_postal_code, text)
    prepared = _ZH_TN_ROOM_NUMBER_RE.sub(replace_room, prepared)
    return _ZH_TN_ADDRESS_CARDINAL_RE.sub(replace_cardinal, prepared)

def _replace_zh_tn_general_quantities(text: str) -> str:
    return _ZH_TN_GENERAL_QUANTITY_RE.sub(
        lambda match: f"{_format_zh_number_value(_normalize_decimal_text(match.group(1)))}{match.group(2)}",
        text,
    )

def _replace_zh_tn_identity_codes(text: str) -> str:
    def verbalize_code(code: str) -> str:
        chars = []
        for char in code:
            if char.isdigit():
                chars.append(_format_zh_digit_sequence(char))
            elif char.isalpha():
                chars.append(char.upper())
            else:
                chars.append(char)
        return "".join(chars)

    def replace_plate(match: re.Match[str]) -> str:
        return f"{match.group(1)}{verbalize_code(match.group(2))}"

    def replace_id(match: re.Match[str]) -> str:
        return f"{match.group(1)}{verbalize_code(match.group(2))}"

    prepared = _ZH_TN_LICENSE_PLATE_RE.sub(replace_plate, text)
    return _ZH_TN_ID_CODE_RE.sub(replace_id, prepared)

def _replace_zh_tn_context_codes(text: str) -> str:
    digit_map = str.maketrans("0123456789", "零一二三四五六七八九")

    def replace(match: re.Match[str]) -> str:
        code = match.group(2).replace("-", "杠").translate(digit_map)
        return f"{match.group(1)}{code}"

    return _ZH_TN_CONTEXT_CODE_RE.sub(replace, text)

def _replace_zh_tn_phone_plus_numbers(text: str) -> str:
    digit_map = str.maketrans("0123456789", "零一二三四五六七八九")

    def replace(match: re.Match[str]) -> str:
        country = match.group(2).translate(digit_map)
        number = match.group(3).translate(digit_map)
        return f"{match.group(1)}加{country} {number}"

    return _ZH_TN_PHONE_PLUS_RE.sub(replace, text)

def _replace_zh_tn_extensions(text: str) -> str:
    digit_map = str.maketrans("0123456789", "零一二三四五六七八九")
    return _ZH_TN_EXTENSION_RE.sub(lambda match: f"{match.group(1)}{match.group(2).translate(digit_map)}", text)

def _replace_zh_tn_prefix_currency_codes(text: str) -> str:
    unit_map = {
        "usd": "美元",
        "eur": "欧元",
        "gbp": "英镑",
        "cny": "人民币",
        "rmb": "人民币",
        "jpy": "日元",
        "hkd": "港元",
    }

    def replace(match: re.Match[str]) -> str:
        amount = _normalize_decimal_text(match.group(2).replace(",", ""))
        return f"{_format_zh_number_value(amount)}{unit_map[match.group(1).lower()]}"

    return _ZH_TN_PREFIX_CURRENCY_RE.sub(replace, text)

def _replace_zh_tn_yuan_symbol_money(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        amount = _normalize_decimal_text(match.group(3).replace(",", ""))
        sign = "负" if match.group(1) else ""
        prefix = "人民币" if match.group(2) == "￥" else ""
        return sign + prefix + format_decimal_yuan_amount(amount, "元", format_number=_format_zh_number_value)

    return _ZH_TN_YUAN_SYMBOL_MONEY_RE.sub(replace, text)

def _replace_zh_tn_symbol_foreign_money(text: str) -> str:
    unit_map = {"$": "美元", "€": "欧元", "£": "英镑", "hk$": "港元"}

    def replace(match: re.Match[str]) -> str:
        amount = _normalize_decimal_text(match.group(3).replace(",", ""))
        sign = "负" if match.group(1) or amount.startswith("-") else ""
        if amount.startswith("-"):
            amount = amount[1:]
        return f"{sign}{_format_zh_number_value(amount)}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_SYMBOL_FOREIGN_MONEY_RE.sub(replace, text)

def _replace_zh_tn_context_compact_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month = int(match.group(3))
        day = int(match.group(4))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}{match.group(2)}年{month}月{day}日"

    return _ZH_TN_CONTEXT_COMPACT_DATE_RE.sub(replace, text)

def _replace_zh_tn_dot_numeric_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month = int(match.group(2))
        day = int(match.group(3))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}年{month}月{day}日"

    return _ZH_TN_DOT_NUMERIC_DATE_RE.sub(replace, text)

def _replace_zh_tn_year_months(text: str) -> str:
    def replace_numeric(match: re.Match[str]) -> str:
        month = int(match.group(3))
        if not 1 <= month <= 12:
            return match.group(0)
        return f"{_format_zh_digit_sequence(match.group(1))}年{_format_zh_integer(month)}月"

    def replace_written(match: re.Match[str]) -> str:
        month = int(match.group(2))
        if not 1 <= month <= 12:
            return match.group(0)
        return f"{_format_zh_digit_sequence(match.group(1))}年{_format_zh_integer(month)}月"

    prepared = _ZH_TN_NUMERIC_YEAR_MONTH_RE.sub(replace_numeric, text)
    return _ZH_TN_YEAR_MONTH_RE.sub(replace_written, prepared)

def _replace_zh_tn_hyphenated_digit_sequences(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return match.group(1).replace("-", "杠").translate(str.maketrans("0123456789", "零一二三四五六七八九"))

    return _ZH_TN_HYPHENATED_DIGIT_SEQUENCE_RE.sub(replace, text)

def _replace_zh_tn_context_landline_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{_format_zh_digit_sequence(match.group(2))}杠{_format_zh_digit_sequence(match.group(3))}"

    return _ZH_TN_CONTEXT_LANDLINE_RE.sub(replace, text)

def _replace_zh_tn_context_long_digits(text: str) -> str:
    digit_map = str.maketrans("0123456789", "零一二三四五六七八九")

    def replace(match: re.Match[str]) -> str:
        digits = "".join(char for char in match.group(2) if char.isdigit())
        return f"{match.group(1)}{digits.translate(digit_map)}"

    return _ZH_TN_CONTEXT_LONG_DIGITS_RE.sub(replace, text)

def _replace_zh_tn_numeric_dates(text: str) -> str:
    def replace_year_month_day(match: re.Match[str]) -> str:
        month = int(match.group(2))
        day = int(match.group(3))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{_format_zh_digit_sequence(match.group(1))}年{_format_zh_integer(month)}月{_format_zh_integer(day)}{match.group(4)}"

    def replace(match: re.Match[str]) -> str:
        year = match.group(1)
        month = int(match.group(3))
        day = int(match.group(4))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{year}年{month}月{day}日"

    prepared = _ZH_TN_YEAR_MONTH_DAY_RE.sub(replace_year_month_day, text)
    return _ZH_TN_NUMERIC_DATE_RE.sub(replace, prepared)

def _replace_zh_tn_per_mille(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"千分之{_format_zh_number_value(match.group(1))}"

    return _ZH_TN_PER_MILLE_RE.sub(replace, text)

def _replace_zh_tn_percentage_points(text: str) -> str:
    return _ZH_TN_PERCENT_POINT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}个百分点",
        text,
    )

def _replace_zh_tn_scientific_notation(text: str) -> str:
    def exponent_text(exponent: str) -> str:
        if exponent.startswith("-"):
            return f"负{_format_zh_number_value(exponent[1:])}"
        if exponent.startswith("+"):
            return _format_zh_number_value(exponent[1:])
        return _format_zh_number_value(exponent)

    def replace_power(match: re.Match[str]) -> str:
        unit = "米每秒" if match.group(3) else ""
        return (
            f"{_format_zh_number_value(match.group(1))}乘以十的"
            f"{exponent_text(match.group(2))}次方{unit}"
        )

    prepared = _ZH_TN_SCIENTIFIC_POWER_RE.sub(replace_power, text)
    return _ZH_TN_SCIENTIFIC_E_RE.sub(
        lambda match: (
            f"{_format_zh_number_value(match.group(1))}乘以十的"
            f"{exponent_text(match.group(2))}次方"
        ),
        prepared,
    )

def _replace_zh_tn_signed_percent(text: str) -> str:
    sign_words = {"+": "正", "-": "负"}

    def replace(match: re.Match[str]) -> str:
        return f"{sign_words[match.group(1)]}百分之{_format_zh_number_value(match.group(2))}"

    return _ZH_TN_SIGNED_PERCENT_RE.sub(replace, text)

def _replace_zh_tn_plus_minus(text: str) -> str:
    unit_map = {
        "°c": "摄氏度",
        "℃": "摄氏度",
        "°f": "华氏度",
        "℉": "华氏度",
        "mm": "毫米",
        "cm": "厘米",
        "km": "千米",
        "m": "米",
        "kg": "千克",
        "mg": "毫克",
        "g": "克",
        "%": "%",
    }

    def replace_unit(match: re.Match[str]) -> str:
        unit = unit_map[match.group(2).lower()]
        if unit == "%":
            return f"正负百分之{_format_zh_number_value(match.group(1))}"
        return f"正负{_format_zh_number_value(match.group(1))}{unit}"

    prepared = _ZH_TN_PLUS_MINUS_UNIT_RE.sub(replace_unit, text)
    return _ZH_TN_PLUS_MINUS_RE.sub(lambda match: f"正负{_format_zh_number_value(match.group(1))}", prepared)

def _replace_zh_tn_discounts(text: str) -> str:
    return _ZH_TN_DISCOUNT_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}折", text)

def _replace_zh_tn_colon_durations(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = int(match.group(2))
        minute = int(match.group(3))
        second = int(match.group(4))
        if minute > 59 or second > 59:
            return match.group(0)
        return f"{match.group(1)}{hour}小时{minute}分钟{second}秒"

    return _ZH_TN_COLON_DURATION_RE.sub(replace, text)

def _replace_zh_tn_comparisons(text: str) -> str:
    operator_words = {
        "!=": "不等于",
        "≠": "不等于",
        ">=": "大于等于",
        "≥": "大于等于",
        "≤": "小于等于",
        "<=": "小于等于",
        "≈": "约等于",
        ">": "大于",
        "<": "小于",
        "=": "等于",
    }

    def replace(match: re.Match[str]) -> str:
        value = match.group(3)
        verbalized_value = _format_zh_number_value(value) if re.fullmatch(r"-?\d+(?:\.\d+)?", value) else value
        return f"{match.group(1)}{operator_words[match.group(2)]}{verbalized_value}"

    return _ZH_TN_COMPARISON_RE.sub(replace, text)

def _replace_zh_tn_math_expressions(text: str) -> str:
    operator_words = {
        "+": "加",
        "＋": "加",
        "-": "减",
        "−": "减",
        "×": "乘",
        "x": "乘",
        "X": "乘",
        "*": "乘",
        "÷": "除以",
        "/": "除以",
    }

    def replace(match: re.Match[str]) -> str:
        return (
            f"{_format_zh_number_value(match.group(1))}{operator_words[match.group(2)]}"
            f"{_format_zh_number_value(match.group(3))}等于{_format_zh_number_value(match.group(4))}"
        )

    return _ZH_TN_MATH_EXPR_RE.sub(replace, text)

def _replace_zh_tn_dimensions(text: str) -> str:
    unit_map = {
        "cm": "厘米",
        "mm": "毫米",
        "km": "千米",
        "m": "米",
        "in": "英寸",
        "ft": "英尺",
        "px": "像素",
    }

    def replace(match: re.Match[str]) -> str:
        unit = unit_map.get((match.group(3) or "").lower(), "")
        return f"{_format_zh_number_value(match.group(1))}乘{_format_zh_number_value(match.group(2))}{unit}"

    return _ZH_TN_DIMENSION_RE.sub(replace, text)

def _replace_zh_tn_blood_pressure(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        systolic = _format_zh_integer(int(match.group(2)))
        diastolic = _format_zh_integer(int(match.group(3)))
        return f"{match.group(1)}{systolic}杠{diastolic}毫米汞柱"

    return _ZH_TN_BLOOD_PRESSURE_RE.sub(replace, text)

def _normalize_zh_tn_measure_units(text: str) -> str:
    prepared = _verbalize_zh_tn_bytes_per_second(text)
    prepared = _verbalize_zh_tn_frames_per_second(prepared)
    prepared = _verbalize_zh_tn_duration_units(prepared)
    prepared = _verbalize_zh_tn_yuan_per_area(prepared)
    prepared = _verbalize_zh_tn_symbol_temperatures(prepared)
    prepared = _verbalize_zh_tn_prefix_temperatures(prepared)
    prepared = _verbalize_zh_tn_kelvin(prepared)
    prepared = _verbalize_zh_tn_degrees(prepared)
    prepared = _verbalize_zh_tn_kilohertz(prepared)
    prepared = _verbalize_zh_tn_acceleration_units(prepared)
    prepared = _verbalize_zh_tn_liter_per_minute(prepared)
    prepared = _verbalize_zh_tn_revolutions_per_minute(prepared)
    prepared = _verbalize_zh_tn_miles_per_hour(prepared)
    prepared = _verbalize_zh_tn_imperial_units(prepared)
    prepared = _verbalize_zh_tn_basis_points(prepared)
    prepared = _verbalize_zh_tn_science_ratio_units(prepared)
    prepared = _verbalize_zh_tn_micro_simple_units(prepared)
    prepared = _verbalize_zh_tn_engineering_units(prepared)
    prepared = _verbalize_zh_tn_concentration_units(prepared)
    prepared = _verbalize_zh_tn_pressure_units(prepared)
    prepared = _verbalize_zh_tn_per_power_units(prepared)
    prepared = _verbalize_zh_tn_power_symbol_units(prepared)
    prepared = _verbalize_zh_tn_electrical_units(prepared)
    prepared = _verbalize_zh_tn_square_meters(prepared)
    prepared = _verbalize_zh_tn_spoken_units(prepared)
    return _ZH_TN_METER_PER_SECOND_RE.sub("米每秒", prepared)

def _verbalize_zh_tn_bytes_per_second(text: str) -> str:
    unit_map = {
        "tb": "太字节每秒",
        "gb": "吉字节每秒",
        "mb": "兆字节每秒",
        "kb": "千字节每秒",
        "gib": "吉比字节每秒",
        "mib": "兆比字节每秒",
        "kib": "千比字节每秒",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_BYTES_PER_SECOND_RE.sub(replace, text)

def _verbalize_zh_tn_frames_per_second(text: str) -> str:
    return _ZH_TN_FPS_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}帧每秒", text)

def _verbalize_zh_tn_duration_units(text: str) -> str:
    unit_map = {"h": "小时", "min": "分钟", "s": "秒"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_COMPACT_DURATION_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_yuan_per_area(text: str) -> str:
    return _ZH_TN_YUAN_PER_AREA_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}元每平方米", text)

def _verbalize_zh_tn_degrees(text: str) -> str:
    return _ZH_TN_DEGREE_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}度", text)

def _verbalize_zh_tn_symbol_temperatures(text: str) -> str:
    unit_map = {"°C": "摄氏度", "℃": "摄氏度", "°F": "华氏度", "℉": "华氏度"}
    return _ZH_TN_SYMBOL_TEMPERATURE_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2)]}",
        text,
    )

def _verbalize_zh_tn_prefix_temperatures(text: str) -> str:
    return _ZH_TN_PREFIX_TEMPERATURE_RE.sub(
        lambda match: f"{match.group(1)}{_format_zh_number_value(match.group(2))}度",
        text,
    )

def _verbalize_zh_tn_kelvin(text: str) -> str:
    return _ZH_TN_KELVIN_RE.sub(
        lambda match: f"{match.group(1)}{_format_zh_number_value(match.group(2))}开尔文",
        text,
    )

def _verbalize_zh_tn_kilohertz(text: str) -> str:
    return _ZH_TN_KILOHERTZ_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}千赫兹", text)

def _verbalize_zh_tn_acceleration_units(text: str) -> str:
    return _ZH_TN_ACCELERATION_UNIT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}米每二次方秒",
        text,
    )

def _verbalize_zh_tn_liter_per_minute(text: str) -> str:
    return _ZH_TN_LITER_PER_MINUTE_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}升每分钟",
        text,
    )

def _verbalize_zh_tn_revolutions_per_minute(text: str) -> str:
    return _ZH_TN_REVOLUTIONS_PER_MINUTE_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}转每分",
        text,
    )

def _verbalize_zh_tn_miles_per_hour(text: str) -> str:
    return _ZH_TN_MPH_RE.sub(lambda match: f"{_format_zh_number_value(match.group(1))}英里每小时", text)

def _verbalize_zh_tn_imperial_units(text: str) -> str:
    unit_map = {"ft": "英尺", "in": "英寸", "lb": "磅", "oz": "盎司", "mi": "英里"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_IMPERIAL_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_basis_points(text: str) -> str:
    return _ZH_TN_BASIS_POINT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}个基点",
        text,
    )

def _verbalize_zh_tn_science_ratio_units(text: str) -> str:
    numerator_units = {
        "mmol": "毫摩尔",
        "mol": "摩尔",
        "ug": "微克",
        "µg": "微克",
        "μg": "微克",
        "mcg": "微克",
        "ng": "纳克",
        "mg": "毫克",
        "g": "克",
        "iu": "国际单位",
        "u": "单位",
    }
    denominator_units = {
        "l": "升",
        "dl": "分升",
        "kg": "千克",
        "ml": "毫升",
        "ul": "微升",
        "µl": "微升",
        "μl": "微升",
    }

    def replace(match: re.Match[str]) -> str:
        return (
            f"{_format_zh_number_value(match.group(1))}"
            f"{numerator_units[match.group(2).lower()]}每{denominator_units[match.group(3).lower()]}"
        )

    return _ZH_TN_SCIENCE_RATIO_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_micro_simple_units(text: str) -> str:
    unit_map = {
        "ul": "微升",
        "µl": "微升",
        "μl": "微升",
        "ug": "微克",
        "µg": "微克",
        "μg": "微克",
        "mcg": "微克",
        "ng": "纳克",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_MICRO_SIMPLE_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_electrical_units(text: str) -> str:
    unit_map = {
        "mω": "兆欧姆",
        "kω": "千欧姆",
        "ω": "欧姆",
        "kv": "千伏",
        "mv": "毫伏",
        "ma": "毫安",
        "mw": "毫瓦",
        "a": "安",
        "w": "瓦",
        "µf": "微法",
        "μf": "微法",
        "uf": "微法",
        "nf": "纳法",
        "pf": "皮法",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_ELECTRICAL_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_engineering_units(text: str) -> str:
    decibel_units = {"dba": "A计权分贝", "dbm": "分贝毫瓦", "db": "分贝"}
    prepared = _ZH_TN_DECIBEL_UNIT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}{decibel_units[match.group(2).lower()]}",
        text,
    )
    prepared = _ZH_TN_TORQUE_UNIT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}牛米",
        prepared,
    )
    prepared = _ZH_TN_NEWTON_UNIT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}牛顿",
        prepared,
    )
    return _ZH_TN_MAH_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}毫安时",
        prepared,
    )

def _verbalize_zh_tn_concentration_units(text: str) -> str:
    return _ZH_TN_CONCENTRATION_UNIT_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}{match.group(2).lower()}",
        text,
    )

def _verbalize_zh_tn_pressure_units(text: str) -> str:
    unit_map = {"mmhg": "毫米汞柱", "mpa": "兆帕", "kpa": "千帕", "pa": "帕"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_PRESSURE_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_per_power_units(text: str) -> str:
    unit_map = {"kg": "千克", "g": "克", "lb": "磅", "w": "瓦"}
    power_map = {"2": "平方米", "²": "平方米", "3": "立方米", "³": "立方米"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}每{power_map[match.group(3)]}"

    return _ZH_TN_PER_POWER_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_square_meters(text: str) -> str:
    return _ZH_TN_SQUARE_METER_RE.sub(
        lambda match: f"{_format_zh_number_value(match.group(1))}平方米",
        text,
    )

def _verbalize_zh_tn_spoken_units(text: str) -> str:
    unit_map = {
        "mbps": "兆比特每秒",
        "kbps": "千比特每秒",
        "gib": "吉比字节",
        "mib": "兆比字节",
        "kib": "千比字节",
        "gb": "吉字节",
        "tb": "太字节",
        "mb": "兆字节",
        "kb": "千字节",
        "kwh": "千瓦时",
        "kw": "千瓦",
        "ml": "毫升",
        "ma": "毫安",
        "ms": "毫秒",
        "cm": "厘米",
        "mm": "毫米",
        "km": "千米",
        "kg": "千克",
        "mg": "毫克",
        "g": "克",
        "l": "升",
        "v": "伏特",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_SPOKEN_UNIT_RE.sub(replace, text)

def _verbalize_zh_tn_power_symbol_units(text: str) -> str:
    unit_map = {"m": "米", "cm": "厘米", "mm": "毫米", "km": "千米"}
    power_map = {"2": "平方", "²": "平方", "3": "立方", "³": "立方"}

    def replace(match: re.Match[str]) -> str:
        return f"{_format_zh_number_value(match.group(1))}{power_map[match.group(3)]}{unit_map[match.group(2).lower()]}"

    return _ZH_TN_POWER_SYMBOL_UNIT_RE.sub(replace, text)

def _replace_zh_tn_numeric_ranges(text: str) -> str:
    return _ZH_TN_NUMERIC_RANGE_RE.sub(r"\1到\2", text)

def _replace_zh_tn_alnum_hyphen_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        parts = [_format_zh_digit_sequence(part) for part in match.group(2).split("-")]
        return f"{match.group(1)}杠{'杠'.join(parts)}"

    return _ZH_TN_ALNUM_HYPHEN_CODE_RE.sub(replace, text)

def _replace_zh_tn_context_short_hyphen_codes(text: str) -> str:
    def verbalize(value: str) -> str:
        output = []
        for char in value:
            if char.isdigit():
                output.append(_format_zh_digit_sequence(char))
            else:
                output.append(char.upper() if char.isalpha() else char)
        return "".join(output)

    def replace(match: re.Match[str]) -> str:
        parts = [verbalize(match.group(2))]
        parts.extend(verbalize(part) for part in match.group(3).split("-"))
        return f"{match.group(1)}{'杠'.join(parts)}"

    return _ZH_TN_CONTEXT_SHORT_HYPHEN_CODE_RE.sub(replace, text)

def _verbalize_zh_ascii_electronic(text: str) -> str:
    verbalized = _ASCII_URL_RE.sub(lambda match: _verbalize_zh_ascii_electronic_token(match.group(0)), text)
    return _ASCII_EMAIL_RE.sub(lambda match: _verbalize_zh_ascii_electronic_token(match.group(0)), verbalized)

def _verbalize_zh_ascii_domains(text: str) -> str:
    return _ASCII_DOMAIN_RE.sub(lambda match: _verbalize_zh_ascii_electronic_token(match.group(0)), text)

def _verbalize_zh_ipv4_addresses(text: str) -> str:
    return _ASCII_IPV4_RE.sub(lambda match: _verbalize_zh_ipv4_address(match.group(0)), text)

def _verbalize_zh_ipv4_address(address: str) -> str:
    digit_names = "零一二三四五六七八九"
    return "".join("点" if char == "." else digit_names[int(char)] for char in address)

def _verbalize_zh_ascii_electronic_token(token: str) -> str:
    replacements = (
        ("://", "冒号斜杠斜杠"),
        ("@", "艾特"),
        (".", "点"),
        ("/", "斜杠"),
        ("-", "杠"),
        ("_", "下划线"),
        ("?", "问号"),
        ("=", "等于"),
        ("&", "与"),
        ("#", "井号"),
        ("+", "加"),
        (":", "冒号"),
    )
    output = token
    for source, target in replacements:
        output = output.replace(source, target)
    return "".join(_format_zh_digit_sequence(char) if char.isdigit() else char for char in output)

def _replace_zh_tn_digit_ordinals(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"第{_format_zh_integer(int(match.group(1)))}{match.group(2)}"

    replaced = _ZH_TN_ORDINAL_DIGIT_RE.sub(replace, text)
    return _ZH_TN_STANDALONE_ORDINAL_DIGIT_RE.sub(
        lambda match: f"第{_format_zh_integer(int(match.group(1)))}",
        replaced,
    )

def prepare_input(text: str) -> str:
    return _prepare_zh_tn_input(text)
