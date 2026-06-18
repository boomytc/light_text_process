from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CASES_DIR = PROJECT_DIR / "data" / "rule_cases"
SUPPORTED_OPERATIONS = {"tn", "itn"}

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from light_text_process.processor import TextProcessor
from light_text_process.schemas import ITNOptions, Num2WordsOptions, TNOptions


@dataclass(frozen=True)
class BenchmarkCase:
    id: str
    operation: str
    language: str
    input: str
    options: dict[str, Any]


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cases = filter_cases(load_cases(args.cases), args)
    if not cases:
        raise SystemExit("error: no benchmark cases selected")

    rows = benchmark_routes(
        cases,
        repeat=args.repeat,
        batch_size=args.batch_size,
    )
    print("operation\tlanguage\titems\telapsed_seconds\titems_per_second")
    for row in rows:
        print(
            f"{row['operation']}\t{row['language']}\t{row['items']}\t"
            f"{row['elapsed_seconds']:.4f}\t{row['items_per_second']:.1f}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark public TN/ITN routes with golden inputs.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_DIR)
    parser.add_argument("--operation", action="append", choices=sorted(SUPPORTED_OPERATIONS))
    parser.add_argument("--language", action="append")
    parser.add_argument("--repeat", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=64)
    return parser


def load_cases(path: Path) -> list[BenchmarkCase]:
    cases = []
    for case_file in sorted(path.glob("*.json")):
        raw_cases = json.loads(case_file.read_text(encoding="utf-8"))
        for raw_case in raw_cases:
            cases.append(
                BenchmarkCase(
                    id=str(raw_case["id"]),
                    operation=str(raw_case["operation"]),
                    language=str(raw_case["language"]),
                    input=str(raw_case["input"]),
                    options=dict(raw_case.get("options", {})),
                )
            )
    return cases


def filter_cases(cases: Iterable[BenchmarkCase], args: argparse.Namespace) -> list[BenchmarkCase]:
    selected = list(cases)
    if args.operation:
        operations = set(args.operation)
        selected = [case for case in selected if case.operation in operations]
    if args.language:
        languages = set(args.language)
        selected = [case for case in selected if case.language in languages]
    return selected


def benchmark_routes(
    cases: Sequence[BenchmarkCase],
    *,
    repeat: int,
    batch_size: int,
) -> list[dict[str, float | int | str]]:
    processor = TextProcessor()
    rows = []
    for (operation, language), route_cases in grouped_by_route(cases).items():
        inputs = [case.input for case in route_cases] * repeat
        started = perf_counter()
        for start in range(0, len(inputs), batch_size):
            processor.batch(
                operation,
                inputs[start : start + batch_size],
                language,
                TNOptions(),
                ITNOptions(),
                Num2WordsOptions(),
            )
        elapsed = perf_counter() - started
        rows.append(
            {
                "operation": operation,
                "language": language,
                "items": len(inputs),
                "elapsed_seconds": elapsed,
                "items_per_second": len(inputs) / elapsed if elapsed else float("inf"),
            }
        )
    return sorted(rows, key=lambda row: (str(row["operation"]), str(row["language"])))


def grouped_by_route(cases: Sequence[BenchmarkCase]) -> dict[tuple[str, str], list[BenchmarkCase]]:
    groups: dict[tuple[str, str], list[BenchmarkCase]] = defaultdict(list)
    for case in cases:
        groups[(case.operation, case.language)].append(case)
    return dict(groups)


if __name__ == "__main__":
    raise SystemExit(main())
