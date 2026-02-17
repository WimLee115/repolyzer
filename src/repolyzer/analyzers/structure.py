"""Analyze repository structure."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .languages import SKIP_DIRS


@dataclass
class StructureReport:
    total_files: int = 0
    total_dirs: int = 0
    total_size_bytes: int = 0
    deepest_path: str = ""
    max_depth: int = 0
    largest_files: list[tuple[str, int]] = None

    def __post_init__(self):
        if self.largest_files is None:
            self.largest_files = []

    @property
    def size_human(self) -> str:
        size = self.total_size_bytes
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


def analyze_structure(root: Path) -> StructureReport:
    total_files = 0
    total_dirs = 0
    total_size = 0
    max_depth = 0
    deepest_path = ""
    file_sizes: list[tuple[str, int]] = []

    root_depth = str(root).count(os.sep)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        total_dirs += len(dirnames)

        current_depth = str(dirpath).count(os.sep) - root_depth
        if current_depth > max_depth:
            max_depth = current_depth
            deepest_path = os.path.relpath(dirpath, root)

        for filename in filenames:
            filepath = Path(dirpath) / filename
            try:
                size = filepath.stat().st_size
                total_files += 1
                total_size += size
                rel = os.path.relpath(filepath, root)
                file_sizes.append((rel, size))
            except (OSError, PermissionError):
                continue

    file_sizes.sort(key=lambda x: x[1], reverse=True)

    return StructureReport(
        total_files=total_files,
        total_dirs=total_dirs,
        total_size_bytes=total_size,
        deepest_path=deepest_path,
        max_depth=max_depth,
        largest_files=file_sizes[:5],
    )
