"""Analyze repository health indicators."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class HealthCheck:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class HealthReport:
    checks: list[HealthCheck] = field(default_factory=list)
    score: int = 0  # 0-100


CI_FILES = [
    ".github/workflows",
    ".gitlab-ci.yml",
    ".circleci/config.yml",
    "Jenkinsfile",
    ".travis.yml",
    "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
]

TEST_PATTERNS = [
    "tests",
    "test",
    "spec",
    "__tests__",
    "test_*.py",
    "*_test.go",
    "*.test.js",
    "*.test.ts",
    "*.spec.js",
    "*.spec.ts",
]

DOCKER_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
]


def analyze_health(root: Path) -> HealthReport:
    checks: list[HealthCheck] = []

    # README
    readme_exists = any(
        (root / name).exists()
        for name in ("README.md", "README.rst", "README.txt", "README")
    )
    checks.append(HealthCheck("README", readme_exists, "Documentation for your project"))

    # LICENSE
    license_exists = any(
        (root / name).exists()
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING")
    )
    checks.append(HealthCheck("License", license_exists, "Open source license"))

    # .gitignore
    gitignore = (root / ".gitignore").exists()
    checks.append(HealthCheck(".gitignore", gitignore, "Git ignore rules"))

    # CI/CD
    ci_found = ""
    for ci in CI_FILES:
        if (root / ci).exists():
            ci_found = ci
            break
    checks.append(HealthCheck("CI/CD", bool(ci_found), ci_found or "No CI/CD configuration found"))

    # Tests
    test_found = ""
    for pattern in TEST_PATTERNS[:5]:  # Check directories
        if (root / pattern).exists():
            test_found = pattern
            break
    checks.append(HealthCheck("Tests", bool(test_found), test_found or "No test directory found"))

    # Docker
    docker_found = ""
    for df in DOCKER_FILES:
        if (root / df).exists():
            docker_found = df
            break
    checks.append(HealthCheck("Docker", bool(docker_found), docker_found or "No Docker configuration"))

    # CONTRIBUTING
    contributing = any(
        (root / name).exists()
        for name in ("CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING")
    )
    checks.append(HealthCheck("Contributing guide", contributing, "Guide for contributors"))

    # CHANGELOG
    changelog = any(
        (root / name).exists()
        for name in ("CHANGELOG.md", "CHANGELOG", "CHANGES.md", "HISTORY.md")
    )
    checks.append(HealthCheck("Changelog", changelog, "Project changelog"))

    # Security policy
    security = any(
        (root / name).exists()
        for name in ("SECURITY.md", ".github/SECURITY.md")
    )
    checks.append(HealthCheck("Security policy", security, "Security reporting guidelines"))

    # Editor config
    editorconfig = any(
        (root / name).exists()
        for name in (".editorconfig", ".prettierrc", ".prettierrc.json", ".eslintrc.json", "ruff.toml", ".flake8", "setup.cfg")
    )
    checks.append(HealthCheck("Linter/Formatter", editorconfig, "Code style configuration"))

    # Calculate score
    passed = sum(1 for c in checks if c.passed)
    score = int((passed / len(checks)) * 100) if checks else 0

    return HealthReport(checks=checks, score=score)
