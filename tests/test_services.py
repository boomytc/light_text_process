from __future__ import annotations

import unittest

from light_text_process.schemas import ITNOptions, Num2WordsOptions, TNOptions
from light_text_process.processor import TextProcessor, _batch_rows


class FakeTextProcessingEngine:
    name = "fake"

    def __init__(self) -> None:
        self.warmed: list[tuple[str, str]] = []

    def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
        return [f"tn:{language}:{text}" for text in texts]

    def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
        standalone = int(options.enable_standalone_number)
        zero_to_nine = int(options.enable_0_to_9)
        return [f"itn:{language}:{standalone}:{zero_to_nine}:{text}" for text in texts]

    def warmup_tn(self, language: str, options: TNOptions) -> None:
        self.warmed.append(("tn", language))

    def warmup_itn(self, language: str, options: ITNOptions) -> None:
        self.warmed.append(("itn", language))


class ServiceSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_engine = FakeTextProcessingEngine()
        self.processor = TextProcessor(text_engine=self.fake_engine)

    def test_tn_and_itn_service_smoke_without_fst_build(self) -> None:
        tn = self.processor.normalize_text("abc", "zh", TNOptions())
        itn = self.processor.inverse_normalize_text(
            "one hundred twenty three",
            "en",
            ITNOptions(enable_standalone_number=False, enable_0_to_9=False),
        )

        self.assertEqual(tn.output, "tn:zh:abc")
        self.assertEqual(tn.metadata["engine"], "fake")
        self.assertEqual(itn.output, "itn:en:0:0:one hundred twenty three")

    def test_default_chinese_itn_uses_native_route(self) -> None:
        processor = TextProcessor()

        response = processor.inverse_normalize_text("二零二六年六月十五日 我有一百二十三元", "zh")

        self.assertEqual(response.output, "2026年06月15日 我有123元")
        self.assertEqual(response.metadata["engine"], "light_text_process_native")

    def test_num2words_success_and_unsupported_currency(self) -> None:
        success = self.processor.number_to_words("123", "en", Num2WordsOptions(mode="cardinal"))
        self.assertIn("one hundred", success.output)

        with self.assertRaisesRegex(ValueError, "unsupported num2words currency for ja: USD"):
            self.processor.number_to_words("1", "ja", Num2WordsOptions(mode="currency", currency="USD"))

    def test_num2words_batch_keeps_input_errors_per_row(self) -> None:
        response = self.processor.batch(
            "num2words",
            ["12", "not-a-number"],
            "en",
            TNOptions(),
            ITNOptions(),
            Num2WordsOptions(mode="cardinal"),
        )

        self.assertEqual(response.success_count, 1)
        self.assertEqual(response.error_count, 1)
        self.assertEqual(response.items[0].output, "twelve")
        self.assertIn("invalid number", response.items[1].error or "")

    def test_warmup_uses_configured_languages(self) -> None:
        result = self.processor.warmup(tn_languages=["zh"], itn_languages=["en"])

        self.assertEqual(result, {"tn": ["zh"], "itn": ["en"]})
        self.assertEqual(
            self.fake_engine.warmed,
            [("tn", "zh"), ("itn", "en")],
        )


class BatchFallbackTests(unittest.TestCase):
    def test_batch_fallback_returns_mixed_input_errors(self) -> None:
        def processor(items: list[str]) -> list[str]:
            if len(items) > 1:
                raise ValueError("batch failed")
            if items[0] == "bad":
                raise ValueError("bad input")
            return [items[0].upper()]

        rows = _batch_rows(["ok", "bad"], processor)

        self.assertEqual(rows[0].output, "OK")
        self.assertEqual(rows[1].error, "bad input")

    def test_batch_fallback_keeps_all_input_errors_per_row(self) -> None:
        def processor(items: list[str]) -> list[str]:
            raise ValueError(f"bad input: {items[0]}")

        rows = _batch_rows(["bad-1", "bad-2"], processor)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].error, "bad input: bad-1")
        self.assertEqual(rows[1].error, "bad input: bad-2")

    def test_batch_fallback_reraises_system_errors(self) -> None:
        def processor(items: list[str]) -> list[str]:
            raise RuntimeError("missing pynini")

        with self.assertRaisesRegex(RuntimeError, "missing pynini"):
            _batch_rows(["a", "b"], processor)


if __name__ == "__main__":
    unittest.main()
