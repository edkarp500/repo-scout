from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from repo_scout.checks import CheckResult, run_checks, score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-scout",
        description="Check whether a repository has common open-source maintenance files.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository path to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output.",
    )
    return parser


def result_to_dict(result: CheckResult) -> dict[str, str]:
    return {
        "name": result.name,
        "status": result.status,
        "message": result.message,
        "suggestion": result.suggestion,
    }


def format_text(path: Path, results: list[CheckResult]) -> str:
    passed, total = score(results)
    lines = [
        f"Repo Scout report for {path}",
        "",
        f"Score: {passed}/{total}",
        "",
    ]

    for result in results:
        lines.append(f"[{result.status}] {result.name}: {result.message}")
        if not result.passed:
            lines.append(f"       Suggestion: {result.suggestion}")

    return "\n".join(lines)


def format_json(path: Path, results: list[CheckResult]) -> str:
    passed, total = score(results)
    payload = {
        "path": str(path),
        "score": {
            "passed": passed,
            "total": total,
        },
        "results": [result_to_dict(result) for result in results],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = Path(args.path).expanduser().resolve()

    try:
        results = run_checks(path)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"repo-scout: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(format_json(path, results))
    else:
        print(format_text(path, results))

    passed, total = score(results)
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

