from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence
from pathlib import Path
import sys
from time import perf_counter


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from light_text_process.paths import GRAMMAR_CACHE_DIR, ensure_runtime_dirs
from light_text_process.processor import (
    DEFAULT_GRAMMAR_WARMUP_PROFILES,
    GRAMMAR_WARMUP_PROFILES,
    TextProcessor,
)


OPERATIONS = ("tn", "itn")


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        if args.command == "status":
            return command_status(args)
        if args.command == "warmup":
            return command_warmup(args)
        if args.command == "clear":
            return command_clear(args)
        if args.command == "rebuild":
            return command_rebuild(args)
        raise ValueError(f"unsupported command: {args.command}")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Maintain project-local fun_text_processing grammar caches.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="show grammar cache status")
    status.add_argument("--profile", action="append", dest="profiles", help="warmup profile to inspect")
    status.add_argument("--verbose", action="store_true", help="list matching cache files")

    warmup = subparsers.add_parser("warmup", help="prebuild grammar caches for warmup profiles")
    warmup.add_argument("--profile", action="append", dest="profiles", help="warmup profile to build")

    clear = subparsers.add_parser("clear", help="remove selected grammar cache files")
    add_cache_scope_arguments(clear)
    clear.add_argument("--yes", action="store_true", help="actually delete files; default is dry-run")

    rebuild = subparsers.add_parser("rebuild", help="clear then warm up selected profiles")
    rebuild.add_argument("--profile", action="append", dest="profiles", help="warmup profile to rebuild")
    rebuild.add_argument("--yes", action="store_true", help="actually delete and rebuild; default is dry-run")

    return parser


def add_cache_scope_arguments(parser: argparse.ArgumentParser) -> None:
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--profile", action="append", dest="profiles", help="clear files expected by this profile")
    scope.add_argument("--all", action="store_true", help="select all grammar cache files")
    parser.add_argument("--operation", choices=OPERATIONS, help="select cache files by operation")
    parser.add_argument("--language", help="select cache files by language code, for example zh, en, ja")


def command_status(args: argparse.Namespace) -> int:
    profiles = profile_names(args.profiles)
    files = cache_files(GRAMMAR_CACHE_DIR)
    print(f"cache_dir: {GRAMMAR_CACHE_DIR}")
    print(f"exists: {GRAMMAR_CACHE_DIR.exists()}")
    print(f"files: {len(files)}")
    print(f"size: {human_bytes(sum(path.stat().st_size for path in files))}")
    print("")
    print("profiles:")
    for profile_name in profiles:
        print_profile_status(profile_name)
    if args.verbose:
        print("")
        print("cache_files:")
        for path in files:
            print(f"  {path.name}\t{human_bytes(path.stat().st_size)}")
    return 0


def command_warmup(args: argparse.Namespace) -> int:
    profiles = profile_names(args.profiles)
    started = perf_counter()
    ensure_runtime_dirs()
    result = TextProcessor().warmup_profiles(profiles)
    elapsed = perf_counter() - started
    print(f"warmed_profiles: {', '.join(result['profiles'])}")
    print(f"tn: {', '.join(result['tn']) or '-'}")
    print(f"itn: {', '.join(result['itn']) or '-'}")
    print(f"elapsed: {elapsed:.3f}s")
    return 0


def command_clear(args: argparse.Namespace) -> int:
    targets = selected_cache_files(
        cache_dir=GRAMMAR_CACHE_DIR,
        profiles=args.profiles,
        include_all=args.all,
        operation=args.operation,
        language=args.language,
    )
    return delete_targets(targets, dry_run=not args.yes)


def command_rebuild(args: argparse.Namespace) -> int:
    profiles = profile_names(args.profiles)
    targets = selected_cache_files(
        cache_dir=GRAMMAR_CACHE_DIR,
        profiles=profiles,
        include_all=False,
        operation=None,
        language=None,
    )
    if not args.yes:
        print("dry_run: true")
        print("would_remove:")
        print_targets(targets)
        print("")
        print("rebuild_skipped: pass --yes to remove files and warm up profiles")
        return 0

    delete_targets(targets, dry_run=False)
    print("")
    return command_warmup(argparse.Namespace(profiles=profiles))


def profile_names(values: Sequence[str] | None) -> list[str]:
    names = list(values or DEFAULT_GRAMMAR_WARMUP_PROFILES)
    unknown = [name for name in names if name not in GRAMMAR_WARMUP_PROFILES]
    if unknown:
        supported = ", ".join(sorted(GRAMMAR_WARMUP_PROFILES))
        raise ValueError(f"unsupported profile: {', '.join(unknown)} (supported: {supported})")
    return names


def print_profile_status(profile_name: str) -> None:
    tasks = GRAMMAR_WARMUP_PROFILES[profile_name]
    print(f"  {profile_name}:")
    for task in tasks:
        missing = [
            file_name
            for file_name in task.expected_cache_files
            if not (GRAMMAR_CACHE_DIR / file_name).is_file()
        ]
        state = "missing" if missing else "ready"
        print(f"    {task.operation}:{task.language}: {state}")
        for file_name in missing:
            print(f"      missing: {file_name}")


def cache_files(cache_dir: Path) -> list[Path]:
    if not cache_dir.exists():
        return []
    return sorted(path for path in cache_dir.iterdir() if path.is_file() and path.suffix == ".far")


def selected_cache_files(
    *,
    cache_dir: Path,
    profiles: Sequence[str] | None,
    include_all: bool,
    operation: str | None,
    language: str | None,
) -> list[Path]:
    if profiles:
        if include_all or operation or language:
            raise ValueError("--profile cannot be combined with --all, --operation, or --language")
        profile_names(profiles)
        names = {
            file_name
            for profile_name in profiles
            for task in GRAMMAR_WARMUP_PROFILES[profile_name]
            for file_name in task.expected_cache_files
        }
        return sorted(path for path in (cache_dir / name for name in names) if path.is_file())

    if include_all and (operation or language):
        raise ValueError("--all cannot be combined with --operation or --language")
    if not include_all and not operation and not language:
        raise ValueError("provide --profile, --all, --operation, or --language")

    return [
        path
        for path in cache_files(cache_dir)
        if (include_all or matches_cache_file(path.name, operation=operation, language=language))
    ]


def matches_cache_file(name: str, *, operation: str | None, language: str | None) -> bool:
    if operation and not matches_operation(name, operation):
        return False
    if language and not matches_language(name, language):
        return False
    return True


def matches_operation(name: str, operation: str) -> bool:
    if operation == "tn":
        return "_tn_" in name or "_tn." in name
    if operation == "itn":
        return "_itn" in name
    raise ValueError(f"unsupported operation: {operation}")


def matches_language(name: str, language: str) -> bool:
    language = language.strip()
    if not language:
        return False
    markers = (
        f"{language}_tn",
        f"_{language}_tn",
        f"_{language}_itn",
    )
    return any(marker in name for marker in markers)


def delete_targets(targets: Sequence[Path], *, dry_run: bool) -> int:
    print(f"dry_run: {str(dry_run).lower()}")
    print(f"targets: {len(targets)}")
    print_targets(targets)
    if dry_run:
        return 0
    for path in targets:
        path.unlink()
    print("removed: done")
    return 0


def print_targets(targets: Iterable[Path]) -> None:
    for path in targets:
        print(f"  {path.name}")


def human_bytes(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GiB"


if __name__ == "__main__":
    raise SystemExit(main())
