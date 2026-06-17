from __future__ import annotations

import unittest

from light_text_process.capabilities import build_capabilities
from light_text_process.capabilities import ITN_LANGUAGES, TN_LANGUAGES


class CapabilityTests(unittest.TestCase):
    def test_tn_and_itn_capabilities_include_vendor_languages(self) -> None:
        self.assertEqual(
            TN_LANGUAGES,
            {"de": "德语", "en": "英语", "es": "西班牙语", "ru": "俄语", "zh": "中文"},
        )
        self.assertEqual(
            ITN_LANGUAGES,
            {
                "de": "德语",
                "en": "英语",
                "es": "西班牙语",
                "fr": "法语",
                "id": "印尼语",
                "ja": "日语",
                "ko": "韩语",
                "pt": "葡萄牙语",
                "ru": "俄语",
                "tl": "他加禄语",
                "vi": "越南语",
                "zh": "中文",
            },
        )

    def test_capabilities_include_language_scoped_options(self) -> None:
        capabilities = build_capabilities()

        tn = capabilities["operations"]["tn"]
        self.assertEqual(tn["display_label"], "文本转读法")
        self.assertIn("de", tn["languages"])
        self.assertIn("ru", tn["languages"])
        self.assertEqual(tn["languages"]["zh"], "中文")
        self.assertNotIn("cache_enabled", tn["options"])
        self.assertNotIn("overwrite_cache", tn["options"])
        self.assertNotIn("cache_enabled", tn["option_details"])
        self.assertNotIn("overwrite_cache", tn["option_details"])

        itn = capabilities["operations"]["itn"]
        self.assertEqual(itn["display_label"], "读法转文本")
        self.assertIn("ja", itn["languages"])
        self.assertIn("vi", itn["languages"])
        self.assertEqual(itn["language_options"], {"ja": ["enable_standalone_number", "enable_0_to_9"]})
        self.assertEqual(itn["options"], [])
        self.assertEqual(itn["option_details"], {})
        self.assertNotIn("cache_enabled", itn["options"])
        self.assertNotIn("overwrite_cache", itn["options"])
        self.assertNotIn("cache_enabled", itn["option_details"])
        self.assertNotIn("overwrite_cache", itn["option_details"])

        num2words = capabilities["operations"]["num2words"]
        self.assertEqual(num2words["display_label"], "数字转外语词")
        self.assertEqual(num2words["modes"]["currency"], "货币读法")
        self.assertIn("modes_by_language", num2words)
        self.assertIn("currencies_by_language", num2words)
        self.assertIn("currency", num2words["modes_by_language"]["ja"])
        self.assertEqual(num2words["currencies_by_language"]["ja"], ["JPY"])


if __name__ == "__main__":
    unittest.main()
