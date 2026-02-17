"""Tests for the health analyzer."""

from repolyzer.analyzers.health import HealthCheck, HealthReport, analyze_health


def test_health_all_missing(tmp_path):
    report = analyze_health(tmp_path)
    assert report.score == 0
    assert all(not c.passed for c in report.checks)


def test_health_readme(tmp_path):
    (tmp_path / "README.md").write_text("# Project")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "README")
    assert check.passed


def test_health_license(tmp_path):
    (tmp_path / "LICENSE").write_text("MIT")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "License")
    assert check.passed


def test_health_license_variants(tmp_path):
    (tmp_path / "LICENCE").write_text("MIT")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "License")
    assert check.passed


def test_health_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == ".gitignore")
    assert check.passed


def test_health_ci_github(tmp_path):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "CI/CD")
    assert check.passed


def test_health_tests_dir(tmp_path):
    (tmp_path / "tests").mkdir()
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Tests")
    assert check.passed


def test_health_contributing(tmp_path):
    (tmp_path / "CONTRIBUTING.md").write_text("# Contributing")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Contributing guide")
    assert check.passed


def test_health_changelog(tmp_path):
    (tmp_path / "CHANGELOG.md").write_text("# Changelog")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Changelog")
    assert check.passed


def test_health_security(tmp_path):
    (tmp_path / "SECURITY.md").write_text("# Security")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Security policy")
    assert check.passed


def test_health_linter_editorconfig(tmp_path):
    (tmp_path / ".editorconfig").write_text("root = true\n")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Linter/Formatter")
    assert check.passed


def test_health_linter_ruff(tmp_path):
    (tmp_path / "ruff.toml").write_text("[lint]\n")
    report = analyze_health(tmp_path)
    check = next(c for c in report.checks if c.name == "Linter/Formatter")
    assert check.passed


def test_health_score_calculation(tmp_path):
    # 10 checks total; create items for all of them
    (tmp_path / "README.md").write_text("# X")
    (tmp_path / "LICENSE").write_text("MIT")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "Dockerfile").write_text("FROM python:3")
    (tmp_path / "CONTRIBUTING.md").write_text("# C")
    (tmp_path / "CHANGELOG.md").write_text("# C")
    (tmp_path / "SECURITY.md").write_text("# S")
    (tmp_path / ".editorconfig").write_text("root = true")

    report = analyze_health(tmp_path)
    assert report.score == 100


def test_health_partial_score(tmp_path):
    (tmp_path / "README.md").write_text("# X")
    (tmp_path / "LICENSE").write_text("MIT")
    report = analyze_health(tmp_path)
    assert 0 < report.score < 100
