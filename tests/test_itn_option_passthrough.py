from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import patch

from light_text_process.paths import ensure_runtime_paths


ensure_runtime_paths()

from fun_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer


class ItnOptionPassthroughTests(unittest.TestCase):
    def test_japanese_itn_options_are_passed_to_classifier(self) -> None:
        calls: list[dict[str, object]] = []

        class FakeClassifyFst:
            def __init__(self, **kwargs: object) -> None:
                calls.append(kwargs)

        class FakeVerbalizeFinalFst:
            pass

        classify_module = types.ModuleType("tokenize_and_classify")
        classify_module.ClassifyFst = FakeClassifyFst
        verbalize_module = types.ModuleType("verbalize_final")
        verbalize_module.VerbalizeFinalFst = FakeVerbalizeFinalFst

        fake_modules = {
            "fun_text_processing.inverse_text_normalization.ja.taggers.tokenize_and_classify": classify_module,
            "fun_text_processing.inverse_text_normalization.ja.verbalizers.verbalize_final": verbalize_module,
        }
        with patch.dict(sys.modules, fake_modules):
            InverseNormalizer(
                lang="ja",
                cache_dir="cache",
                overwrite_cache=True,
                enable_standalone_number=False,
                enable_0_to_9=False,
            )

        self.assertEqual(calls, [
            {
                "cache_dir": "cache",
                "overwrite_cache": True,
                "enable_standalone_number": False,
                "enable_0_to_9": False,
            }
        ])


if __name__ == "__main__":
    unittest.main()
