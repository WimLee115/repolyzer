"""Tests for the CLI entry point."""

import json
import subprocess

from click.testing import CliRunner

from repolyzer.cli import main


def _init_git_repo(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.email", "test@test.com"],
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.name", "Tester"],
        capture_output=True,
    )
    (tmp_path / "README.md").write_text("# Test\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "Init"],
        capture_output=True,
    )


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_runs_on_directory(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\n")
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-git"])
    assert result.exit_code == 0


def test_cli_json_output(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\n")
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-git", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "languages" in data
    assert "structure" in data


def test_cli_json_output_languages(tmp_path):
    (tmp_path / "main.rs").write_text("fn main() {}\n")
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-git", "--json"])
    data = json.loads(result.output)
    assert data["languages"]["total_files"] == 1
    names = [l["name"] for l in data["languages"]["breakdown"]]
    assert "Rust" in names


def test_cli_json_with_git(tmp_path):
    _init_git_repo(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["git"]["is_git_repo"] is True
    assert data["git"]["commits"] >= 1


def test_cli_json_with_health(tmp_path):
    (tmp_path / "README.md").write_text("# Hi")
    runner = CliRunner()
    result = runner.invoke(main, [str(tmp_path), "--no-git", "--json"])
    data = json.loads(result.output)
    assert "health" in data
    assert data["health"]["score"] > 0


def test_cli_skip_flags(tmp_path):
    (tmp_path / "app.py").write_text("# TODO: test\n")
    runner = CliRunner()
    result = runner.invoke(
        main, [str(tmp_path), "--no-git", "--no-health", "--no-todos", "--json"]
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "git" not in data
    assert "health" not in data
    assert "todos" not in data


def test_cli_nonexistent_path():
    runner = CliRunner()
    result = runner.invoke(main, ["/nonexistent/path/xyz"])
    assert result.exit_code != 0
