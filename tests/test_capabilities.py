from __future__ import annotations

import unittest

from light_text_process.capabilities import build_capabilities
from light_text_process.capabilities import ITN_LANGUAGES, TN_LANGUAGES


class CapabilityTests(unittest.TestCase):
    def test_tn_and_itn_capabilities_include_retained_first_party_languages(self) -> None:
        self.assertEqual(
            TN_LANGUAGES,
            {"en": "英语", "zh": "中文"},
        )
        self.assertEqual(
            ITN_LANGUAGES,
            {"en": "英语", "zh": "中文"},
        )

    def test_capabilities_include_language_scoped_options(self) -> None:
        capabilities = build_capabilities()

        tn = capabilities["operations"]["tn"]
        self.assertEqual(tn["display_label"], "文本转读法")
        self.assertEqual(set(tn["languages"]), {"en", "zh"})
        self.assertEqual(tn["languages"]["zh"], "中文")
        self.assertEqual(tn["options"], [])
        self.assertEqual(tn["option_details"], {})

        itn = capabilities["operations"]["itn"]
        self.assertEqual(itn["display_label"], "读法转文本")
        self.assertEqual(set(itn["languages"]), {"en", "zh"})
        self.assertEqual(itn["language_options"], {})
        self.assertEqual(itn["options"], [])
        self.assertEqual(itn["option_details"], {})

        num2words = capabilities["operations"]["num2words"]
        self.assertEqual(num2words["display_label"], "数字转外语词")
        self.assertEqual(num2words["modes"]["currency"], "货币读法")
        self.assertIn("modes_by_language", num2words)
        self.assertIn("currencies_by_language", num2words)
        self.assertIn("currency", num2words["modes_by_language"]["ja"])
        self.assertEqual(num2words["currencies_by_language"]["ja"], ["JPY"])


if __name__ == "__main__":
    unittest.main()
