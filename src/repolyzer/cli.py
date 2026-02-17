"""CLI entry point for repolyzer."""

from __future__ import annotations

import time
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .analyzers import (
    analyze_dependencies,
    analyze_git,
    analyze_health,
    analyze_languages,
    analyze_structure,
    analyze_todos,
)
from .display import display_all


@click.command()
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--no-git", is_flag=True, help="Skip git analysis")
@click.option("--no-health", is_flag=True, help="Skip health checks")
@click.option("--no-todos", is_flag=True, help="Skip TODO/FIXME scanning")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.version_option(version=__version__)
def main(path: str, no_git: bool, no_health: bool, no_todos: bool, as_json: bool):
    """Instant beautiful insights about any codebase.

    Analyzes the repository at PATH (defaults to current directory) and displays
    a comprehensive overview of languages, structure, git history, dependencies,
    health, and code markers.
    """
    console = Console()
    root = Path(path).resolve()
    project_name = root.name

    start = time.monotonic()

    with console.status("[bright_cyan]Scanning codebase...[/bright_cyan]", spinner="dots"):
        languages = analyze_languages(root)
        structure = analyze_structure(root)
        git = analyze_git(root) if not no_git else None
        dependencies = analyze_dependencies(root)
        health = analyze_health(root) if not no_health else None
        todos = analyze_todos(root) if not no_todos else None

    elapsed = time.monotonic() - start

    if as_json:
        _output_json(console, languages, structure, git, dependencies, health, todos)
        return

    from .analyzers.git import GitReport
    from .analyzers.health import HealthReport
    from .analyzers.todos import TodoReport

    display_all(
        console=console,
        project_name=project_name,
        languages=languages,
        structure=structure,
        git=git or GitReport(),
        dependencies=dependencies,
        health=health or HealthReport(),
        todos=todos or TodoReport(),
    )

    console.print(f"  [dim]Scanned in {elapsed:.2f}s[/dim]\n")


def _output_json(console, languages, structure, git, dependencies, health, todos):
    import json

    data = {
        "languages": {
            "total_files": languages.total_files,
            "total_lines": languages.total_lines,
            "breakdown": [
                {"name": l.name, "files": l.files, "lines": l.lines}
                for l in languages.languages
            ],
        },
        "structure": {
            "total_files": structure.total_files,
            "total_dirs": structure.total_dirs,
            "total_size_bytes": structure.total_size_bytes,
            "max_depth": structure.max_depth,
        },
    }

    if git:
        data["git"] = {
            "is_git_repo": git.is_git_repo,
            "commits": git.total_commits,
            "branches": git.branches,
            "tags": git.tags,
            "contributors": git.contributors,
            "current_branch": git.current_branch,
            "uncommitted_changes": git.uncommitted_changes,
        }

    if dependencies:
        data["dependencies"] = {
            "total": dependencies.total_deps,
            "dev": dependencies.total_dev_deps,
            "files": [
                {"name": f.name, "count": f.count, "dev_count": f.dev_count}
                for f in dependencies.files
            ],
        }

    if health:
        data["health"] = {
            "score": health.score,
            "checks": [
                {"name": c.name, "passed": c.passed}
                for c in health.checks
            ],
        }

    if todos:
        data["todos"] = {
            "total": todos.total,
            "counts": dict(todos.counts),
        }

    console.print_json(json.dumps(data))
