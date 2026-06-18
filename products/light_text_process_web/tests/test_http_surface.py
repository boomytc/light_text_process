from __future__ import annotations

import unittest

from app import create_app
from tests.asgi_client import request


class HttpSurfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()

    def test_app_can_be_created(self) -> None:
        self.assertEqual(self.app.title, "Light Text Process Web")

    def test_health(self) -> None:
        response = request(self.app, "GET", "/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_capabilities(self) -> None:
        response = request(self.app, "GET", "/api/v1/capabilities")

        self.assertEqual(response.status_code, 200)
        operations = response.json()["operations"]
        self.assertIn("zh", operations["tn"]["languages"])
        self.assertIn("en", operations["tn"]["languages"])
        self.assertIn("zh", operations["itn"]["languages"])
        self.assertIn("en", operations["itn"]["languages"])
        self.assertIn("en", operations["num2words"]["languages"])

    def test_tn_zh_and_en(self) -> None:
        zh = request(
            self.app,
            "POST",
            "/api/v1/tn",
            {"text": "今天是 2026 年 6 月 15 日。", "language": "zh"},
        )
        en = request(
            self.app,
            "POST",
            "/api/v1/tn",
            {"text": "I paid $12.50 on 06/15/2026.", "language": "en"},
        )

        self.assertEqual(zh.status_code, 200)
        self.assertEqual(zh.json()["operation"], "tn")
        self.assertEqual(en.status_code, 200)
        self.assertEqual(en.json()["operation"], "tn")

    def test_itn_zh_and_en(self) -> None:
        zh = request(
            self.app,
            "POST",
            "/api/v1/itn",
            {"text": "二零二六年六月十五日", "language": "zh"},
        )
        en = request(
            self.app,
            "POST",
            "/api/v1/itn",
            {
                "text": "I paid twelve dollars and fifty cents on june fifteenth twenty twenty six",
                "language": "en",
            },
        )

        self.assertEqual(zh.status_code, 200)
        self.assertEqual(zh.json()["operation"], "itn")
        self.assertEqual(en.status_code, 200)
        self.assertEqual(en.json()["operation"], "itn")

    def test_num2words(self) -> None:
        response = request(
            self.app,
            "POST",
            "/api/v1/num2words",
            {"number": "123", "language": "en"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["output"], "one hundred and twenty-three")

    def test_batch_mixed_results(self) -> None:
        response = request(
            self.app,
            "POST",
            "/api/v1/batch",
            {"operation": "num2words", "items": ["123", "bad-number"], "language": "en"},
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success_count"], 1)
        self.assertEqual(data["error_count"], 1)

    def test_ui_template_and_assets_render(self) -> None:
        index = request(self.app, "GET", "/")
        js = request(self.app, "GET", "/static/js/app.js")
        css = request(self.app, "GET", "/static/css/app.css")
        examples = request(self.app, "GET", "/static/data/examples.json")
        partial = request(self.app, "GET", "/partials/capabilities")

        self.assertEqual(index.status_code, 200)
        self.assertIn("api-request-json", index.text)
        self.assertEqual(js.status_code, 200)
        self.assertIn("buildBatchPayload", js.text)
        self.assertEqual(css.status_code, 200)
        self.assertIn(".view-tabs", css.text)
        self.assertEqual(examples.status_code, 200)
        self.assertGreaterEqual(len(examples.json()), 1)
        self.assertEqual(partial.status_code, 200)
        self.assertIn("能力", partial.text)

    def test_value_error_maps_to_400(self) -> None:
        response = request(
            self.app,
            "POST",
            "/api/v1/tn",
            {"text": "hello", "language": "not-a-language"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("unsupported", response.json()["detail"])

    def test_unexpected_error_maps_to_500(self) -> None:
        from api import routes

        original = routes.processor.number_to_words

        def raise_unexpected(*_args: object) -> object:
            raise RuntimeError("forced unexpected failure")

        routes.processor.number_to_words = raise_unexpected
        try:
            response = request(
                self.app,
                "POST",
                "/api/v1/num2words",
                {"number": "123", "language": "en"},
            )
        finally:
            routes.processor.number_to_words = original

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "forced unexpected failure")


if __name__ == "__main__":
    unittest.main()
