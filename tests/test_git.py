"""Tests for the git analyzer."""

import subprocess

from repolyzer.analyzers.git import GitReport, analyze_git


def _init_git_repo(tmp_path):
    """Initialize a minimal git repo with one commit."""
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
        ["git", "-C", str(tmp_path), "commit", "-m", "Initial commit"],
        capture_output=True,
    )


def test_analyze_git_not_a_repo(tmp_path):
    report = analyze_git(tmp_path)
    assert not report.is_git_repo
    assert report.total_commits == 0


def test_analyze_git_basic(tmp_path):
    _init_git_repo(tmp_path)
    report = analyze_git(tmp_path)

    assert report.is_git_repo
    assert report.total_commits == 1
    assert report.contributors == 1
    assert report.last_commit_message == "Initial commit"
    assert report.current_branch in ("main", "master")
    assert report.uncommitted_changes == 0


def test_analyze_git_uncommitted(tmp_path):
    _init_git_repo(tmp_path)
    (tmp_path / "new_file.txt").write_text("dirty")
    report = analyze_git(tmp_path)
    assert report.uncommitted_changes >= 1


def test_analyze_git_multiple_commits(tmp_path):
    _init_git_repo(tmp_path)
    (tmp_path / "second.txt").write_text("second")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "Second commit"],
        capture_output=True,
    )
    report = analyze_git(tmp_path)
    assert report.total_commits == 2
    assert report.last_commit_message == "Second commit"


def test_analyze_git_branches(tmp_path):
    _init_git_repo(tmp_path)
    subprocess.run(
        ["git", "-C", str(tmp_path), "branch", "feature"],
        capture_output=True,
    )
    report = analyze_git(tmp_path)
    assert report.branches == 2


def test_analyze_git_top_contributors(tmp_path):
    _init_git_repo(tmp_path)
    report = analyze_git(tmp_path)
    assert len(report.top_contributors) >= 1
    assert report.top_contributors[0][0] == "Tester"
    assert report.top_contributors[0][1] == 1


def test_git_report_defaults():
    report = GitReport()
    assert not report.is_git_repo
    assert report.total_commits == 0
    assert report.branches == 0
    assert report.top_contributors == []
