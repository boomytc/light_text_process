from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


PROJECT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_DIR / "scripts" / "validate_rules.py"


def load_validate_rules_module():
    spec = importlib.util.spec_from_file_location("validate_rules", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("validate_rules.py cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_rules = load_validate_rules_module()


class RuleCaseDataTests(unittest.TestCase):
    def test_rule_cases_are_split_by_language_and_operation(self) -> None:
        cases_dir = validate_rules.DEFAULT_CASES_DIR

        self.assertTrue(cases_dir.is_dir())
        self.assertFalse((PROJECT_DIR / "data" / "rule_cases.json").exists())
        self.assertEqual(
            sorted(path.name for path in cases_dir.glob("*.json")),
            sorted(filename for filename, _language, _operation in validate_rules.CASE_FILES),
        )

        for filename, language, operation in validate_rules.CASE_FILES:
            cases = validate_rules.load_cases(cases_dir)
            matching_cases = [
                case
                for case in cases
                if case.language == language and case.operation == operation
            ]
            self.assertGreater(len(matching_cases), 0, filename)

    def test_rule_cases_cover_public_tn_itn_routes(self) -> None:
        cases = validate_rules.load_cases(validate_rules.DEFAULT_CASES_DIR)

        self.assertGreater(len(cases), 0)
        self.assertEqual(
            {case.language for case in cases},
            {"de", "en", "es", "fr", "id", "ja", "ko", "pt", "ru", "tl", "vi", "zh"},
        )
        self.assertEqual({case.operation for case in cases}, {"tn", "itn"})

    def test_rule_case_filters_support_language_operation_category_and_id(self) -> None:
        cases = validate_rules.load_cases(validate_rules.DEFAULT_CASES_DIR)
        args = validate_rules.build_parser().parse_args(
            [
                "--language",
                "zh",
                "--operation",
                "tn",
                "--category",
                "measure",
                "--case",
                "tn-zh-square-meter-word",
            ]
        )

        selected = validate_rules.filter_cases(cases, args)

        self.assertEqual([case.id for case in selected], ["tn-zh-square-meter-word"])

    def test_native_engine_validates_filtered_rule_cases(self) -> None:
        cases = validate_rules.load_cases(validate_rules.DEFAULT_CASES_DIR)
        args = validate_rules.build_parser().parse_args(
            [
                "--language",
                "zh",
                "--operation",
                "itn",
                "--engine",
                "native",
            ]
        )
        selected = validate_rules.filter_cases(cases, args)

        results = validate_rules.run_cases(selected, engine=args.engine)

        self.assertGreater(len(results), 0)
        self.assertTrue(all(result.passed for result in results))


if __name__ == "__main__":
    unittest.main()
