from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str
    suggestion: str

    @property
    def passed(self) -> bool:
        return self.status == "pass"


@dataclass(frozen=True)
class Check:
    name: str
    suggestion: str
    finder: Callable[[Path], Path | None]


def find_named_file(root: Path, names: tuple[str, ...]) -> Path | None:
    normalized = {name.lower() for name in names}
    for child in root.iterdir():
        if child.is_file() and child.name.lower() in normalized:
            return child
    return None


def find_directory(root: Path, names: tuple[str, ...]) -> Path | None:
    normalized = {name.lower() for name in names}
    for child in root.iterdir():
        if child.is_dir() and child.name.lower() in normalized:
            return child
    return None


def find_ci(root: Path) -> Path | None:
    workflows = root / ".github" / "workflows"
    if workflows.is_dir() and any(workflows.glob("*.yml")) or workflows.is_dir() and any(workflows.glob("*.yaml")):
        return workflows
    return None


def find_issue_template(root: Path) -> Path | None:
    issue_template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if issue_template_dir.is_dir() and any(issue_template_dir.iterdir()):
        return issue_template_dir
    issue_template = root / ".github" / "ISSUE_TEMPLATE.md"
    if issue_template.is_file():
        return issue_template
    return None


def find_pull_request_template(root: Path) -> Path | None:
    return find_named_file(root / ".github", ("pull_request_template.md",)) if (root / ".github").is_dir() else None


CHECKS: tuple[Check, ...] = (
    Check(
        "README",
        "Add a README.md with install, usage, examples, and project status.",
        lambda root: find_named_file(root, ("README.md", "README.rst", "README.txt")),
    ),
    Check(
        "License",
        "Add an OSI-approved license file so users know how they can use the project.",
        lambda root: find_named_file(root, ("LICENSE", "LICENSE.md", "COPYING")),
    ),
    Check(
        "Contributing guide",
        "Add CONTRIBUTING.md with setup steps, test commands, and pull request expectations.",
        lambda root: find_named_file(root, ("CONTRIBUTING.md", "CONTRIBUTING.rst")),
    ),
    Check(
        "Code of conduct",
        "Add CODE_OF_CONDUCT.md to set expectations for community behavior.",
        lambda root: find_named_file(root, ("CODE_OF_CONDUCT.md", "CODE-OF-CONDUCT.md")),
    ),
    Check(
        "Changelog",
        "Add CHANGELOG.md or RELEASES.md so users can track project changes.",
        lambda root: find_named_file(root, ("CHANGELOG.md", "RELEASES.md", "HISTORY.md")),
    ),
    Check(
        "Tests",
        "Add tests/ or another visible test directory to make maintenance safer.",
        lambda root: find_directory(root, ("tests", "test", "__tests__")),
    ),
    Check(
        "Continuous integration",
        "Add a CI workflow such as .github/workflows/test.yml.",
        find_ci,
    ),
    Check(
        "Issue templates",
        "Add issue templates so bug reports and feature requests have useful context.",
        find_issue_template,
    ),
    Check(
        "Pull request template",
        "Add .github/pull_request_template.md to guide contributors.",
        find_pull_request_template,
    ),
    Check(
        "Security policy",
        "Add SECURITY.md with a responsible disclosure process.",
        lambda root: find_named_file(root, ("SECURITY.md",)),
    ),
)


def run_checks(root: Path) -> list[CheckResult]:
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    results: list[CheckResult] = []
    for check in CHECKS:
        found = check.finder(root)
        if found is None:
            results.append(CheckResult(check.name, "warn", f"Missing {check.name}", check.suggestion))
        else:
            display_path = found.relative_to(root)
            results.append(CheckResult(check.name, "pass", f"Found {display_path}", check.suggestion))
    return results


def score(results: list[CheckResult]) -> tuple[int, int]:
    return sum(result.passed for result in results), len(results)

