"""Beautiful Rich-based display for repolyzer output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .analyzers.languages import LanguageReport
from .analyzers.structure import StructureReport
from .analyzers.git import GitReport
from .analyzers.dependencies import DependencyReport
from .analyzers.health import HealthReport
from .analyzers.todos import TodoReport, MARKER_STYLES

LOGO = r"""
                      .__
_______   ____ ______ |  |  ___.__._________ _____
\_  __ \_/ __ \\____ \|  | <   |  |\___   // __ \_ __ \
 |  | \/\  ___/|  |_> >  |__\___  | /    /\  ___/|  | \/
 |__|    \___  >   __/|____// ____|/_____ \\___  >__|
             \/|__|         \/           \/    \/
"""


def _bar_chart(value: float, width: int = 20, color: str = "green") -> Text:
    filled = int(value * width)
    empty = width - filled
    bar = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * empty, style="dim")
    return bar


def display_header(console: Console, project_name: str):
    logo_text = Text(LOGO, style="bright_cyan")
    console.print(Panel(
        logo_text,
        subtitle=f"[dim]analyzing [bright_white]{project_name}[/bright_white][/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE,
        padding=(0, 2),
    ))


def display_languages(console: Console, report: LanguageReport):
    if not report.languages:
        return

    table = Table(
        title=None,
        box=None,
        show_header=False,
        padding=(0, 1),
        expand=True,
    )
    table.add_column("Language", ratio=2)
    table.add_column("Bar", ratio=4)
    table.add_column("Stats", ratio=2, justify="right")

    max_lines = report.languages[0].lines if report.languages else 1

    for lang in report.languages[:10]:
        fraction = lang.lines / max_lines if max_lines else 0
        pct = (lang.lines / report.total_lines * 100) if report.total_lines else 0

        name = Text(f"  {lang.name}", style=f"bold {lang.color}")
        bar = _bar_chart(fraction, width=25, color=lang.color)
        stats = Text(f"{pct:5.1f}%  {lang.lines:>7,} lines  {lang.files:>4} files", style="dim")

        table.add_row(name, bar, stats)

    console.print(Panel(
        table,
        title="[bold bright_cyan]Languages[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 1),
    ))


def display_structure(console: Console, report: StructureReport):
    grid = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    grid.add_row(
        Text.assemble(("  Files      ", "dim"), (f"{report.total_files:,}", "bold bright_white")),
        Text.assemble(("  Dirs       ", "dim"), (f"{report.total_dirs:,}", "bold bright_white")),
    )
    grid.add_row(
        Text.assemble(("  Size       ", "dim"), (report.size_human, "bold bright_white")),
        Text.assemble(("  Max depth  ", "dim"), (str(report.max_depth), "bold bright_white")),
    )

    console.print(Panel(
        grid,
        title="[bold bright_cyan]Structure[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    ))


def display_git(console: Console, report: GitReport):
    if not report.is_git_repo:
        console.print(Panel(
            Text("  Not a git repository", style="dim italic"),
            title="[bold bright_cyan]Git[/bold bright_cyan]",
            border_style="cyan",
            box=box.ROUNDED,
        ))
        return

    grid = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    grid.add_row(
        Text.assemble(("  Branch     ", "dim"), (report.current_branch, "bold bright_green")),
        Text.assemble(("  Commits    ", "dim"), (f"{report.total_commits:,}", "bold bright_white")),
    )
    grid.add_row(
        Text.assemble(("  Branches   ", "dim"), (str(report.branches), "bold bright_white")),
        Text.assemble(("  Tags       ", "dim"), (str(report.tags), "bold bright_white")),
    )
    grid.add_row(
        Text.assemble(("  Authors    ", "dim"), (str(report.contributors), "bold bright_white")),
        Text.assemble(
            ("  Changes    ", "dim"),
            (str(report.uncommitted_changes), "bold bright_yellow" if report.uncommitted_changes else "bold bright_white"),
        ),
    )

    if report.last_commit_message:
        grid.add_row(
            Text.assemble(("  Last       ", "dim"), (report.last_commit_message[:40], "italic")),
            Text.assemble(("  ", ""), (report.last_commit_date, "dim")),
        )

    if report.first_commit_date:
        grid.add_row(
            Text.assemble(("  Age        ", "dim"), (report.first_commit_date, "dim italic")),
            Text(""),
        )

    # Top contributors
    if report.top_contributors:
        grid.add_row(Text(""), Text(""))
        for i, (name, count) in enumerate(report.top_contributors[:3]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "  "
            grid.add_row(
                Text.assemble(("  ", ""), (f"{medal} {name}", "bright_white")),
                Text(f"{count:,} commits", style="dim"),
            )

    console.print(Panel(
        grid,
        title="[bold bright_cyan]Git[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    ))


def display_dependencies(console: Console, report: DependencyReport):
    if not report.files:
        return

    table = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    table.add_column(ratio=2)
    table.add_column(ratio=1, justify="right")

    for dep_file in report.files:
        name = Text(f"  {dep_file.name}", style="bold bright_white")
        counts = Text()
        counts.append(f"{dep_file.count} deps", style="bright_green")
        if dep_file.dev_count:
            counts.append(f"  {dep_file.dev_count} dev", style="dim")
        table.add_row(name, counts)

    total = Text()
    total.append("\n  Total: ", style="dim")
    total.append(f"{report.total_deps}", style="bold bright_white")
    total.append(" dependencies", style="dim")
    if report.total_dev_deps:
        total.append(f", {report.total_dev_deps} dev", style="dim")

    from rich.console import Group
    console.print(Panel(
        Group(table, total),
        title="[bold bright_cyan]Dependencies[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    ))


def display_health(console: Console, report: HealthReport):
    table = Table(box=None, show_header=False, padding=(0, 1), expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=3)

    for check in report.checks:
        icon = "[bright_green]  ✓[/bright_green]" if check.passed else "[bright_red]  ✗[/bright_red]"
        style = "bright_white" if check.passed else "dim"
        table.add_row(
            Text.from_markup(icon),
            Text(check.name, style=style),
        )

    # Score bar
    score_color = "bright_green" if report.score >= 70 else "bright_yellow" if report.score >= 40 else "bright_red"
    score_text = Text()
    score_text.append("\n  Health score: ", style="dim")
    score_text.append(f"{report.score}%", style=f"bold {score_color}")
    score_text.append("  ")
    score_text.append_text(_bar_chart(report.score / 100, width=20, color=score_color))

    from rich.console import Group
    console.print(Panel(
        Group(table, score_text),
        title="[bold bright_cyan]Health[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    ))


def display_todos(console: Console, report: TodoReport):
    if not report.total:
        return

    parts = []
    for marker, count in sorted(report.counts.items(), key=lambda x: x[1], reverse=True):
        color = MARKER_STYLES.get(marker, "white")
        parts.append(f"[{color}]  {marker}[/{color}] [{color}]{count}[/{color}]")

    summary = "    ".join(parts)
    total_text = f"\n  [dim]Total:[/dim] [bold bright_white]{report.total}[/bold bright_white] [dim]markers found[/dim]"

    console.print(Panel(
        Text.from_markup(summary + total_text),
        title="[bold bright_cyan]Code Markers[/bold bright_cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 1),
    ))


def display_all(
    console: Console,
    project_name: str,
    languages: LanguageReport,
    structure: StructureReport,
    git: GitReport,
    dependencies: DependencyReport,
    health: HealthReport,
    todos: TodoReport,
):
    console.print()
    display_header(console, project_name)
    display_languages(console, languages)
    display_structure(console, structure)
    display_git(console, git)
    display_dependencies(console, dependencies)
    display_health(console, health)
    display_todos(console, todos)
    console.print()
