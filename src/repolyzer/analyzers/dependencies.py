"""Analyze project dependencies."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DependencyFile:
    name: str
    path: str
    count: int
    dev_count: int = 0


@dataclass
class DependencyReport:
    files: list[DependencyFile] = field(default_factory=list)
    total_deps: int = 0
    total_dev_deps: int = 0


DEPENDENCY_FILES = {
    "package.json": "_parse_package_json",
    "requirements.txt": "_parse_requirements_txt",
    "Pipfile": "_parse_pipfile",
    "pyproject.toml": "_parse_pyproject_toml",
    "Cargo.toml": "_parse_cargo_toml",
    "go.mod": "_parse_go_mod",
    "Gemfile": "_parse_gemfile",
    "composer.json": "_parse_composer_json",
    "pom.xml": "_parse_pom_xml",
    "build.gradle": "_parse_gradle",
    "pubspec.yaml": "_parse_pubspec",
    "mix.exs": "_parse_mix",
}


def _parse_package_json(path: Path) -> tuple[int, int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        deps = len(data.get("dependencies", {}))
        dev = len(data.get("devDependencies", {}))
        return deps, dev
    except (json.JSONDecodeError, OSError):
        return 0, 0


def _parse_requirements_txt(path: Path) -> tuple[int, int]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        count = sum(1 for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("-"))
        return count, 0
    except OSError:
        return 0, 0


def _parse_pyproject_toml(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        deps = 0
        in_deps = False
        in_dev = False
        dev_deps = 0
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                in_deps = "dependencies" in stripped and "dev" not in stripped.lower() and "optional" not in stripped.lower()
                in_dev = "dev" in stripped.lower() and "dependencies" in stripped.lower()
            elif in_deps and stripped.startswith('"'):
                deps += 1
            elif in_dev and stripped.startswith('"'):
                dev_deps += 1
        return deps, dev_deps
    except OSError:
        return 0, 0


def _parse_cargo_toml(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        deps = 0
        dev_deps = 0
        section = ""
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("["):
                section = stripped
            elif "=" in stripped and not stripped.startswith("#"):
                if section == "[dependencies]":
                    deps += 1
                elif section == "[dev-dependencies]":
                    dev_deps += 1
        return deps, dev_deps
    except OSError:
        return 0, 0


def _parse_go_mod(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        in_require = False
        deps = 0
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("require ("):
                in_require = True
            elif stripped == ")":
                in_require = False
            elif in_require and stripped and not stripped.startswith("//"):
                deps += 1
            elif stripped.startswith("require ") and "(" not in stripped:
                deps += 1
        return deps, 0
    except OSError:
        return 0, 0


def _parse_gemfile(path: Path) -> tuple[int, int]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        count = sum(1 for l in lines if l.strip().startswith("gem "))
        return count, 0
    except OSError:
        return 0, 0


def _parse_composer_json(path: Path) -> tuple[int, int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        deps = len(data.get("require", {}))
        dev = len(data.get("require-dev", {}))
        return deps, dev
    except (json.JSONDecodeError, OSError):
        return 0, 0


def _parse_pipfile(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        section = ""
        deps = 0
        dev = 0
        for line in content.splitlines():
            stripped = line.strip()
            if stripped == "[packages]":
                section = "packages"
            elif stripped == "[dev-packages]":
                section = "dev"
            elif stripped.startswith("["):
                section = ""
            elif "=" in stripped and section == "packages":
                deps += 1
            elif "=" in stripped and section == "dev":
                dev += 1
        return deps, dev
    except OSError:
        return 0, 0


def _parse_pom_xml(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        count = content.count("<dependency>")
        return count, 0
    except OSError:
        return 0, 0


def _parse_gradle(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        deps = sum(1 for l in lines if "implementation " in l or "compile " in l or "api " in l)
        dev = sum(1 for l in lines if "testImplementation " in l or "testCompile " in l)
        return deps, dev
    except OSError:
        return 0, 0


def _parse_pubspec(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        section = ""
        deps = 0
        dev = 0
        for line in content.splitlines():
            stripped = line.strip()
            if stripped == "dependencies:":
                section = "deps"
            elif stripped == "dev_dependencies:":
                section = "dev"
            elif not line.startswith(" ") and not line.startswith("\t") and stripped:
                section = ""
            elif ":" in stripped and section == "deps":
                deps += 1
            elif ":" in stripped and section == "dev":
                dev += 1
        return deps, dev
    except OSError:
        return 0, 0


def _parse_mix(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
        count = content.count("{:")
        return count, 0
    except OSError:
        return 0, 0


_PARSERS = {
    "package.json": _parse_package_json,
    "requirements.txt": _parse_requirements_txt,
    "Pipfile": _parse_pipfile,
    "pyproject.toml": _parse_pyproject_toml,
    "Cargo.toml": _parse_cargo_toml,
    "go.mod": _parse_go_mod,
    "Gemfile": _parse_gemfile,
    "composer.json": _parse_composer_json,
    "pom.xml": _parse_pom_xml,
    "build.gradle": _parse_gradle,
    "pubspec.yaml": _parse_pubspec,
    "mix.exs": _parse_mix,
}


def analyze_dependencies(root: Path) -> DependencyReport:
    report = DependencyReport()

    for filename, parser in _PARSERS.items():
        filepath = root / filename
        if filepath.exists():
            deps, dev = parser(filepath)
            if deps or dev:
                report.files.append(DependencyFile(
                    name=filename,
                    path=str(filepath.relative_to(root)),
                    count=deps,
                    dev_count=dev,
                ))
                report.total_deps += deps
                report.total_dev_deps += dev

    return report
