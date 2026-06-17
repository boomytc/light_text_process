from __future__ import annotations

import argparse
import json
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
import sys
from time import perf_counter
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CASES_DIR = PROJECT_DIR / "data" / "rule_cases"
CASE_FILES = (
    ("de_itn.json", "de", "itn"),
    ("de_tn.json", "de", "tn"),
    ("en_tn.json", "en", "tn"),
    ("en_itn.json", "en", "itn"),
    ("es_itn.json", "es", "itn"),
    ("es_tn.json", "es", "tn"),
    ("fr_itn.json", "fr", "itn"),
    ("id_itn.json", "id", "itn"),
    ("ja_itn.json", "ja", "itn"),
    ("ko_itn.json", "ko", "itn"),
    ("pt_itn.json", "pt", "itn"),
    ("ru_itn.json", "ru", "itn"),
    ("ru_tn.json", "ru", "tn"),
    ("tl_itn.json", "tl", "itn"),
    ("vi_itn.json", "vi", "itn"),
    ("zh_tn.json", "zh", "tn"),
    ("zh_itn.json", "zh", "itn"),
)
SUPPORTED_LANGUAGES = {"de", "en", "es", "fr", "id", "ja", "ko", "pt", "ru", "tl", "vi", "zh"}
SUPPORTED_OPERATIONS = {"tn", "itn"}

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from light_text_process.schemas import ITNOptions, Num2WordsOptions, TNOptions
from light_text_process.processor import TextProcessor
from light_text_process.runtime.native import NativeTextProcessingEngine


@dataclass(frozen=True)
class RuleCase:
    id: str
    operation: str
    language: str
    category: str
    input: str
    expected: str
    options: dict[str, Any]


@dataclass(frozen=True)
class RuleResult:
    case: RuleCase
    actual: str | None
    error: str | None

    @property
    def passed(self) -> bool:
        return self.error is None and self.actual == self.case.expected


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        cases = filter_cases(load_cases(args.cases), args)
        if args.list:
            print_cases(cases)
            return 0
        if not cases:
            print("error: no rule cases selected", file=sys.stderr)
            return 2
        started = perf_counter()
        results = run_cases(cases, engine=args.engine)
        elapsed = perf_counter() - started
        print_results(results, verbose=args.verbose)
        print_summary(results, elapsed)
        return 0 if all(result.passed for result in results) else 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate zh/en TN and ITN rule regression cases.",
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=DEFAULT_CASES_DIR,
        help=f"rule case JSON directory (default: {DEFAULT_CASES_DIR})",
    )
    parser.add_argument("--language", action="append", choices=sorted(SUPPORTED_LANGUAGES))
    parser.add_argument("--operation", action="append", choices=sorted(SUPPORTED_OPERATIONS))
    parser.add_argument("--category", action="append", help="case category to include")
    parser.add_argument("--case", action="append", dest="case_ids", help="case id to include")
    parser.add_argument(
        "--engine",
        choices=("default", "native"),
        default="default",
        help="text processing engine to validate (default: default)",
    )
    parser.add_argument("--list", action="store_true", help="list selected cases without running them")
    parser.add_argument("--verbose", action="store_true", help="print passing case outputs too")
    return parser


def load_cases(path: Path) -> list[RuleCase]:
    if not path.is_dir():
        raise ValueError(f"rule cases path must be a directory: {path}")

    raw_cases: list[Any] = []
    for filename, expected_language, expected_operation in CASE_FILES:
        case_path = path / filename
        if not case_path.is_file():
            raise ValueError(f"missing rule case file: {case_path}")
        file_cases = json.loads(case_path.read_text(encoding="utf-8"))
        if not isinstance(file_cases, list) or not file_cases:
            raise ValueError(f"rule case file must contain a non-empty JSON list: {case_path}")
        for index, raw_case in enumerate(file_cases, start=1):
            if not isinstance(raw_case, dict):
                raise ValueError(f"{case_path} case {index} must be an object")
            if raw_case.get("language") != expected_language or raw_case.get("operation") != expected_operation:
                raise ValueError(
                    f"{case_path} case {index} must use {expected_language}/{expected_operation}: "
                    f"{raw_case.get('id', '<missing id>')}"
                )
        raw_cases.extend(file_cases)

    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("rule case directory must contain at least one case")

    cases = []
    seen_ids: set[str] = set()
    for index, raw_case in enumerate(raw_cases, start=1):
        if not isinstance(raw_case, dict):
            raise ValueError(f"case {index} must be an object")
        case = parse_case(raw_case, index)
        if case.id in seen_ids:
            raise ValueError(f"duplicate case id: {case.id}")
        seen_ids.add(case.id)
        cases.append(case)
    return cases


def parse_case(raw_case: dict[str, Any], index: int) -> RuleCase:
    values = {}
    for field in ("id", "operation", "language", "category", "input", "expected"):
        value = raw_case.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"case {index} field {field!r} must be a non-empty string")
        values[field] = value

    operation = values["operation"]
    language = values["language"]
    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(f"case {values['id']} uses unsupported operation: {operation}")
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"case {values['id']} uses unsupported language: {language}")

    options = raw_case.get("options", {})
    if not isinstance(options, dict):
        raise ValueError(f"case {values['id']} options must be an object")
    if operation == "tn":
        TNOptions(**options)
    else:
        ITNOptions(**options)

    return RuleCase(
        id=values["id"],
        operation=operation,
        language=language,
        category=values["category"],
        input=values["input"],
        expected=values["expected"],
        options=options,
    )


def filter_cases(cases: Iterable[RuleCase], args: argparse.Namespace) -> list[RuleCase]:
    selected = list(cases)
    if args.language:
        languages = set(args.language)
        selected = [case for case in selected if case.language in languages]
    if args.operation:
        operations = set(args.operation)
        selected = [case for case in selected if case.operation in operations]
    if args.category:
        categories = set(args.category)
        selected = [case for case in selected if case.category in categories]
    if args.case_ids:
        case_ids = set(args.case_ids)
        selected = [case for case in selected if case.id in case_ids]
        missing = sorted(case_ids - {case.id for case in selected})
        if missing:
            raise ValueError(f"unknown case id: {', '.join(missing)}")
    return selected


def run_cases(
    cases: Sequence[RuleCase],
    *,
    engine: str = "default",
) -> list[RuleResult]:
    if engine == "native":
        service = TextProcessor(text_engine=NativeTextProcessingEngine())
    elif engine == "default":
        service = TextProcessor()
    else:
        raise ValueError(f"unsupported validation engine: {engine}")
    results: list[RuleResult] = []
    for group_cases in grouped_cases(cases).values():
        group_results = run_group(service, group_cases)
        results.extend(group_results)
    result_by_id = {result.case.id: result for result in results}
    return [result_by_id[case.id] for case in cases]


def grouped_cases(cases: Sequence[RuleCase]) -> dict[tuple[str, str, str], list[RuleCase]]:
    groups: dict[tuple[str, str, str], list[RuleCase]] = defaultdict(list)
    for case in cases:
        options_key = json.dumps(case.options, sort_keys=True, ensure_ascii=False)
        groups[(case.operation, case.language, options_key)].append(case)
    return dict(groups)


def run_group(
    service: TextProcessor,
    cases: Sequence[RuleCase],
) -> list[RuleResult]:
    first = cases[0]
    tn_options = TNOptions()
    itn_options = ITNOptions()
    if first.operation == "tn":
        tn_options = TNOptions(**first.options)
    else:
        itn_options = ITNOptions(**first.options)

    try:
        response = service.batch(
            first.operation,
            [case.input for case in cases],
            first.language,
            tn_options,
            itn_options,
            Num2WordsOptions(),
        )
    except Exception as exc:
        return [
            RuleResult(case=case, actual=None, error=str(exc) or exc.__class__.__name__)
            for case in cases
        ]

    results = []
    for case, item in zip(cases, response.items, strict=True):
        results.append(RuleResult(case=case, actual=item.output, error=item.error))
    return results


def print_cases(cases: Sequence[RuleCase]) -> None:
    for case in cases:
        print(f"{case.id}\t{case.operation}\t{case.language}\t{case.category}")


def print_results(results: Sequence[RuleResult], *, verbose: bool) -> None:
    for result in results:
        if result.passed:
            if verbose:
                print(f"PASS {result.case.id}: {result.actual}")
            continue
        print(f"FAIL {result.case.id}")
        print(f"  input:    {result.case.input}")
        print(f"  expected: {result.case.expected}")
        if result.error:
            print(f"  error:    {result.error}")
        else:
            print(f"  actual:   {result.actual}")


def print_summary(results: Sequence[RuleResult], elapsed: float) -> None:
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    print(f"summary: {passed} passed, {failed} failed, {len(results)} total, {elapsed:.3f}s")


if __name__ == "__main__":
    raise SystemExit(main())
