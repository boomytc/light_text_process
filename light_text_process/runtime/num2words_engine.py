from __future__ import annotations

from decimal import Decimal, InvalidOperation

from light_text_process.capabilities import num2words_default_currency
from light_text_process.schemas import Num2WordsOptions


class Num2WordsEngine:
    def convert(self, value: str, language: str, options: Num2WordsOptions) -> str:
        from num2words import num2words

        kwargs = {}
        if options.mode == "currency":
            currency = options.currency.upper() if options.currency else num2words_default_currency(language)
            if currency:
                kwargs["currency"] = currency
        parsed_value = _parse_number(value)
        try:
            return num2words(parsed_value, lang=language, to=options.mode, **kwargs)
        except (NotImplementedError, TypeError, ValueError) as exc:
            message = str(exc) or "num2words conversion failed"
            raise ValueError(f"unsupported num2words combination for {language}: {message}") from exc


def _parse_number(value: str) -> int | Decimal:
    raw = value.strip()
    if not raw:
        raise ValueError("number is required")
    try:
        if any(marker in raw for marker in (".", "e", "E")):
            return Decimal(raw)
        return int(raw)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid number: {value}") from exc
