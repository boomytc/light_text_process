from __future__ import annotations

import re


_EMAIL_SPOKEN_RE = re.compile(
    r"\b([a-z0-9]+(?:\s+[a-z0-9]+)*)\s+(?:at|arroba|at-sign)\s+"
    r"([a-z0-9]+(?:\s+[a-z0-9]+)*)\s+"
    r"(?:dot|point|punto|punkt|точка|ponto)\s+([a-z]{2,})\b",
    re.IGNORECASE,
)

_DIGIT_WORDS = {
    "de": {
        "null": "0",
        "eins": "1",
        "ein": "1",
        "zwei": "2",
        "drei": "3",
        "vier": "4",
        "fünf": "5",
        "fuenf": "5",
        "sechs": "6",
        "sieben": "7",
        "acht": "8",
        "neun": "9",
    },
    "es": {
        "cero": "0",
        "uno": "1",
        "una": "1",
        "dos": "2",
        "tres": "3",
        "cuatro": "4",
        "cinco": "5",
        "seis": "6",
        "siete": "7",
        "ocho": "8",
        "nueve": "9",
    },
    "fr": {
        "zéro": "0",
        "zero": "0",
        "un": "1",
        "une": "1",
        "deux": "2",
        "trois": "3",
        "quatre": "4",
        "cinq": "5",
        "six": "6",
        "sept": "7",
        "huit": "8",
        "neuf": "9",
    },
    "id": {
        "nol": "0",
        "satu": "1",
        "dua": "2",
        "tiga": "3",
        "empat": "4",
        "lima": "5",
        "enam": "6",
        "tujuh": "7",
        "delapan": "8",
        "sembilan": "9",
    },
    "ja": {
        "zero": "0",
        "rei": "0",
        "ichi": "1",
        "ni": "2",
        "san": "3",
        "yon": "4",
        "shi": "4",
        "go": "5",
        "roku": "6",
        "nana": "7",
        "shichi": "7",
        "hachi": "8",
        "kyu": "9",
        "ku": "9",
    },
    "ko": {
        "yeong": "0",
        "gong": "0",
        "il": "1",
        "i": "2",
        "sam": "3",
        "sa": "4",
        "o": "5",
        "yuk": "6",
        "chil": "7",
        "pal": "8",
        "gu": "9",
    },
    "pt": {
        "zero": "0",
        "um": "1",
        "uma": "1",
        "dois": "2",
        "duas": "2",
        "três": "3",
        "tres": "3",
        "quatro": "4",
        "cinco": "5",
        "seis": "6",
        "sete": "7",
        "oito": "8",
        "nove": "9",
    },
    "ru": {
        "ноль": "0",
        "нуль": "0",
        "один": "1",
        "одна": "1",
        "два": "2",
        "две": "2",
        "три": "3",
        "четыре": "4",
        "пять": "5",
        "шесть": "6",
        "семь": "7",
        "восемь": "8",
        "девять": "9",
        "odin": "1",
        "dva": "2",
        "tri": "3",
        "nol": "0",
        "chetyre": "4",
        "pyat": "5",
        "shest": "6",
    },
    "tl": {
        "sero": "0",
        "isa": "1",
        "dalawa": "2",
        "tatlo": "3",
        "apat": "4",
        "lima": "5",
        "anim": "6",
        "pito": "7",
        "walo": "8",
        "siyam": "9",
    },
    "vi": {
        "không": "0",
        "khong": "0",
        "một": "1",
        "mot": "1",
        "hai": "2",
        "ba": "3",
        "bốn": "4",
        "bon": "4",
        "năm": "5",
        "nam": "5",
        "sáu": "6",
        "sau": "6",
        "bảy": "7",
        "bay": "7",
        "tám": "8",
        "tam": "8",
        "chín": "9",
        "chin": "9",
    },
}

_CARDINAL_PHRASES = {
    "de": {"zwölf": "12", "einundzwanzig": "21", "fünfzehn": "15", "dreißig": "30", "fünfzig": "50"},
    "es": {"doce": "12", "veintiuno": "21", "quince": "15", "treinta": "30", "cincuenta": "50"},
    "fr": {"douze": "12", "vingt et un": "21", "quinze": "15", "trente": "30", "cinquante": "50"},
    "id": {"dua belas": "12", "dua puluh satu": "21", "lima belas": "15", "tiga puluh": "30", "lima puluh": "50"},
    "ja": {"ju ni": "12", "niju ichi": "21", "ju go": "15", "sanju": "30", "goju": "50"},
    "ko": {"sip i": "12", "isibil": "21", "sibo": "15", "samsip": "30", "osip": "50"},
    "pt": {"doze": "12", "vinte e um": "21", "quinze": "15", "trinta": "30", "cinquenta": "50"},
    "ru": {"двенадцать": "12", "двадцать один": "21", "пятнадцать": "15", "тридцать": "30", "пятьдесят": "50"},
    "tl": {
        "labindalawa": "12",
        "dalawampu't isa": "21",
        "labinlima": "15",
        "tatlumpu": "30",
        "limampu": "50",
    },
    "vi": {
        "mười hai": "12",
        "muoi hai": "12",
        "hai mươi mốt": "21",
        "hai muoi mot": "21",
        "mười lăm": "15",
        "muoi lam": "15",
        "ba mươi": "30",
        "ba muoi": "30",
        "năm mươi": "50",
        "nam muoi": "50",
    },
}

_DECIMAL_WORDS = {
    "de": ["komma"],
    "es": ["punto", "coma"],
    "fr": ["virgule", "point"],
    "id": ["koma"],
    "ja": ["ten"],
    "ko": ["jeom"],
    "pt": ["vírgula", "virgula", "ponto"],
    "ru": ["запятая", "точка", "tochka"],
    "tl": ["punto"],
    "vi": ["phẩy", "phay", "chấm", "cham"],
}

_DATE_TRIGGERS = {
    "de": ["datum"],
    "es": ["fecha"],
    "fr": ["date"],
    "id": ["tanggal"],
    "ja": ["hiduke"],
    "ko": ["naljja"],
    "pt": ["data"],
    "ru": ["дата", "data"],
    "tl": ["petsa"],
    "vi": ["ngày", "ngay"],
}

_TIME_TRIGGERS = {
    "de": ["uhrzeit"],
    "es": ["hora"],
    "fr": ["heure"],
    "id": ["pukul"],
    "ja": ["jikan"],
    "ko": ["sigan"],
    "pt": ["hora"],
    "ru": ["время", "vremya"],
    "tl": ["oras"],
    "vi": ["giờ", "gio"],
}

_CURRENCY_WORDS = {
    "de": {"euro": "€"},
    "es": {"euro": "€", "euros": "€"},
    "fr": {"euro": "€", "euros": "€"},
    "id": {"rupiah": "Rp"},
    "ja": {"en": "¥", "yen": "¥"},
    "ko": {"won": "₩"},
    "pt": {"euro": "€", "euros": "€"},
    "ru": {"евро": "€", "rubl": "₽"},
    "tl": {"piso": "₱"},
    "vi": {"dong": "₫", "đồng": "₫"},
}

_MEASURE_WORDS = {
    "de": {"kilogramm": "kg", "meter": "m"},
    "es": {"kilogramos": "kg", "metros": "m"},
    "fr": {"kilogrammes": "kg", "metres": "m", "mètres": "m"},
    "id": {"kilogram": "kg", "meter": "m"},
    "ja": {"kiroguramu": "kg", "metoru": "m"},
    "ko": {"killogeuraem": "kg", "miteo": "m"},
    "pt": {"quilogramas": "kg", "metros": "m"},
    "ru": {"килограмм": "kg", "метров": "m"},
    "tl": {"kilo": "kg", "metro": "m"},
    "vi": {"kilogam": "kg", "met": "m", "mét": "m"},
}

_TELEPHONE_TRIGGERS = {
    "de": ["telefon"],
    "es": ["teléfono", "telefono"],
    "fr": ["téléphone", "telephone"],
    "id": ["telepon"],
    "ja": ["denwa"],
    "ko": ["jeonhwa"],
    "pt": ["telefone"],
    "ru": ["телефон", "telefon"],
    "tl": ["telepono"],
    "vi": ["điện thoại", "dien thoai"],
}

_ORDINAL_WORDS = {
    "de": {"erste": "1.", "zweite": "2."},
    "es": {"primero": "1.", "segundo": "2."},
    "fr": {"premier": "1er", "deuxième": "2e", "deuxieme": "2e"},
    "id": {"pertama": "1.", "kedua": "2."},
    "ja": {"dai ichi": "第1", "dai ni": "第2"},
    "ko": {"cheot beonjjae": "1번째", "du beonjjae": "2번째"},
    "pt": {"primeiro": "1.", "segundo": "2."},
    "ru": {"первый": "1-й", "второй": "2-й"},
    "tl": {"una": "1.", "ikalawa": "2."},
    "vi": {"thứ nhất": "1.", "thu nhat": "1.", "thứ hai": "2.", "thu hai": "2."},
}

_FRACTION_WORDS = {
    "de": {"ein halb": "1/2"},
    "es": {"un medio": "1/2"},
    "fr": {"un demi": "1/2"},
    "id": {"setengah": "1/2"},
    "ja": {"ni bun no ichi": "1/2"},
    "ko": {"i bun ui il": "1/2"},
    "pt": {"um meio": "1/2"},
    "ru": {"одна вторая": "1/2"},
    "tl": {"kalahati": "1/2"},
    "vi": {"một phần hai": "1/2", "mot phan hai": "1/2"},
}

_ROMAN_WORDS = {
    "fr": {"romain quatre": "IV"},
}

_WHITELIST_WORDS = {
    language: {"open ai": "OpenAI", "light t t s": "LightTTS"}
    for language in _DIGIT_WORDS
}


def normalize_itn(
    text: str,
    language: str,
    *,
    enable_standalone_number: bool = True,
    enable_0_to_9: bool = True,
) -> str:
    if (
        language == "ja"
        and not enable_standalone_number
        and _number_value(text, language) is not None
    ):
        return text

    normalized = _replace_map(text, _WHITELIST_WORDS[language])
    normalized = _EMAIL_SPOKEN_RE.sub(_restore_email, normalized)
    normalized = _replace_date(normalized, language)
    normalized = _replace_time(normalized, language)
    normalized = _replace_money(normalized, language)
    normalized = _replace_measure(normalized, language)
    normalized = _replace_telephone(normalized, language)
    normalized = _replace_decimal(normalized, language)
    normalized = _replace_map(normalized, _FRACTION_WORDS[language])
    normalized = _replace_map(normalized, _ORDINAL_WORDS[language])
    normalized = _replace_map(normalized, _ROMAN_WORDS.get(language, {}))
    normalized = _replace_cardinal_phrases(normalized, language)
    normalized = _replace_digit_sequences(normalized, language)
    if language == "ja" and enable_0_to_9:
        normalized = _replace_ja_standalone_digits(normalized)
    return normalized


def _restore_email(match: re.Match[str]) -> str:
    local = "".join(match.group(1).split())
    domain = "".join(match.group(2).split())
    return f"{local}@{domain}.{match.group(3).lower()}"


def _replace_date(text: str, language: str) -> str:
    day_or_month = _number_pattern(language, max_extra_digit_words=0)
    year = _number_pattern(language, max_extra_digit_words=5)
    pattern = re.compile(
        rf"(?<!\w)(?P<trigger>{_alternation(_DATE_TRIGGERS[language])})\s+"
        rf"(?P<day>{day_or_month})\s+(?P<month>{day_or_month})\s+(?P<year>{year})(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        day = _number_value(match.group("day"), language)
        month = _number_value(match.group("month"), language)
        year = _number_value(match.group("year"), language)
        if day is None or month is None or year is None:
            return match.group(0)
        return f"{match.group('trigger')} {int(year):04d}-{int(month):02d}-{int(day):02d}"

    return pattern.sub(replace, text)


def _replace_time(text: str, language: str) -> str:
    hour = _number_pattern(language, max_extra_digit_words=0)
    minute = _number_pattern(language, max_extra_digit_words=5)
    pattern = re.compile(
        rf"(?<!\w)(?P<trigger>{_alternation(_TIME_TRIGGERS[language])})\s+"
        rf"(?P<hour>{hour})\s+(?P<minute>{minute})(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        hour = _number_value(match.group("hour"), language)
        minute = _number_value(match.group("minute"), language)
        if hour is None or minute is None:
            return match.group(0)
        return f"{match.group('trigger')} {int(hour):02d}:{int(minute):02d}"

    return pattern.sub(replace, text)


def _replace_money(text: str, language: str) -> str:
    major = _number_pattern(language, max_extra_digit_words=0)
    minor = _number_pattern(language, max_extra_digit_words=5)
    pattern = re.compile(
        rf"(?<!\w)(?P<currency>{_alternation(_CURRENCY_WORDS[language])})\s+"
        rf"(?P<major>{major})(?:\s+(?P<minor>{minor}))?(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        major = _number_value(match.group("major"), language)
        minor = _number_value(match.group("minor") or "", language)
        if major is None:
            return match.group(0)
        symbol = _CURRENCY_WORDS[language][match.group("currency").lower()]
        if minor is None:
            return f"{symbol}{int(major)}"
        return f"{symbol}{int(major)}.{int(minor):02d}"

    return pattern.sub(replace, text)


def _replace_measure(text: str, language: str) -> str:
    number = _number_pattern(language, max_extra_digit_words=0)
    pattern = re.compile(
        rf"(?<!\w)(?P<value>{number})\s+(?P<unit>{_alternation(_MEASURE_WORDS[language])})(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        value = _number_value(match.group("value"), language)
        if value is None:
            return match.group(0)
        unit = _MEASURE_WORDS[language][match.group("unit").lower()]
        return f"{int(value)} {unit}"

    return pattern.sub(replace, text)


def _replace_telephone(text: str, language: str) -> str:
    digit = _digit_pattern(language)
    pattern = re.compile(
        rf"(?<!\w)(?P<trigger>{_alternation(_TELEPHONE_TRIGGERS[language])})\s+"
        rf"(?P<number>{digit}(?:\s+{digit}){{2,}})(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        return f"{match.group('trigger')} {_digits_for_phrase(match.group('number'), _DIGIT_WORDS[language])}"

    return pattern.sub(replace, text)


def _replace_decimal(text: str, language: str) -> str:
    whole = _number_pattern(language, max_extra_digit_words=0)
    fraction = _number_pattern(language, max_extra_digit_words=5)
    pattern = re.compile(
        rf"(?<!\w)(?P<whole>{whole})\s+(?P<sep>{_alternation(_DECIMAL_WORDS[language])})\s+"
        rf"(?P<fraction>{fraction})(?!\w)",
        re.IGNORECASE,
    )

    def replace(match: re.Match[str]) -> str:
        whole = _number_value(match.group("whole"), language)
        fraction = _number_value(match.group("fraction"), language)
        if whole is None or fraction is None:
            return match.group(0)
        return f"{int(whole)}.{fraction}"

    return pattern.sub(replace, text)


def _replace_cardinal_phrases(text: str, language: str) -> str:
    return _replace_map(text, _CARDINAL_PHRASES[language])


def _replace_digit_sequences(text: str, language: str) -> str:
    digit = _digit_pattern(language)
    pattern = re.compile(rf"(?<!\w){digit}(?:\s+{digit})+(?!\w)", re.IGNORECASE)
    return pattern.sub(lambda match: _digits_for_phrase(match.group(0), _DIGIT_WORDS[language]), text)


def _replace_ja_standalone_digits(text: str) -> str:
    pattern = re.compile(rf"(?<!\w){_digit_pattern('ja')}(?!\w)", re.IGNORECASE)

    def replace(match: re.Match[str]) -> str:
        return _DIGIT_WORDS["ja"][match.group(0).lower()]

    return pattern.sub(replace, text)


def _replace_map(text: str, replacements: dict[str, str]) -> str:
    if not replacements:
        return text
    pattern = re.compile(rf"(?<!\w){_alternation(replacements)}(?!\w)", re.IGNORECASE)
    return pattern.sub(lambda match: replacements[match.group(0).lower()], text)


def _number_value(raw_phrase: str, language: str) -> str | None:
    phrase = " ".join(raw_phrase.lower().split())
    if not phrase:
        return None
    mapped = _CARDINAL_PHRASES[language].get(phrase)
    if mapped is not None:
        return mapped
    words = _DIGIT_WORDS[language]
    tokens = phrase.split()
    if all(token in words for token in tokens):
        return "".join(words[token] for token in tokens)
    return None


def _digits_for_phrase(phrase: str, words: dict[str, str]) -> str:
    output = []
    for token in phrase.lower().split():
        digit = words.get(token)
        if digit is None:
            return phrase
        output.append(digit)
    return "".join(output)


def _number_pattern(language: str, *, max_extra_digit_words: int) -> str:
    phrases = _alternation(list(_CARDINAL_PHRASES[language]))
    digit = _digit_pattern(language)
    return rf"(?:{phrases}|{digit}(?:\s+{digit}){{0,{max_extra_digit_words}}})"


def _digit_pattern(language: str) -> str:
    return rf"(?:{_alternation(_DIGIT_WORDS[language])})"


def _alternation(values: dict[str, object] | list[str]) -> str:
    keys = values.keys() if isinstance(values, dict) else values
    return "|".join(re.escape(value) for value in sorted(keys, key=len, reverse=True))
