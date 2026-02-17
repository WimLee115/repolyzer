"""Analyze programming languages used in the repository."""

from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".swift": "Swift",
    ".m": "Objective-C",
    ".scala": "Scala",
    ".zig": "Zig",
    ".lua": "Lua",
    ".r": "R",
    ".R": "R",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".hs": "Haskell",
    ".ml": "OCaml",
    ".v": "V",
    ".nim": "Nim",
    ".cr": "Crystal",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Shell",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".sql": "SQL",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".xml": "XML",
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".tf": "Terraform",
    ".proto": "Protobuf",
    ".graphql": "GraphQL",
    ".gql": "GraphQL",
}

LANGUAGE_COLORS: dict[str, str] = {
    "Python": "yellow",
    "JavaScript": "bright_yellow",
    "TypeScript": "blue",
    "Rust": "red",
    "Go": "cyan",
    "Java": "bright_red",
    "Kotlin": "magenta",
    "Ruby": "red",
    "PHP": "bright_magenta",
    "C": "bright_blue",
    "C++": "bright_blue",
    "C#": "green",
    "Swift": "bright_red",
    "Scala": "red",
    "Shell": "green",
    "HTML": "bright_red",
    "CSS": "bright_blue",
    "Vue": "bright_green",
    "Svelte": "bright_red",
    "Dart": "cyan",
    "Elixir": "magenta",
    "Haskell": "bright_magenta",
    "Zig": "bright_yellow",
    "Lua": "blue",
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".env", "dist", "build", ".next", ".nuxt", "target", ".tox",
    "vendor", ".idea", ".vscode", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", "coverage", ".coverage", "htmlcov", ".eggs",
    "*.egg-info", ".gradle", ".cargo", "bin", "obj",
}


@dataclass
class LanguageStats:
    name: str
    files: int = 0
    lines: int = 0
    color: str = "white"


@dataclass
class LanguageReport:
    languages: list[LanguageStats] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0


def _count_lines(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, PermissionError):
        return 0


def analyze_languages(root: Path) -> LanguageReport:
    lang_files: dict[str, int] = defaultdict(int)
    lang_lines: dict[str, int] = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            ext = Path(filename).suffix
            lang = EXTENSION_MAP.get(ext)
            if lang:
                filepath = Path(dirpath) / filename
                lang_files[lang] += 1
                lang_lines[lang] += _count_lines(filepath)

    languages = []
    for name in lang_files:
        languages.append(LanguageStats(
            name=name,
            files=lang_files[name],
            lines=lang_lines[name],
            color=LANGUAGE_COLORS.get(name, "white"),
        ))

    languages.sort(key=lambda x: x.lines, reverse=True)

    return LanguageReport(
        languages=languages,
        total_files=sum(lang_files.values()),
        total_lines=sum(lang_lines.values()),
    )
