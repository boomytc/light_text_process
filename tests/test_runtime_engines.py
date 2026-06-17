from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

from light_text_process.runtime.base import CompositeTextProcessingEngine, NativeRouteUnsupportedError
from light_text_process.runtime.native import NativeTextProcessingEngine
from light_text_process.schemas import ITNOptions, TNOptions


PROJECT_DIR = Path(__file__).resolve().parents[1]


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
            engine.normalize(["abc"], "ja", TNOptions())

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

    def test_native_english_tn_route_runs_without_vendor_import(self) -> None:
        engine = NativeTextProcessingEngine()

        output = engine.normalize(["Email test@example.com and IP 192.168.0.1."], "en", TNOptions())

        self.assertEqual(output, ["Email test at example dot com and IP one nine two dot one six eight dot zero dot one."])

    def test_native_engine_does_not_import_vendor_backend(self) -> None:
        code = """
import sys
from light_text_process.runtime.native import NativeTextProcessingEngine
from light_text_process.schemas import ITNOptions

engine = NativeTextProcessingEngine()
engine.inverse_normalize(["电话一三八零零一三八零零零"], "zh", ITNOptions())
vendor_module = "_".join(("fun", "text", "processing"))
runtime_module = ".".join(("light_text_process", "runtime", vendor_module))
blocked = [
    name
    for name in sys.modules
    if name == runtime_module
    or name == vendor_module
    or name.startswith(f"{vendor_module}.")
]
print(blocked)
"""

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=PROJECT_DIR,
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "[]")


if __name__ == "__main__":
    unittest.main()
