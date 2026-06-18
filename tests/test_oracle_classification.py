from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


PROJECT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_DIR / "scripts" / "fun_text_processing_oracle.py"


def load_oracle_module():
    spec = importlib.util.spec_from_file_location("fun_text_processing_oracle", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("fun_text_processing_oracle.py cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


oracle_module = load_oracle_module()


class OracleClassificationTests(unittest.TestCase):
    def test_matching_outputs_are_always_match(self) -> None:
        current = oracle_module.EngineOutput(output="123", error=None)
        oracle = oracle_module.EngineOutput(output="123", error=None)

        status = oracle_module.classify(
            current,
            oracle,
            reviewed_status="accepted-improvement",
        )

        self.assertEqual(status, "match")

    def test_unreviewed_output_diff_is_regression(self) -> None:
        current = oracle_module.EngineOutput(output="one", error=None)
        oracle = oracle_module.EngineOutput(output="1", error=None)

        status = oracle_module.classify(current, oracle)

        self.assertEqual(status, "regression")

    def test_current_error_is_unsupported_gap_by_default(self) -> None:
        current = oracle_module.EngineOutput(output=None, error="unsupported")
        oracle = oracle_module.EngineOutput(output="1", error=None)

        status = oracle_module.classify(current, oracle)

        self.assertEqual(status, "unsupported-gap")

    def test_reviewed_diff_can_be_accepted_improvement(self) -> None:
        current = oracle_module.EngineOutput(output="better", error=None)
        oracle = oracle_module.EngineOutput(output="old", error=None)

        status = oracle_module.classify(
            current,
            oracle,
            reviewed_status="accepted-improvement",
        )

        self.assertEqual(status, "accepted-improvement")

    def test_reviewed_golden_expected_diff_is_accepted_improvement(self) -> None:
        current = oracle_module.EngineOutput(output="better", error=None)
        oracle = oracle_module.EngineOutput(output="old", error=None)

        status = oracle_module.classify(
            current,
            oracle,
            expected="better",
            reviewed_status="accepted-improvement",
        )

        self.assertEqual(status, "accepted-improvement")

    def test_expected_without_reviewed_status_is_regression(self) -> None:
        current = oracle_module.EngineOutput(output="better", error=None)
        oracle = oracle_module.EngineOutput(output="old", error=None)

        status = oracle_module.classify(current, oracle, expected="better")

        self.assertEqual(status, "regression")

    def test_current_output_that_misses_golden_expected_is_regression(self) -> None:
        current = oracle_module.EngineOutput(output="unexpected", error=None)
        oracle = oracle_module.EngineOutput(output="old", error=None)

        status = oracle_module.classify(current, oracle, expected="better")

        self.assertEqual(status, "regression")

    def test_accepted_improvement_case_requires_expected_output(self) -> None:
        raw_case = {
            "id": "case-1",
            "operation": "tn",
            "language": "en",
            "category": "electronic",
            "input": "path /tmp/a",
            "oracle_status": "accepted-improvement",
            "oracle_note": "native output is reviewed as better",
        }

        with self.assertRaisesRegex(ValueError, "requires expected output"):
            oracle_module.parse_case(raw_case, Path("cases.json"), 1)

    def test_accepted_improvement_case_requires_note(self) -> None:
        raw_case = {
            "id": "case-1",
            "operation": "tn",
            "language": "en",
            "category": "electronic",
            "input": "path /tmp/a",
            "expected": "path slash tmp slash a",
            "oracle_status": "accepted-improvement",
        }

        with self.assertRaisesRegex(ValueError, "requires oracle_note"):
            oracle_module.parse_case(raw_case, Path("cases.json"), 1)

    def test_report_includes_route_and_category_summary(self) -> None:
        comparisons = [
            oracle_module.Comparison(
                id="case-1",
                operation="tn",
                language="en",
                category="electronic",
                input="a",
                expected="a",
                current=oracle_module.EngineOutput(output="a", error=None),
                oracle=oracle_module.EngineOutput(output="a", error=None),
                status="match",
                note=None,
            ),
            oracle_module.Comparison(
                id="case-2",
                operation="tn",
                language="en",
                category="money",
                input="$1",
                expected="one dollar",
                current=oracle_module.EngineOutput(output="one dollar", error=None),
                oracle=oracle_module.EngineOutput(output="one dollar", error=None),
                status="match",
                note=None,
            ),
        ]

        report = oracle_module.build_report(Path("/tmp/fun_text_processing"), comparisons, 0.1)

        self.assertEqual(
            report["route_summary"],
            [
                {
                    "operation": "tn",
                    "language": "en",
                    "total": 2,
                    "status_counts": {"match": 2},
                }
            ],
        )
        self.assertEqual(len(report["category_summary"]), 2)


if __name__ == "__main__":
    unittest.main()
