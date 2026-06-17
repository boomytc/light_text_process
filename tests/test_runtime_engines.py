from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

from light_text_process.runtime.fun_text_processing import FunTextProcessingEngine
from light_text_process.runtime.base import CompositeTextProcessingEngine, NativeRouteUnsupportedError
from light_text_process.runtime.native import NativeTextProcessingEngine
from light_text_process.schemas import ITNOptions, TNOptions


class RuntimeEngineCacheTests(unittest.TestCase):
    def test_tn_overwrite_clears_process_cache(self) -> None:
        class FakeNormalizer:
            def __init__(self, **kwargs: object) -> None:
                pass

            def normalize_list(self, texts: list[str], **kwargs: object) -> list[str]:
                return texts

        fake_module = types.ModuleType("normalize")
        fake_module.Normalizer = FakeNormalizer

        with (
            patch.dict(sys.modules, {"fun_text_processing.text_normalization.normalize": fake_module}),
            patch("light_text_process.runtime.fun_text_processing.clear_tn_cache") as clear_cache,
        ):
            output = FunTextProcessingEngine().normalize(["abc"], "zh", TNOptions(overwrite_cache=True))

        self.assertEqual(output, ["abc"])
        clear_cache.assert_called_once_with()


class RuntimeEngineBoundaryTests(unittest.TestCase):
    def test_composite_routes_selected_native_pairs_only(self) -> None:
        class FakeEngine:
            def __init__(self, name: str) -> None:
                self.name = name

            def normalize(self, texts: list[str], language: str, options: TNOptions) -> list[str]:
                return [f"{self.name}:tn:{language}:{text}" for text in texts]

            def inverse_normalize(self, texts: list[str], language: str, options: ITNOptions) -> list[str]:
                return [f"{self.name}:itn:{language}:{text}" for text in texts]

            def warmup_tn(self, language: str, options: TNOptions | None = None) -> None:
                return None

            def warmup_itn(self, language: str, options: ITNOptions | None = None) -> None:
                return None

        engine = CompositeTextProcessingEngine(
            native_engine=FakeEngine("native"),
            fallback_engine=FakeEngine("fallback"),
            native_routes={("itn", "zh")},
        )

        self.assertEqual(engine.inverse_normalize(["一二三"], "zh", ITNOptions()), ["native:itn:zh:一二三"])
        self.assertEqual(engine.last_engine_name, "native")
        self.assertEqual(engine.normalize(["123"], "zh", TNOptions()), ["fallback:tn:zh:123"])
        self.assertEqual(engine.last_engine_name, "fallback")

    def test_native_skeleton_fails_visibly_for_unenabled_routes(self) -> None:
        engine = NativeTextProcessingEngine()

        with self.assertRaisesRegex(NativeRouteUnsupportedError, "native TN route is not enabled"):
            engine.normalize(["abc"], "en", TNOptions())

        with self.assertRaisesRegex(NativeRouteUnsupportedError, "native ITN route is not enabled"):
            engine.inverse_normalize(["abc"], "ja", ITNOptions())

    def test_native_chinese_itn_route_runs_without_vendor_import(self) -> None:
        engine = NativeTextProcessingEngine()

        output = engine.inverse_normalize(["电话一三八零零一三八零零零"], "zh", ITNOptions())

        self.assertEqual(output, ["电话13800138000"])

    def test_native_english_itn_route_runs_without_vendor_import(self) -> None:
        engine = NativeTextProcessingEngine()

        output = engine.inverse_normalize(["email t e s t at example dot com"], "en", ITNOptions())

        self.assertEqual(output, ["email test@example.com"])

    def test_native_chinese_tn_route_runs_without_vendor_import(self) -> None:
        engine = NativeTextProcessingEngine()

        output = engine.normalize(["今天是 2026年6月15日。"], "zh", TNOptions())

        self.assertEqual(output, ["今天是 二零二六年六月十五日。"])

    def test_itn_overwrite_clears_process_cache(self) -> None:
        class FakeInverseNormalizer:
            def __init__(self, **kwargs: object) -> None:
                pass

            def inverse_normalize_list(self, texts: list[str]) -> list[str]:
                return texts

        fake_module = types.ModuleType("inverse_normalize")
        fake_module.InverseNormalizer = FakeInverseNormalizer

        with (
            patch.dict(
                sys.modules,
                {"fun_text_processing.inverse_text_normalization.inverse_normalize": fake_module},
            ),
            patch("light_text_process.runtime.fun_text_processing.clear_itn_cache") as clear_cache,
        ):
            output = FunTextProcessingEngine().inverse_normalize(
                ["abc"],
                "zh",
                ITNOptions(overwrite_cache=True),
            )

        self.assertEqual(output, ["abc"])
        clear_cache.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
