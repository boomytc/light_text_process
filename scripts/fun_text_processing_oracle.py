from __future__ import annotations

import argparse
import contextlib
import importlib
import io
import json
import signal
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CASES_DIR = PROJECT_DIR / "data" / "rule_cases"
DEFAULT_OUTPUT = PROJECT_DIR / "runtime" / "oracle" / "fun_text_processing_diff.json"
DEFAULT_CACHE_DIR = PROJECT_DIR / "runtime" / "oracle" / "fun_text_processing_cache"
SUPPORTED_OPERATIONS = {"tn", "itn"}
REVIEW_STATUSES = {"match", "accepted-improvement", "regression", "unsupported-gap"}
STRICT_FAILURE_STATUSES = {"regression", "unsupported-gap"}

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from light_text_process.processor import TextProcessor
from light_text_process.schemas import ITNOptions, TNOptions


@dataclass(frozen=True)
class OracleCase:
    id: str
    operation: str
    language: str
    category: str
    input: str
    expected: str | None
    options: dict[str, Any]
    oracle_status: str | None
    oracle_note: str | None


@dataclass(frozen=True)
class EngineOutput:
    output: str | None
    error: str | None


class OracleTimeoutError(TimeoutError):
    pass


@dataclass(frozen=True)
class Comparison:
    id: str
    operation: str
    language: str
    category: str
    input: str
    expected: str | None
    current: EngineOutput
    oracle: EngineOutput
    status: str
    note: str | None


class FunTextProcessingOracle:
    def __init__(self, reference: Path, cache_dir: Path) -> None:
        self.reference = _validate_reference(reference)
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._normalizers: dict[tuple[str, str], Any] = {}
        self._inverse_normalizers: dict[tuple[str, str], Any] = {}
        parent = str(self.reference.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)

    def process(
        self,
        operation: str,
        language: str,
        texts: Sequence[str],
        options: dict[str, Any] | None = None,
    ) -> list[str]:
        options = options or {}
        if operation == "tn":
            normalizer = self._tn_normalizer(language, options)
            tn_options = TNOptions(**options)
            return normalizer.normalize_list(
                list(texts),
                verbose=False,
                punct_pre_process=tn_options.punct_pre_process,
                punct_post_process=tn_options.punct_post_process,
                batch_size=tn_options.batch_size,
                n_jobs=tn_options.n_jobs,
            )
        if operation == "itn":
            normalizer = self._itn_normalizer(language, options)
            return normalizer.inverse_normalize_list(list(texts), verbose=False)
        raise ValueError(f"unsupported operation: {operation}")

    def _tn_normalizer(self, language: str, options: dict[str, Any]) -> Any:
        tn_options = TNOptions(**options)
        key = (
            language,
            json.dumps(
                {
                    "input_case": tn_options.input_case,
                    "deterministic": tn_options.deterministic,
                    "whitelist_path": tn_options.whitelist_path,
                    "post_process": tn_options.post_process,
                },
                sort_keys=True,
            ),
        )
        if key not in self._normalizers:
            def create_normalizer() -> Any:
                module = importlib.import_module("fun_text_processing.text_normalization.normalize")
                whitelist = _resolve_project_file(tn_options.whitelist_path) if tn_options.whitelist_path else None
                return module.Normalizer(
                    input_case=tn_options.input_case,
                    lang=language,
                    deterministic=tn_options.deterministic,
                    cache_dir=str(self.cache_dir / "tn" / language),
                    overwrite_cache=False,
                    whitelist=str(whitelist) if whitelist else None,
                    post_process=tn_options.post_process,
                )

            self._normalizers[key] = _with_silenced_stdout(create_normalizer)
        return self._normalizers[key]

    def _itn_normalizer(self, language: str, options: dict[str, Any]) -> Any:
        itn_options = ITNOptions(**options)
        key = (
            language,
            json.dumps(
                {
                    "enable_standalone_number": itn_options.enable_standalone_number,
                    "enable_0_to_9": itn_options.enable_0_to_9,
                },
                sort_keys=True,
            ),
        )
        if key not in self._inverse_normalizers:
            def create_inverse_normalizer() -> Any:
                module = importlib.import_module("fun_text_processing.inverse_text_normalization.inverse_normalize")
                kwargs: dict[str, Any] = {
                    "lang": language,
                    "cache_dir": str(self.cache_dir / "itn" / language),
                    "overwrite_cache": False,
                }
                if language == "ja":
                    kwargs.update(
                        {
                            "enable_standalone_number": itn_options.enable_standalone_number,
                            "enable_0_to_9": itn_options.enable_0_to_9,
                        }
                    )
                return module.InverseNormalizer(**kwargs)

            self._inverse_normalizers[key] = _with_silenced_stdout(create_inverse_normalizer)
        return self._inverse_normalizers[key]


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "run":
            return run_oracle(args)
        if args.command == "compare":
            return compare(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    raise ValueError(f"unsupported command: {args.command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Use an isolated fun_text_processing checkout as a reference oracle. "
            "This script is not imported by light_text_process runtime code."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run oracle output for one or more texts")
    add_reference_args(run_parser)
    run_parser.add_argument("--operation", choices=sorted(SUPPORTED_OPERATIONS), required=True)
    run_parser.add_argument("--language", required=True)
    run_parser.add_argument("--text", action="append", required=True)
    run_parser.add_argument(
        "--options-json",
        default="{}",
        help="JSON object with TNOptions or ITNOptions values",
    )

    compare_parser = subparsers.add_parser("compare", help="compare current output with oracle output")
    add_reference_args(compare_parser)
    compare_parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_DIR)
    compare_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    compare_parser.add_argument("--language", action="append")
    compare_parser.add_argument("--operation", action="append", choices=sorted(SUPPORTED_OPERATIONS))
    compare_parser.add_argument("--category", action="append")
    compare_parser.add_argument("--case", action="append", dest="case_ids")
    compare_parser.add_argument(
        "--oracle-timeout-seconds",
        type=float,
        default=0,
        help="per route/options oracle call timeout; 0 disables timeout",
    )
    compare_parser.add_argument(
        "--strict",
        action="store_true",
        help="return non-zero when any comparison does not match",
    )
    compare_parser.add_argument("--verbose", action="store_true")
    return parser


def add_reference_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--reference",
        type=Path,
        required=True,
        help="path to an external fun_text_processing package directory",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_CACHE_DIR,
        help=f"oracle FAR/FST cache directory (default: {DEFAULT_CACHE_DIR})",
    )


def run_oracle(args: argparse.Namespace) -> int:
    options = parse_options_json(args.options_json)
    cache_dir = _validate_runtime_oracle_path(args.cache_dir, "cache-dir")
    oracle = FunTextProcessingOracle(args.reference, cache_dir)
    outputs = oracle.process(args.operation, args.language, args.text, options)
    payload = {
        "operation": args.operation,
        "language": args.language,
        "items": [
            {"input": item, "oracle_output": output}
            for item, output in zip(args.text, outputs, strict=True)
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def compare(args: argparse.Namespace) -> int:
    cases = filter_cases(load_cases(args.cases), args)
    if not cases:
        raise ValueError("no cases selected")

    output = _validate_runtime_oracle_path(args.output, "output")
    cache_dir = _validate_runtime_oracle_path(args.cache_dir, "cache-dir")
    oracle = FunTextProcessingOracle(args.reference, cache_dir)
    started = perf_counter()
    comparisons = compare_cases(
        cases,
        oracle,
        oracle_timeout_seconds=args.oracle_timeout_seconds,
    )
    elapsed = perf_counter() - started
    report = build_report(args.reference, comparisons, elapsed)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print_comparison_summary(comparisons, elapsed, output, verbose=args.verbose)
    if args.strict and any(comparison.status in STRICT_FAILURE_STATUSES for comparison in comparisons):
        return 1
    return 0


def load_cases(path: Path) -> list[OracleCase]:
    if path.is_file():
        case_files = [path]
    elif path.is_dir():
        case_files = sorted(path.glob("*.json"))
    else:
        raise ValueError(f"case path does not exist: {path}")

    cases: list[OracleCase] = []
    seen_ids: set[str] = set()
    for case_file in case_files:
        raw_cases = json.loads(case_file.read_text(encoding="utf-8"))
        if not isinstance(raw_cases, list):
            raise ValueError(f"case file must contain a JSON list: {case_file}")
        for index, raw_case in enumerate(raw_cases, start=1):
            case = parse_case(raw_case, case_file, index)
            if case.id in seen_ids:
                raise ValueError(f"duplicate case id: {case.id}")
            seen_ids.add(case.id)
            cases.append(case)
    return cases


def parse_case(raw_case: Any, case_file: Path, index: int) -> OracleCase:
    if not isinstance(raw_case, dict):
        raise ValueError(f"{case_file} case {index} must be an object")
    values: dict[str, str] = {}
    for field in ("id", "operation", "language", "category", "input"):
        value = raw_case.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{case_file} case {index} field {field!r} must be a non-empty string")
        values[field] = value
    if values["operation"] not in SUPPORTED_OPERATIONS:
        raise ValueError(f"{case_file} case {values['id']} has unsupported operation: {values['operation']}")
    options = raw_case.get("options", {})
    if not isinstance(options, dict):
        raise ValueError(f"{case_file} case {values['id']} options must be an object")
    if values["operation"] == "tn":
        TNOptions(**options)
    else:
        ITNOptions(**options)
    oracle_status = raw_case.get("oracle_status")
    if oracle_status is not None:
        if not isinstance(oracle_status, str) or oracle_status not in REVIEW_STATUSES:
            raise ValueError(
                f"{case_file} case {values['id']} oracle_status must be one of: "
                f"{', '.join(sorted(REVIEW_STATUSES))}"
            )
    oracle_note = raw_case.get("oracle_note")
    if oracle_note is not None and (not isinstance(oracle_note, str) or not oracle_note.strip()):
        raise ValueError(f"{case_file} case {values['id']} oracle_note must be a non-empty string")
    expected = raw_case.get("expected")
    if expected is not None and not isinstance(expected, str):
        raise ValueError(f"{case_file} case {values['id']} expected must be a string when present")
    if oracle_status == "accepted-improvement":
        if expected is None:
            raise ValueError(
                f"{case_file} case {values['id']} accepted-improvement requires expected output"
            )
        if oracle_note is None:
            raise ValueError(
                f"{case_file} case {values['id']} accepted-improvement requires oracle_note"
            )
    return OracleCase(
        id=values["id"],
        operation=values["operation"],
        language=values["language"],
        category=values["category"],
        input=values["input"],
        expected=expected,
        options=options,
        oracle_status=oracle_status,
        oracle_note=oracle_note,
    )


def filter_cases(cases: Iterable[OracleCase], args: argparse.Namespace) -> list[OracleCase]:
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


def compare_cases(
    cases: Sequence[OracleCase],
    oracle: FunTextProcessingOracle,
    *,
    oracle_timeout_seconds: float = 0,
) -> list[Comparison]:
    current = TextProcessor()
    comparisons: list[Comparison] = []
    for group_cases in grouped_cases(cases).values():
        current_outputs = [run_current_case(current, case) for case in group_cases]
        oracle_outputs = run_oracle_group(
            oracle,
            group_cases,
            timeout_seconds=oracle_timeout_seconds,
        )
        for case, current_output, oracle_output in zip(group_cases, current_outputs, oracle_outputs, strict=True):
            status = classify(
                current_output,
                oracle_output,
                expected=case.expected,
                reviewed_status=case.oracle_status,
            )
            comparisons.append(
                Comparison(
                    id=case.id,
                    operation=case.operation,
                    language=case.language,
                    category=case.category,
                    input=case.input,
                    expected=case.expected,
                    current=current_output,
                    oracle=oracle_output,
                    status=status,
                    note=case.oracle_note,
                )
            )
    return comparisons


def grouped_cases(cases: Sequence[OracleCase]) -> dict[tuple[str, str, str], list[OracleCase]]:
    groups: dict[tuple[str, str, str], list[OracleCase]] = {}
    for case in cases:
        options_key = json.dumps(case.options, sort_keys=True, ensure_ascii=False)
        groups.setdefault((case.operation, case.language, options_key), []).append(case)
    return groups


def run_current_case(processor: TextProcessor, case: OracleCase) -> EngineOutput:
    try:
        if case.operation == "tn":
            response = processor.normalize_text(case.input, case.language, TNOptions(**case.options))
        else:
            response = processor.inverse_normalize_text(case.input, case.language, ITNOptions(**case.options))
        return EngineOutput(output=response.output, error=None)
    except Exception as exc:
        return EngineOutput(output=None, error=str(exc) or exc.__class__.__name__)


def run_oracle_case(
    oracle: FunTextProcessingOracle,
    case: OracleCase,
    *,
    timeout_seconds: float = 0,
) -> EngineOutput:
    try:
        with _oracle_timeout(timeout_seconds):
            output = oracle.process(case.operation, case.language, [case.input], case.options)[0]
        return EngineOutput(output=output, error=None)
    except Exception as exc:
        return EngineOutput(output=None, error=str(exc) or exc.__class__.__name__)


def run_oracle_group(
    oracle: FunTextProcessingOracle,
    cases: Sequence[OracleCase],
    *,
    timeout_seconds: float = 0,
) -> list[EngineOutput]:
    first = cases[0]
    try:
        with _oracle_timeout(timeout_seconds):
            outputs = oracle.process(
                first.operation,
                first.language,
                [case.input for case in cases],
                first.options,
            )
        if len(outputs) != len(cases):
            raise ValueError(f"oracle output count mismatch: expected {len(cases)}, got {len(outputs)}")
        return [EngineOutput(output=output, error=None) for output in outputs]
    except OracleTimeoutError as exc:
        error = str(exc) or exc.__class__.__name__
        return [EngineOutput(output=None, error=error) for _case in cases]
    except Exception:
        return [
            run_oracle_case(oracle, case, timeout_seconds=timeout_seconds)
            for case in cases
        ]


def classify(
    current: EngineOutput,
    oracle: EngineOutput,
    *,
    expected: str | None = None,
    reviewed_status: str | None = None,
) -> str:
    if current.error:
        return _reviewed_or_default(reviewed_status, "unsupported-gap")
    if oracle.error:
        if reviewed_status == "accepted-improvement" and expected is not None and current.output == expected:
            return _reviewed_or_default(reviewed_status, "accepted-improvement")
        return _reviewed_or_default(reviewed_status, "regression")
    if current.output == oracle.output:
        return "match"
    if reviewed_status == "accepted-improvement" and expected is not None and current.output == expected:
        return _reviewed_or_default(reviewed_status, "accepted-improvement")
    return _reviewed_or_default(reviewed_status, "regression")


def _reviewed_or_default(reviewed_status: str | None, default: str) -> str:
    if reviewed_status in {None, "match"}:
        return default
    return reviewed_status


def build_report(reference: Path, comparisons: Sequence[Comparison], elapsed: float) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for comparison in comparisons:
        status_counts[comparison.status] = status_counts.get(comparison.status, 0) + 1
    return {
        "reference": str(reference),
        "elapsed_seconds": round(elapsed, 4),
        "summary": {
            "total": len(comparisons),
            "status_counts": dict(sorted(status_counts.items())),
        },
        "route_summary": summarize_comparisons(comparisons, ("operation", "language")),
        "category_summary": summarize_comparisons(comparisons, ("operation", "language", "category")),
        "comparisons": [comparison_to_dict(comparison) for comparison in comparisons],
    }


def summarize_comparisons(comparisons: Sequence[Comparison], fields: tuple[str, ...]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], dict[str, int]] = {}
    totals: dict[tuple[str, ...], int] = {}
    for comparison in comparisons:
        key = tuple(str(getattr(comparison, field)) for field in fields)
        grouped.setdefault(key, {})
        grouped[key][comparison.status] = grouped[key].get(comparison.status, 0) + 1
        totals[key] = totals.get(key, 0) + 1

    summary = []
    for key in sorted(grouped):
        row = {field: value for field, value in zip(fields, key, strict=True)}
        row["total"] = totals[key]
        row["status_counts"] = dict(sorted(grouped[key].items()))
        summary.append(row)
    return summary


def comparison_to_dict(comparison: Comparison) -> dict[str, Any]:
    payload = asdict(comparison)
    return payload


def print_comparison_summary(
    comparisons: Sequence[Comparison],
    elapsed: float,
    output: Path,
    *,
    verbose: bool,
) -> None:
    counts: dict[str, int] = {}
    for comparison in comparisons:
        counts[comparison.status] = counts.get(comparison.status, 0) + 1
        if verbose or comparison.status != "match":
            print(f"{comparison.status.upper()} {comparison.id}")
            print(f"  input:   {comparison.input}")
            print(f"  current: {comparison.current.output if comparison.current.error is None else comparison.current.error}")
            print(f"  oracle:  {comparison.oracle.output if comparison.oracle.error is None else comparison.oracle.error}")
            if comparison.note:
                print(f"  note:    {comparison.note}")
    summary = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"summary: total={len(comparisons)}, {summary}, elapsed={elapsed:.3f}s")
    print("routes:")
    for row in summarize_comparisons(comparisons, ("operation", "language")):
        route = f"{row['operation']}/{row['language']}"
        route_counts = ", ".join(f"{key}={value}" for key, value in row["status_counts"].items())
        print(f"  {route}: total={row['total']}, {route_counts}")
    print(f"report: {output}")


def parse_options_json(raw: str) -> dict[str, Any]:
    try:
        options = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid options JSON: {exc}") from exc
    if not isinstance(options, dict):
        raise ValueError("options JSON must be an object")
    return options


def _validate_reference(reference: Path) -> Path:
    resolved = reference.expanduser().resolve()
    if not resolved.is_dir():
        raise ValueError(f"reference path is not a directory: {reference}")
    if resolved.name != "fun_text_processing":
        raise ValueError(f"reference path must point to a fun_text_processing directory: {reference}")
    for relative in (
        "text_normalization/normalize.py",
        "inverse_text_normalization/inverse_normalize.py",
    ):
        if not (resolved / relative).is_file():
            raise ValueError(f"reference path is missing {relative}: {reference}")
    return resolved


def _validate_runtime_oracle_path(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    oracle_dir = (PROJECT_DIR / "runtime" / "oracle").resolve()
    try:
        resolved.relative_to(oracle_dir)
    except ValueError as exc:
        raise ValueError(f"{label} must stay under {oracle_dir}: {path}") from exc
    return resolved


@contextlib.contextmanager
def _oracle_timeout(seconds: float):
    if seconds <= 0:
        yield
        return

    def handle_timeout(_signum: int, _frame: Any) -> None:
        raise OracleTimeoutError(f"oracle call exceeded {seconds:g}s")

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def _resolve_project_file(raw_path: str) -> Path:
    path = (PROJECT_DIR / raw_path).resolve()
    try:
        path.relative_to(PROJECT_DIR)
    except ValueError as exc:
        raise ValueError(f"path must stay inside project directory: {raw_path}") from exc
    if not path.is_file():
        raise ValueError(f"project file does not exist: {raw_path}")
    return path


def _with_silenced_stdout(callback: Callable[[], Any]) -> Any:
    with contextlib.redirect_stdout(io.StringIO()):
        return callback()


if __name__ == "__main__":
    raise SystemExit(main())
