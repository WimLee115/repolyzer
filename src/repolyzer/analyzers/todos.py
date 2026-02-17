"""Analyze TODO, FIXME, HACK, and other markers in code."""

from __future__ import annotations

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .languages import EXTENSION_MAP, SKIP_DIRS

MARKERS = {
    "TODO": re.compile(r"\bTODO\b", re.IGNORECASE),
    "FIXME": re.compile(r"\bFIXME\b", re.IGNORECASE),
    "HACK": re.compile(r"\bHACK\b", re.IGNORECASE),
    "BUG": re.compile(r"\bBUG\b", re.IGNORECASE),
    "XXX": re.compile(r"\bXXX\b"),
    "OPTIMIZE": re.compile(r"\bOPTIMIZE\b", re.IGNORECASE),
    "DEPRECATED": re.compile(r"\bDEPRECATED\b", re.IGNORECASE),
}

MARKER_STYLES = {
    "TODO": "bright_cyan",
    "FIXME": "bright_red",
    "HACK": "bright_yellow",
    "BUG": "red",
    "XXX": "bright_magenta",
    "OPTIMIZE": "bright_green",
    "DEPRECATED": "dim",
}


@dataclass
class TodoItem:
    marker: str
    text: str
    file: str
    line: int


@dataclass
class TodoReport:
    counts: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    items: list[TodoItem] = field(default_factory=list)
    total: int = 0


def analyze_todos(root: Path, max_items: int = 20) -> TodoReport:
    report = TodoReport()
    code_extensions = set(EXTENSION_MAP.keys())

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            ext = Path(filename).suffix
            if ext not in code_extensions:
                continue

            filepath = Path(dirpath) / filename
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        for marker_name, pattern in MARKERS.items():
                            if pattern.search(line):
                                report.counts[marker_name] += 1
                                report.total += 1
                                if len(report.items) < max_items:
                                    rel_path = os.path.relpath(filepath, root)
                                    text = line.strip()
                                    if len(text) > 80:
                                        text = text[:77] + "..."
                                    report.items.append(TodoItem(
                                        marker=marker_name,
                                        text=text,
                                        file=rel_path,
                                        line=line_num,
                                    ))
                                break  # One marker per line
            except (OSError, PermissionError):
                continue

    return report
