from __future__ import annotations

import asyncio
import unittest

from fastapi import HTTPException

from api.routes import (
    batch_process,
    capabilities,
    inverse_normalize_text,
    normalize_text,
    number_to_words,
)
from light_text_process.schemas import BatchRequest, ITNRequest, Num2WordsRequest, TNRequest


class NativeApiTests(unittest.TestCase):
    def test_capabilities_return_native_surface(self) -> None:
        data = asyncio.run(capabilities())

        self.assertIn("operations", data)
        self.assertIn("tn", data["operations"])
        self.assertIn("itn", data["operations"])
        self.assertIn("num2words", data["operations"])
        self.assertIn("zh", data["operations"]["tn"]["languages"])
        self.assertIn("en", data["operations"]["num2words"]["languages"])

    def test_tn_endpoint_uses_native_schema(self) -> None:
        response = asyncio.run(
            normalize_text(
                TNRequest(
                    text="今天是 2026 年 6 月 15 日。",
                    language="zh",
                )
            )
        )

        self.assertEqual(response.operation, "tn")
        self.assertEqual(response.language, "zh")
        self.assertTrue(response.output)

    def test_itn_endpoint_uses_native_schema(self) -> None:
        response = asyncio.run(
            inverse_normalize_text(
                ITNRequest(
                    text="二零二六年六月十五日",
                    language="zh",
                )
            )
        )

        self.assertEqual(response.operation, "itn")
        self.assertEqual(response.language, "zh")
        self.assertTrue(response.output)

    def test_num2words_endpoint_uses_native_schema(self) -> None:
        response = asyncio.run(number_to_words(Num2WordsRequest(number="123", language="en")))

        self.assertEqual(response.operation, "num2words")
        self.assertEqual(response.output, "one hundred and twenty-three")

    def test_batch_endpoint_returns_row_results(self) -> None:
        response = asyncio.run(
            batch_process(
                BatchRequest(
                    operation="num2words",
                    items=["123", "bad-number"],
                    language="en",
                )
            )
        )

        self.assertEqual(response.operation, "num2words")
        self.assertEqual(response.success_count, 1)
        self.assertEqual(response.error_count, 1)

    def test_value_errors_map_to_http_400(self) -> None:
        with self.assertRaises(HTTPException) as caught:
            asyncio.run(number_to_words(Num2WordsRequest(number="123", language="not-a-language")))

        self.assertEqual(caught.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
