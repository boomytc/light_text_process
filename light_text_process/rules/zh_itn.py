from __future__ import annotations
import re
from collections.abc import Callable


_NUMBER_READING = r"[零〇一二两三四五六七八九十百千万亿兆点]+"

_INTEGER_READING = r"[零〇一二两三四五六七八九十百千万亿兆]+"

_NUMBER_READING_LAZY = r"[零〇一二两三四五六七八九十百千万亿兆点]+?"

_SCORE_DECIMAL_RE = re.compile(rf"((?:评分|得分|分数|打分))({_NUMBER_READING})分(?!之)")

_PROMOTION_MINUS_RE = re.compile(rf"(满)({_NUMBER_READING})(减)({_NUMBER_READING})")

_BUY_GET_RE = re.compile(rf"(买)({_NUMBER_READING})(送)({_NUMBER_READING})")

_COLLOQUIAL_TIME_RE = re.compile(
    rf"(凌晨|早上|上午|中午|下午|傍晚|晚上|夜里)?({_NUMBER_READING})点(半|一刻|三刻)"
)

_DAYPART_TIME_RE = re.compile(
    rf"(凌晨|早上|上午|中午|下午|傍晚|晚上|夜里)\s*({_NUMBER_READING})点"
    rf"(?:(半|一刻|三刻|{_NUMBER_READING})分?)?"
)

_HALF_QUANTITY_UNIT = (
    r"小时|分钟|秒|天|周|个月|月|年|公里|千米|米|厘米|毫米|千克|公斤|克|斤|吨|"
    r"升|毫升|英里|英尺|英寸|磅|元|块"
)

_LEADING_HALF_QUANTITY_RE = re.compile(rf"半({_HALF_QUANTITY_UNIT})")

_MIDDLE_HALF_QUANTITY_RE = re.compile(rf"({_NUMBER_READING_LAZY})个?半({_HALF_QUANTITY_UNIT})")

_TRAILING_HALF_QUANTITY_RE = re.compile(rf"({_NUMBER_READING_LAZY})({_HALF_QUANTITY_UNIT})半")

_MONEY_CONTEXT = r"(?:金额|余额|价格|售价|费用|花费|成本|预算|收入|营收|押金|定金|工资|薪资|月薪|年薪|零钱|找零|我有|还有)"

_DIGIT_READING = r"[零〇一二两三四五六七八九]"

_EXACT_MONEY_RE = re.compile(rf"((?:{_MONEY_CONTEXT}|人民币)?)({_NUMBER_READING})(元|块)整")

_COLLOQUIAL_WAN_YI_MONEY_RE = re.compile(rf"({_MONEY_CONTEXT})({_NUMBER_READING_LAZY})(万|亿)({_DIGIT_READING})")

_COLLOQUIAL_KUAI_MONEY_RE = re.compile(rf"({_MONEY_CONTEXT})({_NUMBER_READING})块({_DIGIT_READING})(?![角毛分])")

_CONTEXT_JIAO_MONEY_RE = re.compile(rf"({_MONEY_CONTEXT})({_DIGIT_READING})(?:角|毛)(?!{_DIGIT_READING}?分)")

_COLLOQUIAL_KUAI_FEN_MONEY_RE = re.compile(rf"({_MONEY_CONTEXT})({_NUMBER_READING})块零({_DIGIT_READING})")

_COLLOQUIAL_MAO_FEN_MONEY_RE = re.compile(
    rf"(?<![元块])({_MONEY_CONTEXT})?({_DIGIT_READING})(?:角|毛)({_DIGIT_READING})(?!分)"
)

_BARE_JIAO_MONEY_RE = re.compile(rf"({_DIGIT_READING})(?:角|毛)钱")

_BARE_FEN_MONEY_RE = re.compile(rf"({_DIGIT_READING})分钱")

_CENTURY_RE = re.compile(rf"第?({_INTEGER_READING})世纪")

_ZERO_BELOW_TEMPERATURE_RE = re.compile(rf"零下({_NUMBER_READING})(摄氏度|华氏度|度|℃|°C|℉|°F)")

_READING_OR_DIGIT = rf"(?:\d+(?:\.\d+)?|{_NUMBER_READING})"

_SIGNED_READING_OR_DIGIT = rf"(?:-?\d+(?:\.\d+)?|(?:负|零下)?{_NUMBER_READING})"

_SPOKEN_PERCENT_RANGE_SHORT_RE = re.compile(rf"百分之?({_READING_OR_DIGIT})(?:到|至)({_READING_OR_DIGIT})")

_SPOKEN_TEMPERATURE_RANGE_RE = re.compile(
    rf"((?:温度|气温|室温|体温|体感|水温|油温)\s*)"
    rf"({_SIGNED_READING_OR_DIGIT})(?:到|至)({_SIGNED_READING_OR_DIGIT})(摄氏度|华氏度|℃|°C|℉|°F|度)"
)

_SPOKEN_RATING_RE = re.compile(rf"((?:评分|得分|分数|打分))({_READING_OR_DIGIT})分?满分({_READING_OR_DIGIT})分")

_SPOKEN_YUAN_PER_UNIT_RE = re.compile(rf"({_READING_OR_DIGIT})元每(斤|公斤|千克|克)")

_SPOKEN_SPEED_PER_HOUR_RE = re.compile(rf"({_READING_OR_DIGIT})(公里|千米)每(?:小时|时)")

_SHORT_MINUTE_SECOND_DURATION_RE = re.compile(rf"({_READING_OR_DIGIT})分({_READING_OR_DIGIT})秒")

_SHORT_MINUTE_DURATION_RE = re.compile(rf"({_READING_OR_DIGIT})分(?=\d+s)")

_NUMERIC_PERCENT_RE = re.compile(r"(正|负)?百分之(\d+(?:\.\d+)?)")

_DATA_RATE_RE = re.compile(
    rf"({_READING_OR_DIGIT})(太字节每秒|吉字节每秒|兆字节每秒|千字节每秒|兆比特每秒|千比特每秒)"
)

_SPOKEN_WEEKDAY_RANGE_RE = re.compile(
    r"((周|星期|礼拜)[一二三四五六日天])到((?:(周|星期|礼拜))?[一二三四五六日天])"
)

_NUMERIC_DATE_RANGE_RE = re.compile(r"(\d{4}年\d{2}月\d{2}日)\s*到\s*(\d{4}年\d{2}月\d{2}日)")

_SPOKEN_ONE_DIGIT_CONTEXT_RE = re.compile(
    r"((?:电话|手机|手机号|热线|客服|座机|号码|账号|卡号|银行卡|身份证|邮编|邮政编码|端口号|端口|"
    r"转|分机|内线|编号|订单号|订单|工单|单号|快递单号|车牌号|车牌|房号|座位|车位)\s*)"
    r"([A-Za-z零〇一二三四五六七八九幺杠加\s]{2,})"
)

_SPOKEN_PUNCTUATION_RE = re.compile(
    r"左书名号|右书名号|左中括号|右中括号|左括号|右括号|左引号|右引号|"
    r"省略号|破折号|百分号|反斜杠|斜杠|空格|逗号|句号|问号|感叹号|叹号|冒号|分号|顿号"
)

_SPOKEN_PUNCTUATION = {
    "逗号": "，",
    "句号": "。",
    "问号": "？",
    "感叹号": "！",
    "叹号": "！",
    "冒号": "：",
    "分号": "；",
    "顿号": "、",
    "反斜杠": "\\",
    "斜杠": "/",
    "破折号": "—",
    "省略号": "……",
    "百分号": "%",
    "空格": " ",
    "左括号": "（",
    "右括号": "）",
    "左中括号": "【",
    "右中括号": "】",
    "左书名号": "《",
    "右书名号": "》",
    "左引号": "“",
    "右引号": "”",
}

_ASR_LEADING_FILLER_RE = re.compile(r"(?m)^\s*(?:嗯|呃|额|啊|那个|就是|这个|然后)+")

_ASR_TRAILING_FILLER_RE = re.compile(r"(?m)(?:啊|呀|哈|呢|嗯|呃|额)+\s*$")

_DECIMAL_TEMP_UNIT_READING = r"摄氏度|华氏度|度"

_DECIMAL_DIGIT_READING = r"[零〇一二三四五六七八九]"

_DECIMAL_TEMP_READING_RE = re.compile(
    rf"(零下)?({_NUMBER_READING})({_DECIMAL_TEMP_UNIT_READING})({_DECIMAL_DIGIT_READING})"
)

_DECIMAL_LENGTH_UNITS = r"米|公里|千米|厘米|毫米|英尺|英寸|英里"

_DECIMAL_LENGTH_READING_RE = re.compile(
    rf"({_NUMBER_READING})({_DECIMAL_LENGTH_UNITS})({_DECIMAL_DIGIT_READING}{{1,2}})"
)

_DECIMAL_WEIGHT_UNITS = r"公斤|千克|斤|磅|克|吨"

_DECIMAL_WEIGHT_READING_RE = re.compile(
    rf"({_NUMBER_READING})({_DECIMAL_WEIGHT_UNITS})({_DECIMAL_DIGIT_READING})"
)

def remove_asr_fillers(text: str) -> str:
    normalized = _ASR_LEADING_FILLER_RE.sub("", text)
    return _ASR_TRAILING_FILLER_RE.sub("", normalized)

def normalize_decimal_temperatures(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_map = {
        "摄氏度": "°C",
        "华氏度": "°F",
        "度": "°C",
    }

    def replace(match: re.Match[str]) -> str:
        sign = "-" if match.group(1) else ""
        value = parse_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        unit = unit_map[match.group(3)]
        digit_map = {"零": "0", "〇": "0", "一": "1", "二": "2", "三": "3", "四": "4",
                     "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
        decimal_digit = digit_map.get(match.group(4))
        if decimal_digit is None:
            return match.group(0)
        return f"{sign}{value}.{decimal_digit}{unit}"

    return _DECIMAL_TEMP_READING_RE.sub(replace, text)

def normalize_decimal_lengths(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_map = {
        "米": "m",
        "公里": "km",
        "千米": "km",
        "厘米": "cm",
        "毫米": "mm",
        "英尺": "ft",
        "英寸": "in",
        "英里": "mi",
    }

    def replace(match: re.Match[str]) -> str:
        value = parse_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        digit_map = {"零": "0", "〇": "0", "一": "1", "二": "2", "三": "3", "四": "4",
                     "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
        decimal_str = "".join(digit_map.get(ch, ch) for ch in match.group(3))
        if not decimal_str:
            return match.group(0)
        return f"{value}.{decimal_str}{unit_map[match.group(2)]}"

    return _DECIMAL_LENGTH_READING_RE.sub(replace, text)

def normalize_decimal_weights(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_map = {
        "公斤": "kg",
        "千克": "kg",
        "斤": "jin",
        "磅": "lb",
        "克": "g",
        "吨": "t",
    }

    def replace(match: re.Match[str]) -> str:
        value = parse_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        digit_map = {"零": "0", "〇": "0", "一": "1", "二": "2", "三": "3", "四": "4",
                     "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
        decimal_digit = digit_map.get(match.group(3))
        if decimal_digit is None:
            return match.group(0)
        return f"{value}.{decimal_digit}{unit_map[match.group(2)]}"

    return _DECIMAL_WEIGHT_READING_RE.sub(replace, text)

def normalize_half_quantities(text: str) -> str:
    def replace_middle(match: re.Match[str]) -> str:
        return f"{match.group(1)}点五{match.group(2)}"

    def replace_trailing(match: re.Match[str]) -> str:
        return f"{match.group(1)}点五{match.group(2)}"

    normalized = _MIDDLE_HALF_QUANTITY_RE.sub(replace_middle, text)
    normalized = _TRAILING_HALF_QUANTITY_RE.sub(replace_trailing, normalized)
    return _LEADING_HALF_QUANTITY_RE.sub(r"零点五\1", normalized)

def normalize_spoken_punctuation(text: str) -> str:
    return _SPOKEN_PUNCTUATION_RE.sub(lambda match: _SPOKEN_PUNCTUATION[match.group(0)], text)

def normalize_colloquial_money(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace_exact(match: re.Match[str]) -> str:
        value = parse_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}元"

    def parse_digit(raw: str) -> int | None:
        value = parse_number_reading(raw)
        if value is None or "." in value:
            return None
        number = int(value)
        return number if 0 <= number <= 9 else None

    def replace_wan_yi(match: re.Match[str]) -> str:
        major = parse_number_reading(match.group(2))
        minor = parse_digit(match.group(4))
        if major is None or minor is None:
            return match.group(0)
        return f"{match.group(1)}{major}.{minor}{match.group(3)}元"

    def replace_kuai(match: re.Match[str]) -> str:
        major = parse_number_reading(match.group(2))
        minor = parse_digit(match.group(3))
        if major is None or minor is None:
            return match.group(0)
        return f"{match.group(1)}{major}.{minor}元"

    def replace_jiao(match: re.Match[str]) -> str:
        digit = parse_digit(match.group(2))
        if digit is None:
            return match.group(0)
        return f"{match.group(1)}0.{digit}元"

    def replace_kuai_fen(match: re.Match[str]) -> str:
        major = parse_number_reading(match.group(2))
        fen = parse_digit(match.group(3))
        if major is None or fen is None:
            return match.group(0)
        return f"{match.group(1)}{major}.0{fen}元"

    def replace_mao_fen(match: re.Match[str]) -> str:
        jiao = parse_digit(match.group(2))
        fen = parse_digit(match.group(3))
        if jiao is None or fen is None:
            return match.group(0)
        return f"{match.group(1) or ''}0.{jiao}{fen}元"

    def replace_bare_jiao(match: re.Match[str]) -> str:
        digit = parse_digit(match.group(1))
        if digit is None:
            return match.group(0)
        return f"0.{digit}元"

    def replace_bare_fen(match: re.Match[str]) -> str:
        digit = parse_digit(match.group(1))
        if digit is None:
            return match.group(0)
        return f"0.0{digit}元"

    normalized = _EXACT_MONEY_RE.sub(replace_exact, text)
    normalized = _COLLOQUIAL_WAN_YI_MONEY_RE.sub(replace_wan_yi, normalized)
    normalized = _COLLOQUIAL_KUAI_FEN_MONEY_RE.sub(replace_kuai_fen, normalized)
    normalized = _COLLOQUIAL_MAO_FEN_MONEY_RE.sub(replace_mao_fen, normalized)
    normalized = _COLLOQUIAL_KUAI_MONEY_RE.sub(replace_kuai, normalized)
    normalized = _CONTEXT_JIAO_MONEY_RE.sub(replace_jiao, normalized)
    normalized = _BARE_JIAO_MONEY_RE.sub(replace_bare_jiao, normalized)
    return _BARE_FEN_MONEY_RE.sub(replace_bare_fen, normalized)

def normalize_centuries(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        century = parse_integer(match.group(1))
        if century is None or not 1 <= century <= 99:
            return match.group(0)
        return f"{century}世纪"

    return _CENTURY_RE.sub(replace, text)

def normalize_zero_below_temperatures(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_map = {
        "摄氏度": "°C",
        "度": "°C",
        "℃": "°C",
        "°C": "°C",
        "华氏度": "°F",
        "℉": "°F",
        "°F": "°F",
    }

    def replace(match: re.Match[str]) -> str:
        value = parse_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"-{value}{unit_map[match.group(2)]}"

    return _ZERO_BELOW_TEMPERATURE_RE.sub(replace, text)

def _parse_reading_or_digit(
    raw: str,
    parse_number_reading: Callable[[str], str | None],
) -> str | None:
    if re.fullmatch(r"\d+(?:\.\d+)?", raw):
        return raw
    return parse_number_reading(raw)

def normalize_spoken_ratings(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        score = _parse_reading_or_digit(match.group(2), parse_number_reading)
        total = _parse_reading_or_digit(match.group(3), parse_number_reading)
        if score is None or total is None:
            return match.group(0)
        return f"{match.group(1)}{score}/{total}"

    return _SPOKEN_RATING_RE.sub(replace, text)

def normalize_yuan_per_units(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_symbols = {"斤": "斤", "公斤": "kg", "千克": "kg", "克": "g"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_reading_or_digit(match.group(1), parse_number_reading)
        if value is None:
            return match.group(0)
        return f"{value}元/{unit_symbols[match.group(2)]}"

    return _SPOKEN_YUAN_PER_UNIT_RE.sub(replace, text)

def normalize_speed_per_hour(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_reading_or_digit(match.group(1), parse_number_reading)
        if value is None:
            return match.group(0)
        return f"{value}km/h"

    return _SPOKEN_SPEED_PER_HOUR_RE.sub(replace, text)

def normalize_short_minute_durations(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace_minute_second(match: re.Match[str]) -> str:
        minute = _parse_reading_or_digit(match.group(1), parse_number_reading)
        second = _parse_reading_or_digit(match.group(2), parse_number_reading)
        if minute is None or second is None:
            return match.group(0)
        return f"{minute}min{second}s"

    def replace_minute(match: re.Match[str]) -> str:
        value = _parse_reading_or_digit(match.group(1), parse_number_reading)
        if value is None:
            return match.group(0)
        return f"{value}min"

    normalized = _SHORT_MINUTE_SECOND_DURATION_RE.sub(replace_minute_second, text)
    return _SHORT_MINUTE_DURATION_RE.sub(replace_minute, normalized)

def normalize_data_rates(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_symbols = {
        "太字节每秒": "TB/s",
        "吉字节每秒": "GB/s",
        "兆字节每秒": "MB/s",
        "千字节每秒": "KB/s",
        "兆比特每秒": "Mbps",
        "千比特每秒": "kbps",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_reading_or_digit(match.group(1), parse_number_reading)
        if value is None:
            return match.group(0)
        return f"{value}{unit_symbols[match.group(2)]}"

    return _DATA_RATE_RE.sub(replace, text)

def normalize_numeric_percents(text: str) -> str:
    sign_symbols = {"正": "+", "负": "-"}

    def replace(match: re.Match[str]) -> str:
        sign = sign_symbols.get(match.group(1) or "", "")
        return f"{sign}{match.group(2)}%"

    return _NUMERIC_PERCENT_RE.sub(replace, text)

def normalize_shorthand_percent_ranges(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _parse_reading_or_digit(match.group(1), parse_number_reading)
        end = _parse_reading_or_digit(match.group(2), parse_number_reading)
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end}%"

    return _SPOKEN_PERCENT_RANGE_SHORT_RE.sub(replace, text)

def normalize_temperature_ranges(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    unit_symbols = {
        "摄氏度": "°C",
        "℃": "°C",
        "°C": "°C",
        "华氏度": "°F",
        "℉": "°F",
        "°F": "°F",
        "度": "°C",
    }

    def parse_signed(raw: str) -> str | None:
        if raw.startswith("负"):
            value = _parse_reading_or_digit(raw[1:], parse_number_reading)
            return f"-{value}" if value is not None else None
        if raw.startswith("零下"):
            value = _parse_reading_or_digit(raw[2:], parse_number_reading)
            return f"-{value}" if value is not None else None
        return _parse_reading_or_digit(raw, parse_number_reading)

    def replace(match: re.Match[str]) -> str:
        start = parse_signed(match.group(2))
        end = parse_signed(match.group(3))
        if start is None or end is None:
            return match.group(0)
        return f"{match.group(1)}{start}-{end}{unit_symbols[match.group(4)]}"

    return _SPOKEN_TEMPERATURE_RANGE_RE.sub(replace, text)

def normalize_spoken_one_digit_sequences(text: str) -> str:
    return _SPOKEN_ONE_DIGIT_CONTEXT_RE.sub(lambda match: f"{match.group(1)}{match.group(2).replace('幺', '一')}", text)

def normalize_weekday_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        prefix = match.group(2)
        end = match.group(3) if match.group(4) else f"{prefix}{match.group(3)}"
        return f"{match.group(1)}-{end}"

    return _SPOKEN_WEEKDAY_RANGE_RE.sub(replace, text)

def normalize_date_range_separators(text: str) -> str:
    return _NUMERIC_DATE_RANGE_RE.sub(r"\1-\2", text)

def normalize_colloquial_times(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def adjust_hour(hour: int, daypart: str | None) -> int:
        if daypart in {"下午", "傍晚", "晚上", "夜里"} and hour < 12:
            return hour + 12
        if daypart == "中午" and hour < 11:
            return hour + 12
        if daypart == "凌晨" and hour == 12:
            return 0
        return hour

    def replace(match: re.Match[str]) -> str:
        hour = parse_integer(match.group(2))
        if hour is None or not 0 <= hour <= 24:
            return match.group(0)
        minute = {"半": 30, "一刻": 15, "三刻": 45}[match.group(3)]
        return f"{adjust_hour(hour, match.group(1)):02d}:{minute:02d}"

    return _COLLOQUIAL_TIME_RE.sub(replace, text)

def normalize_daypart_times(
    text: str,
    *,
    parse_integer: Callable[[str], int | None],
) -> str:
    def adjust_hour(hour: int, daypart: str) -> int:
        if daypart in {"凌晨", "上午", "早上"} and hour == 12:
            return 0
        if daypart in {"晚上", "夜里"} and hour == 12:
            return 0
        if daypart in {"下午", "傍晚", "晚上", "夜里"} and hour < 12:
            return hour + 12
        if daypart == "中午" and hour < 11:
            return hour + 12
        return hour

    def parse_minute(raw: str | None) -> int | None:
        if raw is None:
            return 0
        if raw == "半":
            return 30
        if raw == "一刻":
            return 15
        if raw == "三刻":
            return 45
        return parse_integer(raw)

    def replace(match: re.Match[str]) -> str:
        hour = parse_integer(match.group(2))
        minute = parse_minute(match.group(3))
        if hour is None or minute is None or not 0 <= hour <= 24 or not 0 <= minute <= 59:
            return match.group(0)
        return f"{adjust_hour(hour, match.group(1)):02d}:{minute:02d}"

    return _DAYPART_TIME_RE.sub(replace, text)

def normalize_score_decimals(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace(match: re.Match[str]) -> str:
        value = parse_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}分"

    return _SCORE_DECIMAL_RE.sub(replace, text)

def normalize_promotions(
    text: str,
    *,
    parse_number_reading: Callable[[str], str | None],
) -> str:
    def replace_minus(match: re.Match[str]) -> str:
        threshold = parse_number_reading(match.group(2))
        discount = parse_number_reading(match.group(4))
        if threshold is None or discount is None:
            return match.group(0)
        return f"{match.group(1)}{threshold}{match.group(3)}{discount}"

    def replace_buy_get(match: re.Match[str]) -> str:
        buy = parse_number_reading(match.group(2))
        get = parse_number_reading(match.group(4))
        if buy is None or get is None:
            return match.group(0)
        return f"{match.group(1)}{buy}{match.group(3)}{get}"

    normalized = _PROMOTION_MINUS_RE.sub(replace_minus, text)
    return _BUY_GET_RE.sub(replace_buy_get, normalized)

_ZH_SPOKEN_EMAIL_RE = re.compile(
    r"([A-Za-z0-9._%+\-]+(?:(?:点|加|杠|下划线)[A-Za-z0-9._%+\-]+)*)"
    r"艾特([A-Za-z0-9\-]+(?:点[A-Za-z0-9\-]+)+)"
)

def _restore_itn_format_symbol_match(match: re.Match[str]) -> str:
    symbol = chr(int(match.group(1), 16))
    return f"{symbol} " if symbol == "%" and match.group(2) else symbol

_ZH_MIXED_SPOKEN_EMAIL_RE = re.compile(
    r"([A-Za-z0-9._%+\-]+(?:(?:点|加|杠|下划线)[A-Za-z0-9._%+\-]+)*)"
    r"@([A-Za-z0-9.\-]+(?:点[A-Za-z0-9\-]+)*)"
)

_ZH_SPOKEN_URL_RE = re.compile(
    r"((?:https?|ftp)冒号斜杠斜杠[A-Za-z0-9._~?#@!$&'()*+,;=%\-"
    r"]+(?:(?:点|斜杠|杠|下划线|问号|等于|与|井号|加)[A-Za-z0-9._~?#@!$&'()*+,;=%\-]+)*)"
)

_ZH_SPOKEN_DOMAIN_RE = re.compile(
    r"([A-Za-z0-9-]+(?:点[A-Za-z0-9-]+)+(?:斜杠[A-Za-z0-9._~!$&'()*+,;=%\-]+)*)"
)

_ZH_ITN_EXACT_HOUR_RE = re.compile(r"([零〇一二两三四五六七八九十百千万]{1,4})点整")

_ZH_ITN_POSITIVE_NUMBER_READING = r"[零〇一二两三四五六七八九十百千万亿兆点]+"

_ZH_ITN_NUMBER_READING = rf"负?{_ZH_ITN_POSITIVE_NUMBER_READING}"

_ZH_ITN_CURRENCY_UNITS = "人民币|美元|欧元|英镑|日元|港元"

_ZH_ITN_MONEY_UNITS = rf"{_ZH_ITN_CURRENCY_UNITS}|块钱|元|块"

_ZH_ITN_NEGATIVE_MONEY_RE = re.compile(rf"负({_ZH_ITN_POSITIVE_NUMBER_READING})({_ZH_ITN_MONEY_UNITS})")

_ZH_ITN_NEGATIVE_PERCENT_RE = re.compile(rf"负百分之?({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_POSITIVE_PERCENT_RE = re.compile(rf"正百分之?({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_UNSIGNED_PERCENT_RE = re.compile(rf"百分之?({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_PER_MILLE_RE = re.compile(rf"千分之({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_PREFIX_TEMPERATURE_RE = re.compile(rf"(摄氏|华氏)(零下|负)?({_ZH_ITN_POSITIVE_NUMBER_READING})度")

_ZH_ITN_POSTAL_CODE_RE = re.compile(r"((?:邮编|邮政编码))([零〇一二三四五六七八九]{6})")

_ZH_ITN_CONTEXT_COMPACT_DATE_RE = re.compile(
    r"((?:日期|时间|今天|当天|生日|截止|截至))([零〇一二三四五六七八九]{4})([零〇一二三四五六七八九]{2})([零〇一二三四五六七八九]{2})"
)

_ZH_ITN_DOTTED_DATE_RE = re.compile(
    r"((?:日期|时间|今天|当天|生日|截止|截至))([零〇一二三四五六七八九]{4})点"
    r"([零〇一二两三四五六七八九十]{1,3})点([零〇一二两三四五六七八九十]{1,3})"
)

_ZH_ITN_YEAR_MONTH_DAY_RE = re.compile(
    rf"([零〇一二三四五六七八九]{{4}})年([零〇一二两三四五六七八九十]{{1,3}})月"
    rf"([零〇一二两三四五六七八九十]{{1,3}})[日号]"
)

_ZH_ITN_TIME_WITH_SECONDS_RE = re.compile(
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"([零〇一二两三四五六七八九十]{1,3})分"
    r"([零〇一二两三四五六七八九十]{1,3})秒"
)

_ZH_ITN_TIME_WITH_MINUTES_RE = re.compile(
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"([零〇一二两三四五六七八九十]{1,3})分"
    r"(?![零〇一二两三四五六七八九十]{1,3}秒)"
)

_ZH_ITN_TIME_RANGE_RE = re.compile(
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"(?:(半|[零〇一二两三四五六七八九十]{1,3})分?)?"
    r"到"
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"(?:(半|[零〇一二两三四五六七八九十]{1,3})分?)?"
)

_ZH_ITN_DAYPART_TIME_RANGE_RE = re.compile(
    r"(上午|早上|中午|下午|晚上)?"
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"(?:(半|[零〇一二两三四五六七八九十]{1,3})分?)?"
    r"到"
    r"(上午|早上|中午|下午|晚上)?"
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"(?:(半|[零〇一二两三四五六七八九十]{1,3})分?)?"
)

_ZH_ITN_WEEKDAY_TIME_RE = re.compile(r"((?:周|星期|礼拜)[一二三四五六日天])(?=[零〇一二两三四五六七八九十]{1,3}点)")

_ZH_ITN_PLUS_MINUS_RE = re.compile(
    rf"正负({_ZH_ITN_POSITIVE_NUMBER_READING})"
    r"(摄氏度|华氏度|毫米|厘米|千米|公里|米|千克|公斤|毫克|克|百分比|%)?"
)

_ZH_ITN_YUAN_JIAO_FEN_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(元|块)"
    rf"(?:(?:({_ZH_ITN_POSITIVE_NUMBER_READING})(角|毛))(?:({_ZH_ITN_POSITIVE_NUMBER_READING})分)?|"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})分)"
)

_ZH_ITN_YUAN_JIAO_BARE_FEN_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(元|块)"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(角|毛)([零〇一二三四五六七八九])(?!分)"
)

_ZH_ITN_CONTEXT_JIAO_FEN_RE = re.compile(
    rf"((?:金额|余额|价格|售价|费用|找零|零钱|钱))"
    rf"(?:(?:({_ZH_ITN_POSITIVE_NUMBER_READING})(角|毛))(?:({_ZH_ITN_POSITIVE_NUMBER_READING})分)?|"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})分)"
)

_ZH_ITN_FOREIGN_MONEY_SUBUNITS_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(美元|欧元|英镑)"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(美分|欧分|便士|分)"
)

_ZH_ASR_DIGIT_CHARS = "零〇一二三四五六七八九幺"

_ZH_ITN_PHONE_PLUS_RE = re.compile(rf"((?:电话|手机|手机号|热线))加([{_ZH_ASR_DIGIT_CHARS}]{{2,3}})([{_ZH_ASR_DIGIT_CHARS}]{{7,}})")

_ZH_ITN_BLOOD_PRESSURE_RE = re.compile(
    rf"((?:血压)\s*)({_ZH_ITN_POSITIVE_NUMBER_READING})(?:杠|比)({_ZH_ITN_POSITIVE_NUMBER_READING})(?:毫米汞柱|mmHg)",
    re.IGNORECASE,
)

_ZH_ITN_CONTEXT_HYPHEN_DIGITS_RE = re.compile(
    r"((?:电话|热线|客服|座机|号码|账号|卡号))"
    rf"([{_ZH_ASR_DIGIT_CHARS}]{{2,4}}(?:杠[{_ZH_ASR_DIGIT_CHARS}]{{2,8}})+)"
)

_ZH_ITN_CONTEXT_LONG_DIGITS_RE = re.compile(
    rf"((?:电话|手机号|账号|卡号|银行卡|身份证|号码))([{_ZH_ASR_DIGIT_CHARS}]{{7,}})"
)

_ZH_ITN_CONTEXT_GROUPED_DIGITS_RE = re.compile(
    rf"((?:账号|卡号|银行卡|身份证|号码))"
    rf"((?:[{_ZH_ASR_DIGIT_CHARS}0-9]{{2,4}}(?:\s+|空格))+[{_ZH_ASR_DIGIT_CHARS}0-9]{{2,8}})"
)

_ZH_ITN_SHORT_CONTEXT_DIGITS_RE = re.compile(
    rf"((?:工号|员工号|客服号|坐席号|尾号|后四位|末四位))([{_ZH_ASR_DIGIT_CHARS}]{{2,8}})"
)

_ZH_ITN_CONTEXT_CODE_RE = re.compile(
    r"((?:订单号|订单|发票号|发票|快递单号|单号|编号|工单|序列号|SKU))"
    r"([A-Za-z](?:\s*[A-Za-z]){0,7}(?:(?:杠)?[零〇一二两三四五六七八九十百千万亿兆]{1,})"
    r"(?:杠[零〇一二两三四五六七八九十百千万亿兆]{1,})*)"
)

_ZH_ITN_CONTEXT_HASH_CODE_RE = re.compile(
    r"((?:订单号|订单|发票号|发票|快递单号|单号|编号|工单|工单号|序列号|SKU))"
    r"([A-Za-z](?:\s*[A-Za-z]){0,7})井号([零〇一二三四五六七八九]{1,8})"
)

_ZH_ITN_CONTEXT_COLON_CODE_RE = re.compile(
    r"((?:订单号|订单|订单编号|发票号|发票|快递单号|单号|编号|工单|工单号|序列号|SKU))"
    r"([A-Za-z](?:\s*[A-Za-z]){0,7})冒号([零〇一二三四五六七八九]{1,8})"
)

_ZH_ITN_CONTEXT_UNDERSCORE_CODE_RE = re.compile(
    r"((?:订单号|订单|发票号|发票|快递单号|单号|编号|工单|工单号|序列号|SKU))"
    r"([A-Za-z](?:\s*[A-Za-z]){0,7})下划线([零〇一二三四五六七八九]{1,8})"
)

_ZH_ITN_PARAMETER_RE = re.compile(
    r"((?:参数|字段|查询参数))([A-Za-z][A-Za-z0-9_]*)等于"
    r"(.+?)(?=(?:参数|字段|查询参数|编号|工单|订单|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_LICENSE_PLATE_RE = re.compile(
    r"((?:车牌号|车牌|牌照|车号))"
    r"([\u4e00-\u9fff])\s*([A-Za-z])\s*([零〇一二三四五六七八九A-Za-z]{4,7})"
)

_ZH_ITN_ID_CODE_RE = re.compile(
    r"((?:护照号|护照|驾驶证|驾照|证件号|证件|身份证号|身份证))"
    r"([A-Za-z]?(?:\s*[零〇一二三四五六七八九A-Za-z]){6,20})"
)

_ZH_ITN_TAX_CODE_RE = re.compile(
    r"((?:统一社会信用代码|社会信用代码|纳税人识别号|税号))"
    r"([A-Za-z0-9零〇一二三四五六七八九](?:\s*[A-Za-z0-9零〇一二三四五六七八九]){7,24})"
)

_ZH_ITN_EXTENSION_RE = re.compile(rf"(转|分机|内线)([{_ZH_ASR_DIGIT_CHARS}]{{1,6}})")

_ZH_ITN_SPOKEN_COLON_TIME_RE = re.compile(
    r"((?:时间|会议时间|回访时间|预约时间|通话时间)?)([零〇一二三四五六七八九]{1,2})冒号([零〇一二三四五六七八九]{2})"
)

_ZH_ITN_ADDRESS_CARDINAL_RE = re.compile(
    r"([零〇一二两三四五六七八九十百千万]{1,8})(号|栋|幢|楼|层|单元)"
)

_ZH_ITN_ROOM_NUMBER_RE = re.compile(rf"([{_ZH_ASR_DIGIT_CHARS}]{{2,6}})(会议室|室|房间|房|户)")

_ZH_ITN_MEETING_ROOM_NUMBER_RE = re.compile(rf"(会议室)([{_ZH_ASR_DIGIT_CHARS}]{{2,6}})")

_ZH_ITN_PREFIXED_ROOM_CODE_RE = re.compile(
    rf"((?:房间号|房间|房号|会议室|座位))([A-Za-z]?)([{_ZH_ASR_DIGIT_CHARS}]{{2,6}})"
)

_ZH_ITN_DISCOUNT_RE = re.compile(rf"(?<![零〇一二两三四五六七八九十百千万亿兆点])({_ZH_ITN_POSITIVE_NUMBER_READING})折")

_ZH_ITN_MULTIPLIER_RE = re.compile(rf"({_ZH_ITN_POSITIVE_NUMBER_READING})倍")

_ZH_ITN_CONTEXT_WAN_YI_RE = re.compile(
    rf"((?:金额|预算|收入|营收|增长|用户|人数|播放|浏览|下载|销量))({_ZH_ITN_POSITIVE_NUMBER_READING})(万|亿)"
)

_ZH_ITN_PH_VALUE_RE = re.compile(rf"(pH)({_ZH_ITN_POSITIVE_NUMBER_READING})", re.IGNORECASE)

_ZH_ITN_FILE_CONTEXT_RE = re.compile(
    r"((?:文件|文件名|路径|目录))"
    r"(.+?)(?=(?:文件|文件名|路径|目录|账号|用户|话题|标签)|$)"
)

_ZH_ITN_HTTP_STATUS_RE = re.compile(r"((?:HTTP|HTTPS)\s*)([零〇一二三四五六七八九]{3})", re.IGNORECASE)

_ZH_ITN_PORT_RE = re.compile(r"((?:端口号|端口|port)\s*)([零〇一二三四五六七八九]{2,5})", re.IGNORECASE)

_ZH_ITN_ISO_DATETIME_RE = re.compile(
    r"([零〇一二三四五六七八九]{4}杠[零〇一二三四五六七八九]{2}杠[零〇一二三四五六七八九]{2}"
    r"[Tt][零〇一二三四五六七八九]{2}冒号[零〇一二三四五六七八九]{2}"
    r"(?:冒号[零〇一二三四五六七八九]{2})?(?:Z|z)?)"
)

_ZH_ITN_SPACE_DATETIME_RE = re.compile(
    r"([零〇一二三四五六七八九]{4}杠[零〇一二三四五六七八九]{2}杠[零〇一二三四五六七八九]{2})"
    r"\s*([零〇一二三四五六七八九]{2}冒号[零〇一二三四五六七八九]{2}"
    r"(?:冒号[零〇一二三四五六七八九]{2})?)"
)

_ZH_ITN_SPOKEN_DATETIME_RE = re.compile(
    r"([零〇一二三四五六七八九]{4}杠[零〇一二三四五六七八九]{2}杠[零〇一二三四五六七八九]{2})"
    r"([零〇一二两三四五六七八九十]{1,3})点"
    r"([零〇一二两三四五六七八九十]{1,3})分"
    r"(?:([零〇一二两三四五六七八九十]{1,3})秒)?"
)

_ZH_ITN_SHORTCUT_TOKEN = (
    r"(?:Ctrl|Control|Cmd|Command|Shift|Alt|Option|Meta|Win|Windows|Fn|Esc|Tab|Enter|Return|"
    r"Space|Delete|Del|Backspace|F[零〇一二三四五六七八九]{1,2}|[A-Za-z])"
)

_ZH_ITN_SHORTCUT_RE = re.compile(
    rf"(?<![A-Za-z0-9])({_ZH_ITN_SHORTCUT_TOKEN}(?:加{_ZH_ITN_SHORTCUT_TOKEN}){{1,5}})(?![A-Za-z0-9])"
)

_ZH_ITN_SEMVER_RE = re.compile(
    r"((?:版本|发布|标签)\s*)"
    r"([Vv][A-Za-z零〇一二三四五六七八九点杠加]+)"
    r"(?=(?:IPv6|ipv6|MAC地址|MAC|mac地址|mac|BSSID|UUID|uuid|ISBN|DOI|doi|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;\s])"
)

_ZH_ITN_CONTEXT_DOTTED_VERSION_RE = re.compile(
    rf"((?:版本|构建|发布|标签)\s*)({_ZH_ITN_POSITIVE_NUMBER_READING}(?:点{_ZH_ITN_POSITIVE_NUMBER_READING})+)"
)

_ZH_ITN_IPV4_PORT_RE = re.compile(
    r"[零〇一二三四五六七八九]{1,3}点[零〇一二三四五六七八九]{1,3}"
    r"点[零〇一二三四五六七八九]{1,3}点[零〇一二三四五六七八九]{1,3}"
    r"冒号[零〇一二三四五六七八九]{1,5}"
)

_ZH_ITN_IPV6_RE = re.compile(
    r"((?:IPv6|ipv6)\s*)"
    r"(.+?)(?=(?:MAC地址|MAC|mac地址|mac|BSSID|UUID|uuid|ISBN|DOI|doi|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_ISBN_RE = re.compile(
    r"((?:ISBN(?:-1[03])?)\s*)"
    r"(.+?)(?=(?:IPv6|ipv6|MAC地址|MAC|mac地址|mac|BSSID|UUID|uuid|DOI|doi|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_DOI_RE = re.compile(
    r"((?:DOI|doi)\s*)"
    r"(.+?)(?=(?:IPv6|ipv6|MAC地址|MAC|mac地址|mac|BSSID|UUID|uuid|ISBN|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_MAC_ADDRESS_RE = re.compile(
    r"((?:MAC地址|MAC|mac地址|mac|BSSID)\s*)"
    r"(.+?)(?=(?:IPv6|ipv6|UUID|uuid|ISBN|DOI|doi|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_UUID_RE = re.compile(
    r"((?:UUID|uuid)\s*)"
    r"(.+?)(?=(?:IPv6|ipv6|MAC地址|MAC|mac地址|mac|BSSID|ISBN|DOI|doi|颜色|色值|十六进制|背景色|前景色|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_HEX_COLOR_RE = re.compile(
    r"((?:颜色|色值|十六进制|背景色|前景色)\s*)"
    r"(.+?)(?=(?:IPv6|ipv6|MAC地址|MAC|mac地址|mac|BSSID|UUID|uuid|ISBN|DOI|doi|文件|文件名|路径|目录|账号|用户|话题|标签)|$|[，,。；;])"
)

_ZH_ITN_SOCIAL_HANDLE_RE = re.compile(
    r"((?:账号|用户))艾特(.+?)(?=(?:文件|文件名|路径|目录|账号|用户|话题|标签)|$)"
)

_ZH_ITN_SOCIAL_HASHTAG_RE = re.compile(
    r"((?:话题|标签))井号(.+?)(?=(?:文件|文件名|路径|目录|账号|用户|话题|标签)|$)"
)

_ZH_ITN_SEPARATED_DATE_RE = re.compile(
    r"(日期)([零〇一二三四五六七八九]{4})(杠|斜杠)([零〇一二两三四五六七八九十]{1,3})"
    r"\3([零〇一二两三四五六七八九十]{1,3})"
)

_ZH_ITN_YEAR_MONTH_RE = re.compile(
    rf"([零〇一二三四五六七八九]{{4}})年([零〇一二两三四五六七八九十]{{1,3}})月"
    r"(?![零〇一二两三四五六七八九十]{1,3}[日号])"
)

_ZH_ITN_TIMEZONE_RE = re.compile(r"(UTC|GMT)(加|正|减|负)([零〇一二两三四五六七八九十]{1,3})")

_ZH_ITN_SIGNED_NUMBER_RE = re.compile(rf"(负|正)({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_MONTH_DAY_RE = re.compile(
    rf"(?<!年)([零〇一二两三四五六七八九十]{{1,3}})月([零〇一二两三四五六七八九十]{{1,3}})[日号]"
)

_ZH_ITN_YEAR_QUARTER_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})年第?({_ZH_ITN_POSITIVE_NUMBER_READING})季度"
)

_ZH_ITN_QUARTER_YEAR_RE = re.compile(
    rf"第?({_ZH_ITN_POSITIVE_NUMBER_READING})季度({_ZH_ITN_POSITIVE_NUMBER_READING})"
)

_ZH_ITN_FISCAL_YEAR_PREFIX_RE = re.compile(rf"财年({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_FISCAL_YEAR_SUFFIX_RE = re.compile(rf"({_ZH_ITN_POSITIVE_NUMBER_READING})财年")

_ZH_ITN_PERCENT_POINT_RE = re.compile(rf"({_ZH_ITN_POSITIVE_NUMBER_READING})个?百分点")

_ZH_ITN_SCIENTIFIC_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})乘以?十的(负|正)?({_ZH_ITN_POSITIVE_NUMBER_READING})次方(米每秒)?"
)

_ZH_ITN_MATH_EXPR_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(加|减|乘以|乘|除以|除)"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(?:等于|等)"
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})(?=$|[，,。；;\s])"
)

_ZH_ITN_DIMENSION_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})乘({_ZH_ITN_POSITIVE_NUMBER_READING})"
    r"(厘米|毫米|千米|公里|米|英寸|英尺|像素)?"
)

_ZH_ITN_RANKING_ORDINAL_RE = re.compile(rf"(排名)第({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_DIRECT_UNIT_RE = re.compile(
    rf"(负?{_ZH_ITN_POSITIVE_NUMBER_READING}?)(兆字节每秒|千字节每秒|吉字节每秒|太字节每秒|"
    rf"吉比字节每秒|兆比字节每秒|千比字节每秒|兆比特每秒|千比特每秒|英里每小时|"
    rf"千瓦时|吉比字节|兆比字节|千比字节|"
    rf"毫摩尔每升|微克每毫升|纳克每毫升|毫克每分升|毫克每千克|毫克每毫升|"
    rf"国际单位每升|单位每升|毫米汞柱|"
    rf"摄氏度|华氏度|开尔文|"
    rf"平方公里|平方千米|平方厘米|平方毫米|平方米|平米|立方公里|立方千米|立方厘米|立方毫米|立方米|"
    rf"A计权分贝|分贝毫瓦|瓦每平方米|毫安时|个基点|牛米|基点|分贝|"
    rf"米每二次方秒|米每秒平方|升每分钟|牛顿|兆帕|帕|"
    rf"兆欧姆|千欧姆|毫伏|千伏|毫瓦|欧姆|微法|纳法|皮法|"
    rf"兆字节|千字节|吉赫兹|兆赫兹|千赫兹|吉字节|太字节|帧每秒|毫秒|"
    rf"英尺|英寸|盎司|英里|小时|分钟|毫安|毫升|微升|微克|纳克|"
    rf"伏特|千瓦|千帕|赫兹|转每分|ppm|ppb|秒|度|安|瓦|磅)"
)

_ZH_ITN_WRITTEN_PERCENT_ADJACENT_RE = re.compile(
    rf"(-\d+(?:\.\d+)?%)(?=负?{_ZH_ITN_POSITIVE_NUMBER_READING})"
)

_ZH_ITN_GENERAL_QUANTITY_RE = re.compile(
    rf"(?<!到)({_ZH_ITN_POSITIVE_NUMBER_READING})"
    r"(岁|人|个|件|次|名|位|台|辆|本|张|条|份|套|家|只|双|瓶|盒|包|颗|粒|间|门|类|组|批|项|页|行|天|周)"
    r"(?!基点|百分点|方)"
)

_ZH_ITN_RANGE_UNITS = (
    "平方公里|平方米|平方厘米|平方千米|平方毫米|立方公里|立方千米|立方米|立方厘米|立方毫米|"
    "千克|公斤|小时|分钟|美元|欧元|英镑|日元|港元|"
    "公里|千米|平米|年|月|日|天|秒|米|元|块|吨|克|人|个|件|次|名|位|台|辆|本|张|条|份|套|项|页"
)

_ZH_ITN_REPEATED_UNIT_RANGE_RE = re.compile(
    rf"([零〇一二两三四五六七八九十百千万亿兆点]+?)({_ZH_ITN_RANGE_UNITS})到"
    rf"([零〇一二两三四五六七八九十百千万亿兆点]+?)\2"
)

_ZH_ITN_PERCENT_RANGE_RE = re.compile(
    rf"百分之?({_ZH_ITN_POSITIVE_NUMBER_READING})到百分之?({_ZH_ITN_POSITIVE_NUMBER_READING})"
)

_ZH_ITN_RANGE_RE = re.compile(
    rf"({_ZH_ITN_POSITIVE_NUMBER_READING})到([零〇一二两三四五六七八九十百千万亿兆点]+?)({_ZH_ITN_RANGE_UNITS})"
)

_ZH_ITN_RATIO_RE = re.compile(rf"({_ZH_ITN_POSITIVE_NUMBER_READING})比({_ZH_ITN_POSITIVE_NUMBER_READING})")

_ZH_ITN_ALNUM_HYPHEN_RE = re.compile(r"([A-Za-z0-9]+(?:-\d+)*)杠([零〇一二三四五六七八九]+)")

_ZH_ITN_CONTEXT_SHORT_HYPHEN_CODE_RE = re.compile(
    r"((?:车位|门牌|房号|座位)\s*)([A-Za-z]?)([零〇一二三四五六七八九0-9]+)杠([零〇一二三四五六七八九0-9]+(?:杠[零〇一二三四五六七八九0-9]+)*)",
    re.IGNORECASE,
)

_ZH_ITN_COMPARISON_RE = re.compile(
    rf"([A-Za-z][A-Za-z0-9_]*|[\u4e00-\u9fff]{{1,8}})(大于等于|小于等于|不等于|约等于|大于|小于|等于)({_ZH_ITN_POSITIVE_NUMBER_READING})"
)

_ZH_ITN_SYMBOLIC_COMPARISON_RE = re.compile(
    r"(?<!问号)(?<!与)([A-Za-z][A-Za-z0-9_]*)(大于等于|小于等于|不等于|约等于|大于|小于|等于)([A-Za-z][A-Za-z0-9_]*)"
)

_ZH_ITN_INTEGER_READING = r"[零〇一二两三四五六七八九十百千万亿兆]+"

_ZH_ITN_FRACTION_READING = rf"{_ZH_ITN_INTEGER_READING}分之{_ZH_ITN_INTEGER_READING}"

_ZH_ITN_MEASURE_UNITS = (
    "块钱|兆比特每秒|兆比特一秒|千比特每秒|千比特一秒|千米每小时|公里每小时|"
    "千米一小时|公里一小时|兆字节每秒|千字节每秒|吉字节每秒|太字节每秒|英里每小时|"
    "千米一小时|公里一小时|平方公里|平方米|平方厘米|平方千米|平方毫米|立方公里|"
    "立方千米|立方厘米|立方毫米|立方米|米每秒|米一秒|摄氏度|华氏度|开尔文|兆字节|千字节|吉字节|太字节|"
    "吉比字节|兆比字节|千比字节|兆赫兹|吉赫兹|千赫兹|赫兹|千瓦时|千瓦|"
    "毫摩尔每升|微克每毫升|纳克每毫升|毫克每分升|毫克每千克|毫克每毫升|"
    "国际单位每升|单位每升|毫米汞柱|"
    "A计权分贝|分贝毫瓦|瓦每平方米|毫安时|个基点|牛米|基点|分贝|"
    "米每二次方秒|米每秒平方|升每分钟|牛顿|兆帕|帕|"
    "兆欧姆|千欧姆|毫伏|千伏|毫瓦|欧姆|微法|纳法|皮法|"
    "帧每秒|毫秒|小时|分钟|英尺|英寸|盎司|英里|伏特|毫安|千克|公斤|"
    "厘米|毫米|千米|公里|平米|毫升|微升|微克|纳克|千帕|ppm|ppb|元|块|吨|克|安|瓦|磅|秒|度|米|升"
)

_ZH_ITN_SPEED_READING = rf"{_ZH_ITN_NUMBER_READING}(?:千米每小时|公里每小时|千米一小时|公里一小时)"

_ZH_ITN_NUMBER_CHARS_TEXT = "负零〇一二两三四五六七八九十百千万亿兆点"

_ZH_ITN_DATE_READING = r"[零〇一二三四五六七八九十]{2,4}年[零〇一二三四五六七八九十]+月[零〇一二三四五六七八九十]+[日号]"

_ZH_ITN_TIME_READING = r"[零〇一二两三四五六七八九十]{1,3}点(?:半|[零〇一二两三四五六七八九十]{1,3}分?)?"

_ZH_ITN_PHONE_READING = r"[零〇一二三四五六七八九]{7,}"

_ZH_ITN_EMBEDDED_TOKEN_RE = re.compile(
    rf"([\u4e00-\u9fffA-Za-z])("
    rf"{_ZH_ITN_DATE_READING}|"
    rf"{_ZH_ITN_SPEED_READING}|"
    rf"{_ZH_ITN_FRACTION_READING}|"
    rf"百分之?{_ZH_ITN_NUMBER_READING}|"
    rf"{_ZH_ITN_PHONE_READING}|"
    rf"{_ZH_ITN_NUMBER_READING}(?:{_ZH_ITN_CURRENCY_UNITS})|"
    rf"{_ZH_ITN_NUMBER_READING}(?:{_ZH_ITN_MEASURE_UNITS})|"
    rf"{_ZH_ITN_TIME_READING}"
    rf")"
)

_ZH_ITN_TRAILING_TOKEN_RE = re.compile(
    rf"(?<![{_ZH_ITN_NUMBER_CHARS_TEXT}])("
    rf"{_ZH_ITN_DATE_READING}|"
    rf"{_ZH_ITN_SPEED_READING}|"
    rf"{_ZH_ITN_FRACTION_READING}|"
    rf"百分之?{_ZH_ITN_NUMBER_READING}|"
    rf"{_ZH_ITN_PHONE_READING}|"
    rf"{_ZH_ITN_NUMBER_READING}(?:{_ZH_ITN_CURRENCY_UNITS})|"
    rf"{_ZH_ITN_NUMBER_READING}(?:{_ZH_ITN_MEASURE_UNITS})|"
    rf"{_ZH_ITN_TIME_READING}"
    rf")([\u4e00-\u9fffA-Za-z])"
)

_ZH_ITN_WRITTEN_PREFIX_TOKEN = (
    r"(?:\d{4}年\d{2}月\d{2}日|(?<!年)\d{2}月\d{2}日|\d{7,}|\d{1,2}:\d{2}(?::\d{2})?|"
    r"-?\d+(?:\.\d+)?(?:块钱|人民币|美元|欧元|英镑|日元|港元|元|块|bp|bps|%|‰|°C|°F|MΩ|kΩ|Ω|µF|μF|uF|nF|pF|kV|mV|mW|W/m²|N·m|mAh|dBA|dBm|dB|µg/mL|μg/mL|ug/mL|ng/mL|IU/L|U/L|mg/kg|mg/dL|mg/mL|mmol/L|mmHg|MPa|kPa|Pa|ppm|ppb|µL|μL|uL|µg|μg|ug|ng|kg|mg|g|t|m²|cm²|km²|mm²|m³|cm³|m/s²|L/min|km/h|m/s|GiB/s|MiB/s|KiB/s|MB/s|KB/s|GB/s|TB/s|Mbps|kbps|GiB|MiB|KiB|GB|TB|fps|rpm|mph|deg|min|ms|ft|in|lb|oz|mi|mA|A|N|V|L|mbps|gb|tb|v|l|h|s|厘米|毫米|公里|千米|米|m|cm|mm|km)?)"
)

_ZH_ITN_WRITTEN_TRAILING_TOKEN = (
    r"(?:(?<!年)\d{2}月\d{2}日|\d{7,}|\d{1,2}:\d{2}(?::\d{2})?|"
    r"-?\d+(?:\.\d+)?(?:块钱|人民币|美元|欧元|英镑|日元|港元|元|块|bp|bps|%|‰|°C|°F|MΩ|kΩ|Ω|µF|μF|uF|nF|pF|kV|mV|mW|W/m²|N·m|mAh|dBA|dBm|dB|µg/mL|μg/mL|ug/mL|ng/mL|IU/L|U/L|mg/kg|mg/dL|mg/mL|mmol/L|mmHg|MPa|kPa|Pa|ppm|ppb|µL|μL|uL|µg|μg|ug|ng|kg|mg|g|t|m²|cm²|km²|mm²|m³|cm³|m/s²|L/min|km/h|m/s|GiB/s|MiB/s|KiB/s|MB/s|KB/s|GB/s|TB/s|Mbps|kbps|GiB|MiB|KiB|GB|TB|fps|rpm|mph|deg|min|ms|ft|in|lb|oz|mi|mA|A|N|V|L|mbps|gb|tb|v|l|h|s|厘米|毫米|公里|千米|米|m|cm|mm|km)?)"
)

_ZH_ITN_WRITTEN_UNIT_TOKEN = (
    r"(?:-?\d+(?:\.\d+)?(?:块钱|人民币|美元|欧元|英镑|日元|港元|元|块|bp|bps|%|‰|°C|°F|MΩ|kΩ|Ω|µF|μF|uF|nF|pF|kV|mV|mW|W/m²|N·m|mAh|dBA|dBm|dB|µg/mL|μg/mL|ug/mL|ng/mL|IU/L|U/L|mg/kg|mg/dL|mg/mL|mmol/L|mmHg|MPa|kPa|Pa|ppm|ppb|µL|μL|uL|µg|μg|ug|ng|kg|mg|g|t|m²|cm²|km²|mm²|m³|cm³|m/s²|L/min|km/h|m/s|GiB/s|MiB/s|KiB/s|MB/s|KB/s|GB/s|TB/s|Mbps|kbps|GiB|MiB|KiB|GB|TB|fps|rpm|mph|deg|min|ms|ft|in|lb|oz|mi|mA|A|N|V|L|mbps|gb|tb|v|l|h|s|厘米|毫米|公里|千米|米|m|cm|mm|km))"
)

_ZH_ITN_OUTPUT_PREFIX_SPACE_RE = re.compile(rf"([\u4e00-\u9fff])\s+({_ZH_ITN_WRITTEN_PREFIX_TOKEN})")

_ZH_ITN_OUTPUT_TRAILING_SPACE_RE = re.compile(rf"({_ZH_ITN_WRITTEN_TRAILING_TOKEN})\s+([\u4e00-\u9fff])")

_ZH_ITN_OUTPUT_ADJACENT_VALUE_SPACE_RE = re.compile(rf"({_ZH_ITN_WRITTEN_UNIT_TOKEN})\s+({_ZH_ITN_WRITTEN_UNIT_TOKEN})")

_ZH_ITN_OUTPUT_CONTEXT_GROUPED_DIGITS_RE = re.compile(
    r"((?:账号|卡号|银行卡|身份证|号码))((?:\d{2,4}\s+)+\d{2,8})"
)

_ZH_ITN_OUTPUT_TAX_CODE_RE = re.compile(
    r"((?:统一社会信用代码|社会信用代码|纳税人识别号|税号))([A-Za-z0-9](?:\s*[A-Za-z0-9]){7,24})"
)

_ZH_ITN_NUMBER_CHARS = frozenset(_ZH_ITN_NUMBER_CHARS_TEXT)

_ZH_ITN_ORDINAL_RE = re.compile(r"第([零〇一二两三四五六七八九十百千万]+)([名届次章节条段课页期])")

_ZH_ITN_ALNUM_DIGIT_RE = re.compile(r"([A-Za-z0-9]+)([零〇一二三四五六七八九]+)([A-Za-z0-9]*)")

_ZH_DIGIT_VALUES = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "幺": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

_ZH_UNIT_VALUES = {"十": 10, "百": 100, "千": 1000}

_ZH_CURRENCY_CODE_OUTPUT_REPLACEMENTS = (
    (re.compile(r"USD(-?\d+(?:\.\d+)?)"), r"\1美元"),
    (re.compile(r"EUR(-?\d+(?:\.\d+)?)"), r"\1欧元"),
    (re.compile(r"GBP(-?\d+(?:\.\d+)?)"), r"\1英镑"),
    (re.compile(r"CNY(-?\d+(?:\.\d+)?)"), r"\1人民币"),
    (re.compile(r"JPY(-?\d+(?:\.\d+)?)"), r"\1日元"),
    (re.compile(r"HKD(-?\d+(?:\.\d+)?)"), r"\1港元"),
    (re.compile(r"€(-?\d+(?:\.\d+)?)"), r"\1欧元"),
    (re.compile(r"£(-?\d+(?:\.\d+)?)"), r"\1英镑"),
)

_ZH_ITN_BLANK_LINE_COMMAND_RE = re.compile(r"(?:空一行|空行)")

_ZH_ITN_LINE_BREAK_COMMAND_RE = re.compile(r"(?:换行|新的一行|另起一行|下一行)")

_ZH_ITN_TAB_COMMAND_RE = re.compile(r"(?:制表符|制表位)")

_ZH_ITN_BULLET_COMMAND_RE = re.compile(r"(?:项目符号|列表项)")

_ZH_ITN_HEADING_COMMAND_RE = re.compile(r"([一二三])级标题")

_ZH_ITN_ORDERED_ITEM_COMMAND_RE = re.compile(r"(^|\n)[ \t]*(?:(?:编号|序号)([一二三四五六七八九十1-9])|第([一二三四五六七八九十1-9])(?:项|条))")

_ZH_ITN_BOLD_SPAN_RE = re.compile(r"加粗开始(.+?)加粗结束", re.DOTALL)

_ZH_ITN_CODE_SPAN_RE = re.compile(r"代码开始(.+?)代码结束", re.DOTALL)

_ZH_ITN_FORMAT_SYMBOL_COMMAND_RE = re.compile(
    r"(?:左大括号|右大括号|左花括号|右花括号|左尖括号|右尖括号|"
    r"反斜杠|竖线|波浪号|"
    r"艾特|井号|下划线|等号|加号|减号|百分号|星号|对勾|对号|勾号|叉号|错号)"
)

_ZH_ITN_SPEED_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)km\s*(?:每小时|一小时)")

_ZH_ITN_MPS_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)米\s*(?:每秒|一秒)")

_ZH_ITN_ACCELERATION_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)米每(?:二次方秒|秒平方)")

_ZH_ITN_LITER_PER_MINUTE_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)L每分钟")

_ZH_ITN_COORDINATE_DEGREE_OUTPUT_RE = re.compile(r"(北纬|南纬|东经|西经)(-?\d+(?:\.\d+)?)(?:deg|度)")

_ZH_ITN_YUAN_PER_AREA_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*元\s*每(?:平方米|平米|㎡|m²)")

_ZH_ITN_PH_OUTPUT_RE = re.compile(r"pH\s+(-?\d+(?:\.\d+)?)")

_ZH_ITN_UNIT_CASE_OUTPUT_REPLACEMENTS = (
    (re.compile(r"(-?\d+(?:\.\d+)?)ω(?![A-Za-z])"), r"\1Ω"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mω(?![A-Za-z])"), r"\1MΩ"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kω(?![A-Za-z])"), r"\1kΩ"),
    (re.compile(r"(-?\d+(?:\.\d+)?)uf(?![A-Za-z])"), r"\1µF"),
    (re.compile(r"(-?\d+(?:\.\d+)?)μf(?![A-Za-z])"), r"\1µF"),
    (re.compile(r"(-?\d+(?:\.\d+)?)µf(?![A-Za-z])"), r"\1µF"),
    (re.compile(r"(-?\d+(?:\.\d+)?)nf(?![A-Za-z])"), r"\1nF"),
    (re.compile(r"(-?\d+(?:\.\d+)?)pf(?![A-Za-z])"), r"\1pF"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kv(?![A-Za-z])"), r"\1kV"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mv(?![A-Za-z])"), r"\1mV"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mw(?![A-Za-z])"), r"\1mW"),
    (re.compile(r"(-?\d+(?:\.\d+)?)a(?![A-Za-z=!<>≈])"), r"\1A"),
    (re.compile(r"(-?\d+(?:\.\d+)?)w(?![A-Za-z])"), r"\1W"),
    (re.compile(r"(-?\d+(?:\.\d+)?)w/m²(?![A-Za-z])"), r"\1W/m²"),
    (re.compile(r"(-?\d+(?:\.\d+)?)n[·.]?m(?![A-Za-z])"), r"\1N·m"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mah(?![A-Za-z])"), r"\1mAh"),
    (re.compile(r"(-?\d+(?:\.\d+)?)dba(?![A-Za-z])"), r"\1dBA"),
    (re.compile(r"(-?\d+(?:\.\d+)?)dbm(?![A-Za-z])"), r"\1dBm"),
    (re.compile(r"(-?\d+(?:\.\d+)?)db(?![A-Za-z])"), r"\1dB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mpa(?![A-Za-z])"), r"\1MPa"),
    (re.compile(r"(-?\d+(?:\.\d+)?)pa(?![A-Za-z])"), r"\1Pa"),
    (re.compile(r"(-?\d+(?:\.\d+)?)n(?![A-Za-z·.])"), r"\1N"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mb/s(?![A-Za-z])"), r"\1MB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kb/s(?![A-Za-z])"), r"\1KB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)gb/s(?![A-Za-z])"), r"\1GB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)tb/s(?![A-Za-z])"), r"\1TB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)gib/s(?![A-Za-z])"), r"\1GiB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mib/s(?![A-Za-z])"), r"\1MiB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kib/s(?![A-Za-z])"), r"\1KiB/s"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mbps(?![A-Za-z])"), r"\1Mbps"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kbps(?![A-Za-z])"), r"\1kbps"),
    (re.compile(r"(-?\d+(?:\.\d+)?)gib(?![A-Za-z])"), r"\1GiB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mib(?![A-Za-z])"), r"\1MiB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kib(?![A-Za-z])"), r"\1KiB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mb(?![A-Za-z])"), r"\1MB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kb(?![A-Za-z])"), r"\1KB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)gb(?![A-Za-z])"), r"\1GB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)tb(?![A-Za-z])"), r"\1TB"),
    (re.compile(r"(-?\d+(?:\.\d+)?)ghz(?![A-Za-z])"), r"\1GHz"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mhz(?![A-Za-z])"), r"\1MHz"),
    (re.compile(r"(-?\d+(?:\.\d+)?)khz(?![A-Za-z])"), r"\1kHz"),
    (re.compile(r"(-?\d+(?:\.\d+)?)hz(?![A-Za-z])"), r"\1Hz"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kwh(?![A-Za-z])"), r"\1kWh"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kw(?![A-Za-z])"), r"\1kW"),
    (re.compile(r"(-?\d+(?:\.\d+)?)mmhg(?![A-Za-z])"), r"\1mmHg"),
    (re.compile(r"(-?\d+(?:\.\d+)?)kpa(?![A-Za-z])"), r"\1kPa"),
    (re.compile(r"(-?\d+(?:\.\d+)?)ml(?![A-Za-z])"), r"\1mL"),
    (re.compile(r"(-?\d+(?:\.\d+)?)ma(?![A-Za-z])"), r"\1mA"),
    (re.compile(r"(-?\d+(?:\.\d+)?)v(?![A-Za-z])"), r"\1V"),
)

_ZH_ITN_LITER_OUTPUT_RE = re.compile(r"(-?\d+(?:\.\d+)?)升")

_ZH_ITN_TEMPERATURE_OUTPUT_REPLACEMENTS = (
    (re.compile(r"(-?\d+(?:\.\d+)?)摄氏度"), r"\1°C"),
    (re.compile(r"(-?\d+(?:\.\d+)?)华氏度"), r"\1°F"),
    (re.compile(r"(-?\d+(?:\.\d+)?)开尔文"), r"\1K"),
)

_ZH_ITN_PER_POWER_OUTPUT_REPLACEMENTS = (
    (re.compile(r"(-?\d+(?:\.\d+)?)(kg|g|lb|千克|公斤|克|磅)每平方米"), "m²"),
    (re.compile(r"(-?\d+(?:\.\d+)?)(kg|g|lb|千克|公斤|克|磅)每立方米"), "m³"),
)

def _parse_zh_number_reading(text: str) -> str | None:
    if "点" not in text:
        value = _parse_zh_integer(text)
        return str(value) if value is not None else None

    integer_text, fractional_text = text.split("点", 1)
    integer = _parse_zh_integer(integer_text) if integer_text else 0
    if integer is None or not fractional_text:
        return None
    if not all(char in _ZH_DIGIT_VALUES for char in fractional_text):
        return None
    fractional = "".join(str(_ZH_DIGIT_VALUES[char]) for char in fractional_text)
    return f"{integer}.{fractional}"

def _parse_zh_integer(text: str) -> int | None:
    if not text:
        return None
    if all(char in _ZH_DIGIT_VALUES for char in text):
        return int("".join(str(_ZH_DIGIT_VALUES[char]) for char in text))
    for unit_label, unit_value in (("兆", 1000000000000), ("亿", 100000000), ("万", 10000)):
        if unit_label not in text:
            continue
        left, right = text.split(unit_label, 1)
        left_value = _parse_zh_integer(left) if left else 1
        right_value = _parse_zh_integer(right) if right else 0
        if left_value is None or right_value is None:
            return None
        return left_value * unit_value + right_value

    total = 0
    current = 0
    for char in text:
        if char in _ZH_DIGIT_VALUES:
            current = _ZH_DIGIT_VALUES[char]
            continue
        unit = _ZH_UNIT_VALUES.get(char)
        if unit is None:
            return None
        if current == 0:
            current = 1
        total += current * unit
        current = 0
    return total + current

def _prepare_zh_itn_input(text: str) -> str:
    prepared = _normalize_zh_itn_exact_hours(remove_asr_fillers(text))
    prepared = normalize_spoken_one_digit_sequences(prepared)
    prepared = _normalize_zh_itn_spoken_datetimes(prepared)
    prepared = _normalize_zh_itn_technical_tokens(prepared)
    prepared = _normalize_zh_itn_shortcuts(prepared)
    prepared = normalize_data_rates(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_file_social_tokens(prepared)
    prepared = _normalize_zh_itn_postal_codes(prepared)
    prepared = _normalize_zh_itn_year_month_days(prepared)
    prepared = _normalize_zh_itn_address_numbers(prepared)
    prepared = _normalize_zh_itn_identity_codes(prepared)
    prepared = _normalize_zh_itn_context_compact_dates(prepared)
    prepared = _normalize_zh_itn_dotted_dates(prepared)
    prepared = normalize_date_range_separators(prepared)
    prepared = _normalize_zh_itn_ph_values(prepared)
    prepared = _space_zh_itn_weekday_times(prepared)
    prepared = normalize_weekday_ranges(prepared)
    prepared = _normalize_zh_itn_daypart_time_ranges(prepared)
    prepared = _normalize_zh_itn_time_ranges(prepared)
    prepared = normalize_daypart_times(prepared, parse_integer=_parse_zh_integer)
    prepared = normalize_colloquial_times(prepared, parse_integer=_parse_zh_integer)
    prepared = _normalize_zh_itn_time_with_seconds(prepared)
    prepared = normalize_short_minute_durations(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_score_decimals(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_spoken_ratings(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_time_with_minutes(prepared)
    prepared = _normalize_zh_itn_plus_minus(prepared)
    prepared = _normalize_zh_itn_prefix_temperatures(prepared)
    prepared = normalize_decimal_temperatures(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_zero_below_temperatures(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_discounts(prepared)
    prepared = normalize_colloquial_money(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_context_wan_yi(prepared)
    prepared = _normalize_zh_itn_context_hash_codes(prepared)
    prepared = _normalize_zh_itn_context_colon_codes(prepared)
    prepared = _normalize_zh_itn_context_underscore_codes(prepared)
    prepared = _normalize_zh_itn_context_codes(prepared)
    prepared = _normalize_zh_itn_parameter_tokens(prepared)
    prepared = _normalize_zh_itn_phone_plus_numbers(prepared)
    prepared = _normalize_zh_itn_context_short_hyphen_codes(prepared)
    prepared = _normalize_zh_itn_context_hyphen_digits(prepared)
    prepared = _normalize_zh_itn_short_context_digits(prepared)
    prepared = _normalize_zh_itn_context_grouped_digits(prepared)
    prepared = _normalize_zh_itn_context_long_digits(prepared)
    prepared = _normalize_zh_itn_extensions(prepared)
    prepared = _normalize_zh_itn_separated_dates(prepared)
    prepared = _normalize_zh_itn_year_month_days(prepared)
    prepared = _normalize_zh_itn_year_months(prepared)
    prepared = _normalize_zh_itn_timezones(prepared)
    prepared = _normalize_zh_itn_spoken_colon_times(prepared)
    prepared = _normalize_zh_itn_month_days(prepared)
    prepared = _normalize_zh_itn_quarters(prepared)
    prepared = _normalize_zh_itn_fiscal_years(prepared)
    prepared = normalize_centuries(prepared, parse_integer=_parse_zh_integer)
    prepared = _normalize_zh_itn_percentage_points(prepared)
    prepared = _normalize_zh_itn_scientific_notation(prepared)
    prepared = _normalize_zh_itn_math_expressions(prepared)
    prepared = _normalize_zh_itn_dimensions(prepared)
    prepared = normalize_promotions(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_half_quantities(prepared)
    prepared = normalize_yuan_per_units(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_speed_per_hour(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_data_rates(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_decimal_lengths(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = normalize_decimal_weights(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_general_quantities(prepared)
    prepared = normalize_temperature_ranges(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_percent_ranges(prepared)
    prepared = _normalize_zh_itn_repeated_unit_ranges(prepared)
    prepared = _normalize_zh_itn_ranges(prepared)
    prepared = _normalize_zh_itn_blood_pressure(prepared)
    prepared = _normalize_zh_itn_direct_units(prepared)
    prepared = _normalize_zh_itn_multipliers(prepared)
    prepared = _normalize_zh_itn_foreign_money_subunits(prepared)
    prepared = _normalize_zh_itn_money_bare_fen(prepared)
    prepared = _normalize_zh_itn_money_subunits(prepared)
    prepared = _normalize_zh_itn_context_jiao_fen(prepared)
    prepared = _normalize_zh_itn_negative_money(prepared)
    prepared = _normalize_zh_itn_negative_percent(prepared)
    prepared = _normalize_zh_itn_positive_percent(prepared)
    prepared = normalize_shorthand_percent_ranges(prepared, parse_number_reading=_parse_zh_number_reading)
    prepared = _normalize_zh_itn_unsigned_percent(prepared)
    prepared = normalize_numeric_percents(prepared)
    prepared = _normalize_zh_itn_signed_numbers(prepared)
    prepared = _normalize_zh_itn_per_mille(prepared)
    prepared = _space_zh_itn_after_written_percent(prepared)
    prepared = _normalize_zh_itn_ranking_ordinals(prepared)
    prepared = _normalize_zh_itn_ranges(prepared)
    prepared = _normalize_zh_itn_ratios(prepared)
    prepared = _normalize_zh_itn_comparisons(prepared)
    prepared = _normalize_zh_itn_symbolic_comparisons(prepared)
    return _normalize_zh_itn_alnum_hyphens(prepared)

def _space_zh_itn_weekday_times(text: str) -> str:
    return _ZH_ITN_WEEKDAY_TIME_RE.sub(r"\1 ", text)

def _normalize_zh_itn_exact_hours(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_integer(match.group(1))
        if value is None or value > 24:
            return match.group(0)
        return f"{value:02d}:00"

    return _ZH_ITN_EXACT_HOUR_RE.sub(replace, text)

def _normalize_zh_itn_file_social_tokens(text: str) -> str:
    normalized = _ZH_ITN_FILE_CONTEXT_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2))}",
        text,
    )
    normalized = _ZH_ITN_SOCIAL_HANDLE_RE.sub(
        lambda match: f"{match.group(1)}@{_restore_zh_spoken_file_token(match.group(2))}",
        normalized,
    )
    return _ZH_ITN_SOCIAL_HASHTAG_RE.sub(
        lambda match: f"{match.group(1)}#{_restore_zh_spoken_file_token(match.group(2))}",
        normalized,
    )

def _normalize_zh_itn_technical_tokens(text: str) -> str:
    normalized = _ZH_ITN_ISO_DATETIME_RE.sub(
        lambda match: _restore_zh_spoken_file_token(match.group(1)).upper(),
        text,
    )
    normalized = _ZH_ITN_SPACE_DATETIME_RE.sub(
        lambda match: f"{_restore_zh_spoken_file_token(match.group(1))} {_restore_zh_spoken_file_token(match.group(2))}",
        normalized,
    )
    normalized = _ZH_ITN_HTTP_STATUS_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2))}",
        normalized,
    )
    normalized = _ZH_ITN_PORT_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2))}",
        normalized,
    )
    normalized = _ZH_ITN_SEMVER_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).lower()}",
        normalized,
    )
    normalized = _normalize_zh_itn_context_dotted_versions(normalized)
    normalized = _ZH_ITN_IPV4_PORT_RE.sub(
        lambda match: _restore_zh_spoken_file_token(match.group(0)),
        normalized,
    )
    normalized = _ZH_ITN_IPV6_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).lower()}",
        normalized,
    )
    normalized = _ZH_ITN_ISBN_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).upper()}",
        normalized,
    )
    normalized = _ZH_ITN_DOI_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).lower()}",
        normalized,
    )
    normalized = _ZH_ITN_MAC_ADDRESS_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).upper()}",
        normalized,
    )
    normalized = _ZH_ITN_UUID_RE.sub(
        lambda match: f"{match.group(1)}{_restore_zh_spoken_file_token(match.group(2)).lower()}",
        normalized,
    )

    def replace_color(match: re.Match[str]) -> str:
        value = _restore_zh_spoken_file_token(match.group(2)).upper()
        return f"{match.group(1)}{value if value.startswith('#') else f'#{value}'}"

    return _ZH_ITN_HEX_COLOR_RE.sub(replace_color, normalized)

def _normalize_zh_itn_context_dotted_versions(text: str) -> str:
    def parse_component(raw: str) -> str | None:
        if all(char in _ZH_DIGIT_VALUES for char in raw):
            return "".join(str(_ZH_DIGIT_VALUES[char]) for char in raw)
        value = _parse_zh_integer(raw)
        return str(value) if value is not None else None

    def replace(match: re.Match[str]) -> str:
        parts = [parse_component(part) for part in match.group(2).split("点")]
        if any(part is None for part in parts):
            return match.group(0)
        return f"{match.group(1)}{'.'.join(part for part in parts if part is not None)}"

    return _ZH_ITN_CONTEXT_DOTTED_VERSION_RE.sub(replace, text)

def _normalize_zh_itn_spoken_datetimes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_zh_integer(match.group(2))
        minute = _parse_zh_integer(match.group(3))
        second = _parse_zh_integer(match.group(4) or "零")
        if (
            hour is None
            or minute is None
            or second is None
            or not 0 <= hour <= 24
            or not 0 <= minute <= 59
            or not 0 <= second <= 59
        ):
            return match.group(0)
        suffix = f":{second:02d}" if match.group(4) else ""
        return f"{_restore_zh_spoken_file_token(match.group(1))} {hour:02d}:{minute:02d}{suffix}"

    return _ZH_ITN_SPOKEN_DATETIME_RE.sub(replace, text)

def _normalize_zh_itn_shortcuts(text: str) -> str:
    return _ZH_ITN_SHORTCUT_RE.sub(lambda match: _restore_zh_shortcut(match.group(1)), text)

def _restore_zh_shortcut(shortcut: str) -> str:
    return "+".join(_restore_zh_shortcut_token(token) for token in shortcut.split("加"))

def _restore_zh_shortcut_token(token: str) -> str:
    normalized = token.strip()
    modifier_tokens = {
        "Ctrl": "Ctrl",
        "Control": "Ctrl",
        "Cmd": "Cmd",
        "Command": "Cmd",
        "Shift": "Shift",
        "Alt": "Alt",
        "Option": "Option",
        "Meta": "Meta",
        "Win": "Win",
        "Windows": "Win",
        "Fn": "Fn",
        "Esc": "Esc",
        "Tab": "Tab",
        "Enter": "Enter",
        "Return": "Return",
        "Space": "Space",
        "Delete": "Delete",
        "Del": "Delete",
        "Backspace": "Backspace",
    }
    if normalized in modifier_tokens:
        return modifier_tokens[normalized]
    if re.fullmatch(r"F[零〇一二三四五六七八九]{1,2}", normalized):
        return f"F{_restore_zh_spoken_file_token(normalized[1:])}"
    if len(normalized) == 1 and normalized.isalpha():
        return normalized.upper()
    return _restore_zh_spoken_file_token(normalized)

def _restore_zh_spoken_file_token(text: str) -> str:
    replacements = (
        ("波浪号", "~"),
        ("反斜杠", "\\"),
        ("下划线", "_"),
        ("斜杠", "/"),
        ("井号", "#"),
        ("艾特", "@"),
        ("冒号", ":"),
        ("点", "."),
        ("杠", "-"),
    )
    output = text.replace(" ", "")
    for source, target in replacements:
        output = output.replace(source, target)
    return "".join(str(_ZH_DIGIT_VALUES[char]) if char in _ZH_DIGIT_VALUES else char for char in output)

def _normalize_zh_itn_postal_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}"

    return _ZH_ITN_POSTAL_CODE_RE.sub(replace, text)

def _normalize_zh_itn_address_numbers(text: str) -> str:
    def replace_room(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(1))
        return f"{digits}{match.group(2)}"

    def replace_prefixed_room(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}"

    def replace_prefixed_code(match: re.Match[str]) -> str:
        prefix = match.group(1)
        letter = match.group(2).upper()
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3))
        return f"{prefix}{letter}{digits}"

    def replace_cardinal(match: re.Match[str]) -> str:
        value = _parse_zh_integer(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}{match.group(2)}"

    normalized = _ZH_ITN_PREFIXED_ROOM_CODE_RE.sub(replace_prefixed_code, text)
    normalized = _ZH_ITN_MEETING_ROOM_NUMBER_RE.sub(replace_prefixed_room, normalized)
    normalized = _ZH_ITN_ROOM_NUMBER_RE.sub(replace_room, normalized)
    return _ZH_ITN_ADDRESS_CARDINAL_RE.sub(replace_cardinal, normalized)

def _normalize_zh_itn_identity_codes(text: str) -> str:
    def restore_code(raw: str) -> str:
        chars = []
        for char in raw:
            if char.isspace():
                continue
            if char in _ZH_DIGIT_VALUES:
                chars.append(str(_ZH_DIGIT_VALUES[char]))
            elif char.isalpha():
                chars.append(char.upper())
            else:
                chars.append(char)
        return "".join(chars)

    def replace_plate(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)}{match.group(3).upper()}{restore_code(match.group(4))}"

    def replace_id(match: re.Match[str]) -> str:
        code = restore_code(match.group(2))
        if not any(char.isdigit() for char in code):
            return match.group(0)
        return f"{match.group(1)}{code}"

    normalized = _ZH_ITN_LICENSE_PLATE_RE.sub(replace_plate, text)
    normalized = _ZH_ITN_TAX_CODE_RE.sub(replace_id, normalized)
    return _ZH_ITN_ID_CODE_RE.sub(replace_id, normalized)

def _normalize_zh_itn_context_compact_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year_digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        month = int("".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3)))
        day = int("".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(4)))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}{year_digits}-{month:02d}-{day:02d}"

    return _ZH_ITN_CONTEXT_COMPACT_DATE_RE.sub(replace, text)

def _normalize_zh_itn_dotted_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year_digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        month = _parse_zh_integer(match.group(3))
        day = _parse_zh_integer(match.group(4))
        if month is None or day is None:
            return match.group(0)
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{match.group(1)}{year_digits}.{month:02d}.{day:02d}"

    return _ZH_ITN_DOTTED_DATE_RE.sub(replace, text)

def _normalize_zh_itn_time_with_seconds(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_zh_integer(match.group(1))
        minute = _parse_zh_integer(match.group(2))
        second = _parse_zh_integer(match.group(3))
        if (
            hour is None
            or minute is None
            or second is None
            or not 0 <= hour <= 24
            or not 0 <= minute <= 59
            or not 0 <= second <= 59
        ):
            return match.group(0)
        return f"{hour:02d}:{minute:02d}:{second:02d}"

    return _ZH_ITN_TIME_WITH_SECONDS_RE.sub(replace, text)

def _normalize_zh_itn_time_with_minutes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_zh_integer(match.group(1))
        minute = _parse_zh_integer(match.group(2))
        if hour is None or minute is None or not 0 <= hour <= 24 or not 0 <= minute <= 59:
            return match.group(0)
        return f"{hour:02d}:{minute:02d}"

    return _ZH_ITN_TIME_WITH_MINUTES_RE.sub(replace, text)

def _normalize_zh_itn_spoken_colon_times(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_zh_integer(match.group(2))
        minute = _parse_zh_integer(match.group(3))
        if hour is None or minute is None or not 0 <= hour <= 24 or not 0 <= minute <= 59:
            return match.group(0)
        return f"{match.group(1)}{hour:02d}:{minute:02d}"

    return _ZH_ITN_SPOKEN_COLON_TIME_RE.sub(replace, text)

def _normalize_zh_itn_time_ranges(text: str) -> str:
    def parse_minute(raw: str | None) -> int | None:
        if raw is None:
            return 0
        if raw == "半":
            return 30
        return _parse_zh_integer(raw)

    def replace(match: re.Match[str]) -> str:
        start_hour = _parse_zh_integer(match.group(1))
        start_minute = parse_minute(match.group(2))
        end_hour = _parse_zh_integer(match.group(3))
        end_minute = parse_minute(match.group(4))
        if (
            start_hour is None
            or start_minute is None
            or end_hour is None
            or end_minute is None
            or not 0 <= start_hour <= 24
            or not 0 <= start_minute <= 59
            or not 0 <= end_hour <= 24
            or not 0 <= end_minute <= 59
        ):
            return match.group(0)
        return f"{start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

    return _ZH_ITN_TIME_RANGE_RE.sub(replace, text)

def _normalize_zh_itn_daypart_time_ranges(text: str) -> str:
    def parse_minute(raw: str | None) -> int | None:
        if raw is None:
            return 0
        if raw == "半":
            return 30
        return _parse_zh_integer(raw)

    def adjust_hour(hour: int, daypart: str | None, *, start_hour: int | None = None) -> int:
        if daypart in {"下午", "晚上"} and hour < 12:
            return hour + 12
        if daypart == "中午" and hour < 11:
            return hour + 12
        if daypart is None and start_hour is not None and start_hour >= 12 and hour <= 12:
            return hour + 12
        return hour

    def replace(match: re.Match[str]) -> str:
        start_hour = _parse_zh_integer(match.group(2))
        start_minute = parse_minute(match.group(3))
        end_hour = _parse_zh_integer(match.group(5))
        end_minute = parse_minute(match.group(6))
        if (
            start_hour is None
            or start_minute is None
            or end_hour is None
            or end_minute is None
            or not 0 <= start_hour <= 24
            or not 0 <= start_minute <= 59
            or not 0 <= end_hour <= 24
            or not 0 <= end_minute <= 59
        ):
            return match.group(0)
        adjusted_start_hour = adjust_hour(start_hour, match.group(1))
        adjusted_end_hour = adjust_hour(end_hour, match.group(4), start_hour=adjusted_start_hour)
        return f"{adjusted_start_hour:02d}:{start_minute:02d}-{adjusted_end_hour:02d}:{end_minute:02d}"

    return _ZH_ITN_DAYPART_TIME_RANGE_RE.sub(replace, text)

def _normalize_zh_itn_plus_minus(text: str) -> str:
    unit_map = {
        None: "",
        "摄氏度": "°C",
        "华氏度": "°F",
        "毫米": "mm",
        "厘米": "cm",
        "千米": "km",
        "公里": "km",
        "米": "m",
        "千克": "kg",
        "公斤": "kg",
        "毫克": "mg",
        "克": "g",
        "百分比": "%",
        "%": "%",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"±{value}{unit_map[match.group(2)]}"

    return _ZH_ITN_PLUS_MINUS_RE.sub(replace, text)

def _normalize_zh_itn_prefix_temperatures(text: str) -> str:
    unit_map = {"摄氏": "°C", "华氏": "°F"}

    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(3))
        if value is None:
            return match.group(0)
        sign = "-" if match.group(2) else ""
        return f"{sign}{value}{unit_map[match.group(1)]}"

    return _ZH_ITN_PREFIX_TEMPERATURE_RE.sub(replace, text)

def _normalize_zh_itn_context_hyphen_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        groups = match.group(2).split("杠")
        digits = ["".join(str(_ZH_DIGIT_VALUES[char]) for char in group) for group in groups]
        return f"{match.group(1)}{'-'.join(digits)}"

    return _ZH_ITN_CONTEXT_HYPHEN_DIGITS_RE.sub(replace, text)

def _normalize_zh_itn_context_short_hyphen_codes(text: str) -> str:
    def parse_digit_text(raw: str) -> str:
        return "".join(str(_ZH_DIGIT_VALUES[char]) if char in _ZH_DIGIT_VALUES else char for char in raw)

    def replace(match: re.Match[str]) -> str:
        first = f"{match.group(2).upper()}{parse_digit_text(match.group(3))}"
        rest = "-".join(parse_digit_text(group) for group in match.group(4).split("杠"))
        return f"{match.group(1)}{first}-{rest}"

    return _ZH_ITN_CONTEXT_SHORT_HYPHEN_CODE_RE.sub(replace, text)

def _normalize_zh_itn_short_context_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}"

    return _ZH_ITN_SHORT_CONTEXT_DIGITS_RE.sub(replace, text)

def _normalize_zh_itn_context_long_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}"

    return _ZH_ITN_CONTEXT_LONG_DIGITS_RE.sub(replace, text)

def _normalize_zh_itn_context_grouped_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = re.sub(r"(?:\s+|空格)", "", match.group(2))
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) if char in _ZH_DIGIT_VALUES else char for char in raw)
        return f"{match.group(1)}{digits}"

    return _ZH_ITN_CONTEXT_GROUPED_DIGITS_RE.sub(replace, text)

def _normalize_zh_itn_context_hash_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        letters = "".join(match.group(2).split()).upper()
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3))
        return f"{match.group(1)}{letters}#{digits}"

    return _ZH_ITN_CONTEXT_HASH_CODE_RE.sub(replace, text)

def _normalize_zh_itn_context_colon_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        letters = "".join(match.group(2).split()).upper()
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3))
        return f"{match.group(1)}{letters}:{digits}"

    return _ZH_ITN_CONTEXT_COLON_CODE_RE.sub(replace, text)

def _normalize_zh_itn_context_underscore_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        letters = "".join(match.group(2).split()).upper()
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3))
        return f"{match.group(1)}{letters}_{digits}"

    return _ZH_ITN_CONTEXT_UNDERSCORE_CODE_RE.sub(replace, text)

def _normalize_zh_itn_parameter_tokens(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{match.group(2)}={_restore_zh_spoken_file_token(match.group(3))}"

    return _ZH_ITN_PARAMETER_RE.sub(replace, text)

def _normalize_zh_itn_context_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        chars = []
        number_run = []

        def flush_number_run() -> bool:
            if not number_run:
                return True
            raw = "".join(number_run)
            if all(char in _ZH_DIGIT_VALUES for char in raw):
                chars.append("".join(str(_ZH_DIGIT_VALUES[char]) for char in raw))
            else:
                value = _parse_zh_integer(raw)
                if value is None:
                    return False
                chars.append(str(value))
            number_run.clear()
            return True

        for char in match.group(2):
            if char.isspace():
                continue
            if char == "杠":
                if not flush_number_run():
                    return match.group(0)
                chars.append("-")
            elif char in _ZH_ITN_NUMBER_CHARS and char != "点":
                number_run.append(char)
            elif char.isalpha():
                if not flush_number_run():
                    return match.group(0)
                chars.append(char.upper())
            elif not flush_number_run():
                return match.group(0)
        if not flush_number_run():
            return match.group(0)
        return f"{match.group(1)}{''.join(chars)}"

    return _ZH_ITN_CONTEXT_CODE_RE.sub(replace, text)

def _normalize_zh_itn_phone_plus_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        country = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        number = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(3))
        return f"{match.group(1)}+{country}{number}"

    return _ZH_ITN_PHONE_PLUS_RE.sub(replace, text)

def _normalize_zh_itn_extensions(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}"

    return _ZH_ITN_EXTENSION_RE.sub(replace, text)

def _normalize_zh_itn_separated_dates(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year_digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        month = _parse_zh_integer(match.group(4))
        day = _parse_zh_integer(match.group(5))
        if month is None or day is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        separator = "/" if match.group(3) == "斜杠" else "-"
        return f"{match.group(1)}{year_digits}{separator}{month:02d}{separator}{day:02d}"

    return _ZH_ITN_SEPARATED_DATE_RE.sub(replace, text)

def _normalize_zh_itn_year_month_days(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year_digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(1))
        month = _parse_zh_integer(match.group(2))
        day = _parse_zh_integer(match.group(3))
        if month is None or day is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        following = match.string[match.end() :]
        separator = " " if following and not following[0].isspace() and following[0] not in "，,。；;、" else ""
        return f"{year_digits}年{month:02d}月{day:02d}日{separator}"

    return _ZH_ITN_YEAR_MONTH_DAY_RE.sub(replace, text)

def _normalize_zh_itn_year_months(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        year_digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(1))
        month = _parse_zh_integer(match.group(2))
        if month is None or not 1 <= month <= 12:
            return match.group(0)
        return f"{year_digits}-{month:02d}"

    return _ZH_ITN_YEAR_MONTH_RE.sub(replace, text)

def _normalize_zh_itn_timezones(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        hour = _parse_zh_integer(match.group(3))
        if hour is None or not 0 <= hour <= 14:
            return match.group(0)
        sign = "+" if match.group(2) in {"加", "正"} else "-"
        return f"{match.group(1).upper()}{sign}{hour}"

    return _ZH_ITN_TIMEZONE_RE.sub(replace, text)

def _normalize_zh_itn_math_expressions(text: str) -> str:
    operator_symbols = {"加": "+", "减": "-", "乘": "×", "乘以": "×", "除": "÷", "除以": "÷"}

    def replace(match: re.Match[str]) -> str:
        left = _parse_zh_number_reading(match.group(1))
        right = _parse_zh_number_reading(match.group(3))
        result = _parse_zh_number_reading(match.group(4))
        if left is None or right is None or result is None:
            return match.group(0)
        return f"{left}{operator_symbols[match.group(2)]}{right}={result}"

    return _ZH_ITN_MATH_EXPR_RE.sub(replace, text)

def _normalize_zh_itn_dimensions(text: str) -> str:
    unit_map = {
        "厘米": "cm",
        "毫米": "mm",
        "千米": "km",
        "公里": "km",
        "米": "m",
        "英寸": "in",
        "英尺": "ft",
        "像素": "px",
    }

    def replace(match: re.Match[str]) -> str:
        left = _parse_zh_number_reading(match.group(1))
        right = _parse_zh_number_reading(match.group(2))
        if left is None or right is None:
            return match.group(0)
        unit = unit_map.get(match.group(3) or "", "")
        return f"{left}x{right}{unit}"

    return _ZH_ITN_DIMENSION_RE.sub(replace, text)

def _normalize_zh_itn_direct_units(text: str) -> str:
    unit_map = {
        "兆字节每秒": "MB/s",
        "千字节每秒": "KB/s",
        "吉字节每秒": "GB/s",
        "太字节每秒": "TB/s",
        "吉比字节每秒": "GiB/s",
        "兆比字节每秒": "MiB/s",
        "千比字节每秒": "KiB/s",
        "兆比特每秒": "Mbps",
        "千比特每秒": "kbps",
        "英里每小时": "mph",
        "兆字节": "MB",
        "千字节": "KB",
        "吉字节": "GB",
        "太字节": "TB",
        "吉比字节": "GiB",
        "兆比字节": "MiB",
        "千比字节": "KiB",
        "吉赫兹": "GHz",
        "兆赫兹": "MHz",
        "千赫兹": "kHz",
        "赫兹": "Hz",
        "千瓦时": "kWh",
        "千瓦": "kW",
        "毫摩尔每升": "mmol/L",
        "微克每毫升": "µg/mL",
        "纳克每毫升": "ng/mL",
        "毫克每分升": "mg/dL",
        "毫克每千克": "mg/kg",
        "毫克每毫升": "mg/mL",
        "国际单位每升": "IU/L",
        "单位每升": "U/L",
        "毫米汞柱": "mmHg",
        "摄氏度": "°C",
        "华氏度": "°F",
        "开尔文": "K",
        "平方米": "m²",
        "平米": "m²",
        "平方厘米": "cm²",
        "平方毫米": "mm²",
        "平方千米": "km²",
        "平方公里": "km²",
        "立方米": "m³",
        "立方厘米": "cm³",
        "立方毫米": "mm³",
        "立方千米": "km³",
        "立方公里": "km³",
        "A计权分贝": "dBA",
        "分贝毫瓦": "dBm",
        "瓦每平方米": "W/m²",
        "米每二次方秒": "m/s²",
        "米每秒平方": "m/s²",
        "升每分钟": "L/min",
        "毫安时": "mAh",
        "个基点": "bp",
        "牛米": "N·m",
        "牛顿": "N",
        "基点": "bp",
        "分贝": "dB",
        "兆帕": "MPa",
        "帕": "Pa",
        "兆欧姆": "MΩ",
        "千欧姆": "kΩ",
        "欧姆": "Ω",
        "千伏": "kV",
        "毫伏": "mV",
        "伏特": "V",
        "毫瓦": "mW",
        "微法": "µF",
        "纳法": "nF",
        "皮法": "pF",
        "毫安": "mA",
        "安": "A",
        "瓦": "W",
        "千帕": "kPa",
        "ppm": "ppm",
        "ppb": "ppb",
        "帧每秒": "fps",
        "毫秒": "ms",
        "英尺": "ft",
        "英寸": "in",
        "盎司": "oz",
        "英里": "mi",
        "微升": "µL",
        "微克": "µg",
        "纳克": "ng",
        "小时": "h",
        "分钟": "min",
        "秒": "s",
        "度": "°",
        "磅": "lb",
        "毫升": "mL",
        "转每分": "rpm",
    }

    def replace(match: re.Match[str]) -> str:
        raw_value = match.group(1)
        sign = "-" if raw_value.startswith("负") else ""
        if sign:
            raw_value = raw_value[1:]
        value = _parse_zh_number_reading(raw_value)
        if value is None:
            return match.group(0)
        return f"{sign}{value}{unit_map[match.group(2)]}"

    return _ZH_ITN_DIRECT_UNIT_RE.sub(replace, text)

def _normalize_zh_itn_blood_pressure(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        systolic = _parse_zh_number_reading(match.group(2))
        diastolic = _parse_zh_number_reading(match.group(3))
        if systolic is None or diastolic is None or "." in systolic or "." in diastolic:
            return match.group(0)
        return f"{match.group(1)}{systolic}/{diastolic}mmHg"

    return _ZH_ITN_BLOOD_PRESSURE_RE.sub(replace, text)

def _normalize_zh_itn_discounts(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}折"

    return _ZH_ITN_DISCOUNT_RE.sub(replace, text)

def _normalize_zh_itn_general_quantities(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}{match.group(2)}"

    return _ZH_ITN_GENERAL_QUANTITY_RE.sub(replace, text)

def _normalize_zh_itn_context_wan_yi(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}{match.group(3)}"

    return _ZH_ITN_CONTEXT_WAN_YI_RE.sub(replace, text)

def _normalize_zh_itn_ph_values(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{value}"

    return _ZH_ITN_PH_VALUE_RE.sub(replace, text)

def _normalize_zh_itn_multipliers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}倍"

    return _ZH_ITN_MULTIPLIER_RE.sub(replace, text)

def _normalize_zh_itn_month_days(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        month = _parse_zh_integer(match.group(1))
        day = _parse_zh_integer(match.group(2))
        if month is None or day is None or not 1 <= month <= 12 or not 1 <= day <= 31:
            return match.group(0)
        return f"{month:02d}月{day:02d}日"

    return _ZH_ITN_MONTH_DAY_RE.sub(replace, text)

def _normalize_zh_itn_quarters(text: str) -> str:
    def normalize(year_text: str, quarter_text: str, fallback: str) -> str:
        year = _parse_zh_integer(year_text)
        quarter = _parse_zh_integer(quarter_text)
        if year is None or quarter is None or not 1 <= quarter <= 4:
            return fallback
        return f"{year}Q{quarter}"

    prepared = _ZH_ITN_YEAR_QUARTER_RE.sub(
        lambda match: normalize(match.group(1), match.group(2), match.group(0)),
        text,
    )
    return _ZH_ITN_QUARTER_YEAR_RE.sub(
        lambda match: normalize(match.group(2), match.group(1), match.group(0)),
        prepared,
    )

def _normalize_zh_itn_fiscal_years(text: str) -> str:
    def normalize(year_text: str, fallback: str) -> str:
        year = _parse_zh_integer(year_text)
        if year is None:
            return fallback
        return f"FY{year}"

    prepared = _ZH_ITN_FISCAL_YEAR_PREFIX_RE.sub(lambda match: normalize(match.group(1), match.group(0)), text)
    return _ZH_ITN_FISCAL_YEAR_SUFFIX_RE.sub(lambda match: normalize(match.group(1), match.group(0)), prepared)

def _normalize_zh_itn_percentage_points(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}pp"

    return _ZH_ITN_PERCENT_POINT_RE.sub(replace, text)

def _normalize_zh_itn_scientific_notation(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        mantissa = _parse_zh_number_reading(match.group(1))
        exponent = _parse_zh_number_reading(match.group(3))
        if mantissa is None or exponent is None:
            return match.group(0)
        sign = "-" if match.group(2) == "负" else ""
        unit = "m/s" if match.group(4) else ""
        return f"{mantissa}e{sign}{exponent}{unit}"

    return _ZH_ITN_SCIENTIFIC_RE.sub(replace, text)

def _normalize_zh_itn_negative_money(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"-{value}{match.group(2)}"

    return _ZH_ITN_NEGATIVE_MONEY_RE.sub(replace, text)

def _normalize_zh_itn_money_bare_fen(text: str) -> str:
    def parse_digit(raw: str) -> int | None:
        value = _parse_zh_number_reading(raw)
        if value is None or "." in value:
            return None
        digit = int(value)
        return digit if 0 <= digit <= 9 else None

    def replace(match: re.Match[str]) -> str:
        yuan = _parse_zh_number_reading(match.group(1))
        jiao = parse_digit(match.group(3))
        fen = parse_digit(match.group(5))
        if yuan is None or "." in yuan or jiao is None or fen is None:
            return match.group(0)
        return f"{yuan}.{jiao}{fen}元"

    return _ZH_ITN_YUAN_JIAO_BARE_FEN_RE.sub(replace, text)

def _normalize_zh_itn_money_subunits(text: str) -> str:
    def parse_digit(raw: str | None) -> int | None:
        if raw is None:
            return 0
        value = _parse_zh_number_reading(raw)
        if value is None or "." in value:
            return None
        digit = int(value)
        return digit if 0 <= digit <= 9 else None

    def replace(match: re.Match[str]) -> str:
        yuan = _parse_zh_number_reading(match.group(1))
        jiao = parse_digit(match.group(3))
        fen = parse_digit(match.group(5) or match.group(6))
        if yuan is None or "." in yuan or jiao is None or fen is None:
            return match.group(0)
        fraction = f"{jiao}{fen}".rstrip("0")
        amount = f"{yuan}.{fraction}" if fraction else yuan
        return f"{amount}元"

    return _ZH_ITN_YUAN_JIAO_FEN_RE.sub(replace, text)

def _normalize_zh_itn_context_jiao_fen(text: str) -> str:
    def parse_digit(raw: str | None) -> int | None:
        if raw is None:
            return 0
        value = _parse_zh_number_reading(raw)
        if value is None or "." in value:
            return None
        digit = int(value)
        return digit if 0 <= digit <= 9 else None

    def replace(match: re.Match[str]) -> str:
        jiao = parse_digit(match.group(2))
        fen = parse_digit(match.group(4) or match.group(5))
        if jiao is None or fen is None:
            return match.group(0)
        return f"{match.group(1)}0.{jiao}{fen}元"

    return _ZH_ITN_CONTEXT_JIAO_FEN_RE.sub(replace, text)

def _normalize_zh_itn_foreign_money_subunits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        major = _parse_zh_number_reading(match.group(1))
        minor = _parse_zh_number_reading(match.group(3))
        if major is None or minor is None or "." in major or "." in minor:
            return match.group(0)
        minor_value = int(minor)
        if not 0 <= minor_value <= 99:
            return match.group(0)
        return f"{major}.{minor_value:02d}{match.group(2)}"

    return _ZH_ITN_FOREIGN_MONEY_SUBUNITS_RE.sub(replace, text)

def _normalize_zh_itn_negative_percent(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"-{value}%"

    return _ZH_ITN_NEGATIVE_PERCENT_RE.sub(replace, text)

def _normalize_zh_itn_positive_percent(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"+{value}%"

    return _ZH_ITN_POSITIVE_PERCENT_RE.sub(replace, text)

def _normalize_zh_itn_unsigned_percent(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}%"

    return _ZH_ITN_UNSIGNED_PERCENT_RE.sub(replace, text)

def _normalize_zh_itn_signed_numbers(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(2))
        if value is None:
            return match.group(0)
        sign = "-" if match.group(1) == "负" else "+"
        return f"{sign}{value}"

    return _ZH_ITN_SIGNED_NUMBER_RE.sub(replace, text)

def _normalize_zh_itn_per_mille(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(1))
        if value is None:
            return match.group(0)
        return f"{value}‰"

    return _ZH_ITN_PER_MILLE_RE.sub(replace, text)

def _space_zh_itn_after_written_percent(text: str) -> str:
    return _ZH_ITN_WRITTEN_PERCENT_ADJACENT_RE.sub(r"\1 ", text)

def _normalize_zh_itn_ranking_ordinals(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_integer(match.group(2))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}第{value}"

    return _ZH_ITN_RANKING_ORDINAL_RE.sub(replace, text)

def _normalize_zh_itn_ranges(text: str) -> str:
    unit_map = {
        "千克": "kg",
        "公斤": "kg",
        "克": "g",
        "平方米": "m²",
        "平米": "m²",
        "平方厘米": "cm²",
        "平方毫米": "mm²",
        "平方千米": "km²",
        "平方公里": "km²",
        "立方米": "m³",
        "立方厘米": "cm³",
        "立方毫米": "mm³",
        "立方千米": "km³",
        "立方公里": "km³",
    }

    def replace(match: re.Match[str]) -> str:
        start = _parse_zh_number_reading(match.group(1))
        end = _parse_zh_number_reading(match.group(2))
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end}{unit_map.get(match.group(3), match.group(3))}"

    return _ZH_ITN_RANGE_RE.sub(replace, text)

def _normalize_zh_itn_repeated_unit_ranges(text: str) -> str:
    unit_map = {
        "千克": "kg",
        "公斤": "kg",
        "克": "g",
        "平方米": "m²",
        "平米": "m²",
        "平方厘米": "cm²",
        "平方毫米": "mm²",
        "平方千米": "km²",
        "平方公里": "km²",
        "立方米": "m³",
        "立方厘米": "cm³",
        "立方毫米": "mm³",
        "立方千米": "km³",
        "立方公里": "km³",
    }

    def replace(match: re.Match[str]) -> str:
        start = _parse_zh_number_reading(match.group(1))
        end = _parse_zh_number_reading(match.group(3))
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end}{unit_map.get(match.group(2), match.group(2))}"

    return _ZH_ITN_REPEATED_UNIT_RANGE_RE.sub(replace, text)

def _normalize_zh_itn_percent_ranges(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        start = _parse_zh_number_reading(match.group(1))
        end = _parse_zh_number_reading(match.group(2))
        if start is None or end is None:
            return match.group(0)
        return f"{start}-{end}%"

    return _ZH_ITN_PERCENT_RANGE_RE.sub(replace, text)

def _normalize_zh_itn_ratios(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        left = _parse_zh_number_reading(match.group(1))
        right = _parse_zh_number_reading(match.group(2))
        if left is None or right is None:
            return match.group(0)
        return f"{left}:{right}"

    return _ZH_ITN_RATIO_RE.sub(replace, text)

def _normalize_zh_itn_comparisons(text: str) -> str:
    operator_symbols = {
        "大于等于": ">=",
        "小于等于": "<=",
        "不等于": "!=",
        "约等于": "≈",
        "大于": ">",
        "小于": "<",
        "等于": "=",
    }

    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_number_reading(match.group(3))
        if value is None:
            return match.group(0)
        return f"{match.group(1)}{operator_symbols[match.group(2)]}{value}"

    return _ZH_ITN_COMPARISON_RE.sub(replace, text)

def _normalize_zh_itn_symbolic_comparisons(text: str) -> str:
    operator_symbols = {
        "大于等于": ">=",
        "小于等于": "<=",
        "不等于": "!=",
        "约等于": "≈",
        "大于": ">",
        "小于": "<",
        "等于": "=",
    }

    return _ZH_ITN_SYMBOLIC_COMPARISON_RE.sub(
        lambda match: f"{match.group(1)}{operator_symbols[match.group(2)]}{match.group(3)}",
        text,
    )

def _normalize_zh_itn_alnum_hyphens(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}-{digits}"

    normalized = text
    for _ in range(8):
        next_normalized = _ZH_ITN_ALNUM_HYPHEN_RE.sub(replace, normalized)
        if next_normalized == normalized:
            return normalized
        normalized = next_normalized
    return normalized

def _restore_zh_itn_layout_commands(text: str) -> str:
    restored = _ZH_ITN_HEADING_COMMAND_RE.sub(lambda match: f" __HEADING_{_ZH_DIGIT_VALUES[match.group(1)]}__ ", text)
    restored = _ZH_ITN_BULLET_COMMAND_RE.sub(" __BULLET__ ", restored)
    restored = _ZH_ITN_TAB_COMMAND_RE.sub("\t", restored)
    restored = _ZH_ITN_BLANK_LINE_COMMAND_RE.sub("\n\n", restored)
    restored = _ZH_ITN_LINE_BREAK_COMMAND_RE.sub("\n", restored)
    restored = _ZH_ITN_ORDERED_ITEM_COMMAND_RE.sub(_restore_zh_itn_ordered_item_match, restored)
    restored = re.sub(r"[ \t]*__HEADING_([123])__[ \t]*", lambda match: f"{'#' * int(match.group(1))} ", restored)
    restored = re.sub(r"[ \t]*__BULLET__[ \t]*", "- ", restored)
    restored = _ZH_ITN_BOLD_SPAN_RE.sub(lambda match: f"**{match.group(1).strip()}**", restored)
    restored = _ZH_ITN_CODE_SPAN_RE.sub(lambda match: f"`{match.group(1).strip()}`", restored)
    restored = re.sub(r"[ ]*\t[ ]*", "\t", restored)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", restored)

def _restore_zh_itn_ordered_item_match(match: re.Match[str]) -> str:
    raw_number = match.group(2) or match.group(3)
    value = int(raw_number) if raw_number.isdigit() else _parse_zh_integer(raw_number)
    if value is None:
        return match.group(0)
    return f"{match.group(1)}{value}. "

def _restore_zh_itn_format_symbols(text: str) -> str:
    symbol_map = {
        "艾特": "@",
        "井号": "#",
        "下划线": "_",
        "等号": "=",
        "加号": "+",
        "减号": "-",
        "百分号": "%",
        "星号": "*",
        "对勾": "✓",
        "对号": "✓",
        "勾号": "✓",
        "叉号": "×",
        "错号": "×",
        "左大括号": "{",
        "右大括号": "}",
        "左花括号": "{",
        "右花括号": "}",
        "左尖括号": "<",
        "右尖括号": ">",
        "反斜杠": "\\",
        "竖线": "|",
        "波浪号": "~",
    }

    def replace(match: re.Match[str]) -> str:
        return f" __FMT_{ord(symbol_map[match.group(0)]):X}__ "

    restored = _ZH_ITN_FORMAT_SYMBOL_COMMAND_RE.sub(replace, text)
    if restored == text:
        return text
    return re.sub(r"\s*__FMT_([0-9A-F]+)__([ \t]*)", _restore_itn_format_symbol_match, restored)

def _segment_zh_itn_tokens(text: str) -> str:
    def segment(match: re.Match[str]) -> str:
        prefix, token = match.groups()
        if prefix in _ZH_ITN_NUMBER_CHARS:
            return f"{prefix}{token}"
        return f"{prefix} {token}"

    def split_trailing(match: re.Match[str]) -> str:
        token, suffix = match.groups()
        if suffix in _ZH_ITN_NUMBER_CHARS and token[-1] in _ZH_ITN_NUMBER_CHARS:
            return f"{token}{suffix}"
        if "点" in token and suffix in {"分", "半"}:
            return f"{token}{suffix}"
        if suffix in {"每", "一"} and token.endswith(("千米", "公里")):
            return f"{token}{suffix}"
        return f"{token} {suffix}"

    segmented = _ZH_ITN_EMBEDDED_TOKEN_RE.sub(segment, text)
    for _ in range(8):
        next_segmented = _ZH_ITN_TRAILING_TOKEN_RE.sub(split_trailing, segmented)
        if next_segmented == segmented:
            return segmented
        segmented = next_segmented
    return segmented

def _compact_zh_itn_spacing(text: str) -> str:
    compacted = _ZH_ITN_OUTPUT_PREFIX_SPACE_RE.sub(r"\1\2", text)
    compacted = _ZH_ITN_OUTPUT_TRAILING_SPACE_RE.sub(r"\1\2", compacted)
    compacted = _ZH_ITN_OUTPUT_ADJACENT_VALUE_SPACE_RE.sub(r"\1\2", compacted)
    compacted = _compact_zh_itn_output_grouped_digits(compacted)
    compacted = _compact_zh_itn_output_tax_codes(compacted)
    compacted = _localize_zh_itn_currency_codes(compacted)
    compacted = _ZH_ITN_SPEED_OUTPUT_RE.sub(r"\1km/h", compacted)
    compacted = _ZH_ITN_ACCELERATION_OUTPUT_RE.sub(r"\1m/s²", compacted)
    compacted = _ZH_ITN_MPS_OUTPUT_RE.sub(r"\1m/s", compacted)
    compacted = _ZH_ITN_LITER_PER_MINUTE_OUTPUT_RE.sub(r"\1L/min", compacted)
    compacted = _ZH_ITN_COORDINATE_DEGREE_OUTPUT_RE.sub(r"\1\2°", compacted)
    compacted = _ZH_ITN_YUAN_PER_AREA_OUTPUT_RE.sub(r"\1元/m²", compacted)
    compacted = _ZH_ITN_PH_OUTPUT_RE.sub(r"pH\1", compacted)
    compacted = _normalize_zh_itn_unit_case(compacted)
    compacted = _ZH_ITN_LITER_OUTPUT_RE.sub(r"\1L", compacted)
    for pattern, replacement in _ZH_ITN_TEMPERATURE_OUTPUT_REPLACEMENTS:
        compacted = pattern.sub(replacement, compacted)
    compacted = _normalize_zh_itn_per_power_units(compacted)
    compacted = _ZH_ITN_OUTPUT_PREFIX_SPACE_RE.sub(r"\1\2", compacted)
    compacted = _ZH_ITN_OUTPUT_TRAILING_SPACE_RE.sub(r"\1\2", compacted)
    compacted = _ZH_ITN_OUTPUT_ADJACENT_VALUE_SPACE_RE.sub(r"\1\2", compacted)
    compacted = _replace_zh_itn_ordinals(compacted)
    compacted = _replace_zh_itn_alnum_digits(compacted)
    compacted = _normalize_zh_itn_native_residuals(compacted)
    return _restore_zh_ascii_electronic(compacted)

def _normalize_zh_itn_native_residuals(text: str) -> str:
    number = r"[零〇一二两三四五六七八九十百千万亿兆点](?:\s*[零〇一二两三四五六七八九十百千万亿兆点])*"
    compacted = text

    def parse(raw: str) -> str | None:
        return _parse_zh_number_reading(re.sub(r"\s+", "", raw))

    def replace_fraction(match: re.Match[str]) -> str:
        denominator = parse(match.group(1))
        numerator = parse(match.group(2))
        if numerator is None or denominator is None:
            return match.group(0)
        return f"{numerator}/{denominator}"

    compacted = re.sub(rf"({number})\s*分之\s*({number})", replace_fraction, compacted)

    def replace_yuan_area(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}元/m²" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*元\s*每\s*(?:平方米|平米)", replace_yuan_area, compacted)

    def replace_per_square_meter(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}kg/m²" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*(?:千克|公斤)\s*每\s*(?:平方米|平米)", replace_per_square_meter, compacted)

    power_units = {
        "平方米": "m²",
        "平米": "m²",
        "平方厘米": "cm²",
        "平方毫米": "mm²",
        "平方千米": "km²",
        "平方公里": "km²",
        "立方米": "m³",
        "立方厘米": "cm³",
        "立方毫米": "mm³",
        "立方千米": "km³",
        "立方公里": "km³",
    }

    def replace_power(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}{power_units[match.group(2)]}" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*({'|'.join(power_units)})", replace_power, compacted)

    def replace_kilometer(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}km" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*千米", replace_kilometer, compacted)

    def replace_kilogram(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}kg" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*(?:千克|公斤)", replace_kilogram, compacted)

    direct_units = {
        "厘米": "cm",
        "毫米": "mm",
        "千米": "km",
        "公里": "公里",
        "米每秒": "m/s",
        "米": "米",
        "千克": "kg",
        "公斤": "kg",
        "克": "g",
        "升": "L",
    }

    def replace_direct(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}{direct_units[match.group(2)]}" if value is not None else match.group(0)

    compacted = re.sub(rf"({number})\s*({'|'.join(direct_units)})", replace_direct, compacted)
    compacted = re.sub(r"(\d+(?:\.\d+)?)米\s*每秒", r"\1m/s", compacted)

    def replace_large_money(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}{match.group(2)}元" if value is not None else match.group(0)

    compacted = re.sub(rf"(?<![0-9.])({number})\s*(万|亿)\s*元", replace_large_money, compacted)

    money_units = "人民币|美元|欧元|英镑|日元|港元|块钱|元|块"

    def replace_money(match: re.Match[str]) -> str:
        value = parse(match.group(1))
        return f"{value}{match.group(2)}" if value is not None else match.group(0)

    compacted = re.sub(rf"(?<![0-9.])({number})\s*({money_units})", replace_money, compacted)
    compacted = re.sub(r"(\d+(?:\.\d+)?)(元|块)钱", r"\1\2钱", compacted)
    compacted = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=\d)", "", compacted)
    compacted = re.sub(
        r"(\d+(?:\.\d+)?(?:元|块|美元|欧元|英镑|日元|港元|kg|cm|mm|km|m²|cm²|m³|m/s|L|米|公里))\s+(?=[\u4e00-\u9fff])",
        r"\1",
        compacted,
    )
    compacted = re.sub(r"(\d+/\d+)\s+(?=[\u4e00-\u9fff])", r"\1", compacted)
    return compacted

def _compact_zh_itn_output_grouped_digits(text: str) -> str:
    return _ZH_ITN_OUTPUT_CONTEXT_GROUPED_DIGITS_RE.sub(lambda match: f"{match.group(1)}{match.group(2).replace(' ', '')}", text)

def _compact_zh_itn_output_tax_codes(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        code = re.sub(r"\s+", "", match.group(2)).upper()
        if not any(char.isdigit() for char in code):
            return match.group(0)
        return f"{match.group(1)}{code}"

    return _ZH_ITN_OUTPUT_TAX_CODE_RE.sub(replace, text)

def _restore_zh_ascii_electronic(text: str) -> str:
    restored = _ZH_SPOKEN_URL_RE.sub(
        lambda match: _restore_zh_ascii_electronic_token(match.group(1)),
        text,
    )
    restored = _ZH_SPOKEN_EMAIL_RE.sub(
        lambda match: f"{match.group(1)}@{_restore_zh_ascii_electronic_token(match.group(2))}",
        restored,
    )
    restored = _ZH_MIXED_SPOKEN_EMAIL_RE.sub(
        lambda match: (
            f"{_restore_zh_ascii_electronic_token(match.group(1))}@"
            f"{_restore_zh_ascii_electronic_token(match.group(2))}"
        ),
        restored,
    )
    return _ZH_SPOKEN_DOMAIN_RE.sub(
        lambda match: _restore_zh_ascii_electronic_token(match.group(1)),
        restored,
    )

def _restore_zh_ascii_electronic_token(token: str) -> str:
    replacements = (
        ("冒号斜杠斜杠", "://"),
        ("下划线", "_"),
        ("斜杠", "/"),
        ("艾特", "@"),
        ("点", "."),
        ("加", "+"),
        ("杠", "-"),
        ("问号", "?"),
        ("等于", "="),
        ("与", "&"),
        ("井号", "#"),
        ("冒号", ":"),
    )
    output = token
    for source, target in replacements:
        output = output.replace(source, target)
    return "".join(str(_ZH_DIGIT_VALUES[char]) if char in _ZH_DIGIT_VALUES else char for char in output)

def _localize_zh_itn_currency_codes(text: str) -> str:
    localized = text
    for pattern, replacement in _ZH_CURRENCY_CODE_OUTPUT_REPLACEMENTS:
        localized = pattern.sub(replacement, localized)
    return localized

def _normalize_zh_itn_unit_case(text: str) -> str:
    output = text
    for pattern, replacement in _ZH_ITN_UNIT_CASE_OUTPUT_REPLACEMENTS:
        output = pattern.sub(replacement, output)
    return output

def _normalize_zh_itn_per_power_units(text: str) -> str:
    unit_map = {"千克": "kg", "公斤": "kg", "克": "g", "磅": "lb"}
    output = text
    for pattern, denominator in _ZH_ITN_PER_POWER_OUTPUT_REPLACEMENTS:
        output = pattern.sub(
            lambda match: f"{match.group(1)}{unit_map.get(match.group(2), match.group(2))}/{denominator}",
            output,
        )
    return output

def _replace_zh_itn_ordinals(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        value = _parse_zh_integer(match.group(1))
        if value is None:
            return match.group(0)
        return f"第{value}{match.group(2)}"

    return _ZH_ITN_ORDINAL_RE.sub(replace, text)

def _replace_zh_itn_alnum_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        digits = "".join(str(_ZH_DIGIT_VALUES[char]) for char in match.group(2))
        return f"{match.group(1)}{digits}{match.group(3)}"

    return _ZH_ITN_ALNUM_DIGIT_RE.sub(replace, text)

def prepare_input(text: str) -> str:
    return _segment_zh_itn_tokens(_prepare_zh_itn_input(text))

def finalize_outputs(texts: list[str]) -> list[str]:
    return [
        _restore_zh_itn_layout_commands(
            _restore_zh_itn_format_symbols(normalize_spoken_punctuation(_compact_zh_itn_spacing(text)))
        )
        for text in texts
    ]
