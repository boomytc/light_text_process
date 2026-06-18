from __future__ import annotations

import json
from pathlib import Path
import unittest

from light_text_process import TextProcessor
from light_text_process.capabilities import build_capabilities
from light_text_process.schemas import ITNOptions, Num2WordsOptions, TNOptions


class ExamplesDataTests(unittest.TestCase):
    def test_examples_are_supported_and_match_native_outputs(self) -> None:
        processor = TextProcessor()
        capabilities = build_capabilities()["operations"]
        examples = json.loads(Path("static/data/examples.json").read_text(encoding="utf-8"))
        seen_ids: set[str] = set()

        for example in examples:
            with self.subTest(example=example["id"]):
                self.assertNotIn(example["id"], seen_ids)
                seen_ids.add(example["id"])
                operation = example["operation"]
                language = example["language"]
                self.assertIn(operation, capabilities)
                self.assertIn(language, capabilities[operation]["languages"])
                self.assertEqual(_run_example(processor, example), example["expected"])


def _run_example(processor: TextProcessor, example: dict[str, object]) -> str:
    operation = str(example["operation"])
    language = str(example["language"])
    text = str(example["input"])
    options = example.get("options") or {}

    if operation == "tn":
        return processor.normalize_text(text, language, TNOptions(**options)).output
    if operation == "itn":
        return processor.inverse_normalize_text(text, language, ITNOptions(**options)).output
    if operation == "num2words":
        return processor.number_to_words(text, language, Num2WordsOptions(**options)).output
    raise AssertionError(f"unsupported example operation: {operation}")


if __name__ == "__main__":
    unittest.main()
