from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        print("cache_policy: none")
        print("status: vendor grammar caches are not used")
        return 0
    raise ValueError(f"unsupported command: {args.command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report the vendor-free grammar cache policy.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="show cache policy")
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
