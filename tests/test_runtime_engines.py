from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

from light_text_process.runtime.fun_text_processing import FunTextProcessingEngine
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
