"""Analyze git repository information."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GitReport:
    is_git_repo: bool = False
    total_commits: int = 0
    branches: int = 0
    tags: int = 0
    contributors: int = 0
    last_commit_message: str = ""
    last_commit_date: str = ""
    last_commit_author: str = ""
    remote_url: str = ""
    current_branch: str = ""
    uncommitted_changes: int = 0
    top_contributors: list[tuple[str, int]] = field(default_factory=list)
    first_commit_date: str = ""


def _run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def analyze_git(root: Path) -> GitReport:
    report = GitReport()

    # Check if it's a git repo
    git_dir = root / ".git"
    if not git_dir.exists():
        return report

    report.is_git_repo = True

    # Current branch
    report.current_branch = _run_git(root, "rev-parse", "--abbrev-ref", "HEAD")

    # Total commits
    commit_count = _run_git(root, "rev-list", "--count", "HEAD")
    report.total_commits = int(commit_count) if commit_count.isdigit() else 0

    # Branches
    branches_output = _run_git(root, "branch", "--list")
    if branches_output:
        report.branches = len(branches_output.strip().splitlines())

    # Tags
    tags_output = _run_git(root, "tag", "--list")
    if tags_output:
        report.tags = len(tags_output.strip().splitlines())

    # Contributors
    shortlog = _run_git(root, "shortlog", "-sn", "--no-merges", "HEAD")
    if shortlog:
        lines = shortlog.strip().splitlines()
        report.contributors = len(lines)
        report.top_contributors = []
        for line in lines[:5]:
            parts = line.strip().split("\t", 1)
            if len(parts) == 2:
                count = int(parts[0].strip())
                name = parts[1].strip()
                report.top_contributors.append((name, count))

    # Last commit
    last_log = _run_git(root, "log", "-1", "--format=%s|%ar|%an")
    if last_log and "|" in last_log:
        parts = last_log.split("|", 2)
        report.last_commit_message = parts[0]
        report.last_commit_date = parts[1] if len(parts) > 1 else ""
        report.last_commit_author = parts[2] if len(parts) > 2 else ""

    # First commit date
    first_log = _run_git(root, "log", "--reverse", "--format=%ar", "-1")
    report.first_commit_date = first_log

    # Remote URL
    report.remote_url = _run_git(root, "remote", "get-url", "origin")

    # Uncommitted changes
    status = _run_git(root, "status", "--porcelain")
    if status:
        report.uncommitted_changes = len(status.strip().splitlines())

    return report
