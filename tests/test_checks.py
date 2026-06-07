from pathlib import Path

from repo_scout.checks import run_checks, score


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def test_complete_repository_scores_full_marks(tmp_path: Path) -> None:
    touch(tmp_path / "README.md")
    touch(tmp_path / "LICENSE")
    touch(tmp_path / "CONTRIBUTING.md")
    touch(tmp_path / "CODE_OF_CONDUCT.md")
    touch(tmp_path / "CHANGELOG.md")
    touch(tmp_path / "tests" / "test_example.py")
    touch(tmp_path / ".github" / "workflows" / "test.yml")
    touch(tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug_report.md")
    touch(tmp_path / ".github" / "pull_request_template.md")
    touch(tmp_path / "SECURITY.md")

    results = run_checks(tmp_path)

    assert score(results) == (10, 10)
    assert all(result.status == "pass" for result in results)


def test_missing_files_are_reported_as_warnings(tmp_path: Path) -> None:
    touch(tmp_path / "README.md")

    results = run_checks(tmp_path)
    statuses = {result.name: result.status for result in results}

    assert statuses["README"] == "pass"
    assert statuses["License"] == "warn"
    assert score(results) == (1, 10)

