import json
from pathlib import Path

from repo_scout.cli import main


def test_cli_prints_json(tmp_path: Path, capsys) -> None:
    (tmp_path / "README.md").write_text("# Example\n", encoding="utf-8")

    exit_code = main([str(tmp_path), "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert payload["score"]["passed"] == 1
    assert payload["score"]["total"] == 10


def test_cli_returns_error_for_missing_path(tmp_path: Path, capsys) -> None:
    exit_code = main([str(tmp_path / "missing")])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "does not exist" in captured.err

