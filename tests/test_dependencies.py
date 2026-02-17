"""Tests for the dependencies analyzer."""

import json

from repolyzer.analyzers.dependencies import (
    DependencyReport,
    analyze_dependencies,
    _parse_package_json,
    _parse_requirements_txt,
    _parse_cargo_toml,
    _parse_go_mod,
    _parse_pyproject_toml,
)


def test_parse_package_json(tmp_path):
    pj = tmp_path / "package.json"
    pj.write_text(json.dumps({
        "dependencies": {"react": "^18", "axios": "^1"},
        "devDependencies": {"jest": "^29"},
    }))
    deps, dev = _parse_package_json(pj)
    assert deps == 2
    assert dev == 1


def test_parse_package_json_empty(tmp_path):
    pj = tmp_path / "package.json"
    pj.write_text("{}")
    deps, dev = _parse_package_json(pj)
    assert deps == 0
    assert dev == 0


def test_parse_package_json_invalid(tmp_path):
    pj = tmp_path / "package.json"
    pj.write_text("not json")
    deps, dev = _parse_package_json(pj)
    assert deps == 0
    assert dev == 0


def test_parse_requirements_txt(tmp_path):
    req = tmp_path / "requirements.txt"
    req.write_text("flask>=2.0\nrequests\n# comment\n\n-r other.txt\n")
    deps, dev = _parse_requirements_txt(req)
    assert deps == 2
    assert dev == 0


def test_parse_cargo_toml(tmp_path):
    cargo = tmp_path / "Cargo.toml"
    cargo.write_text("""\
[package]
name = "myapp"

[dependencies]
serde = "1.0"
tokio = "1.0"

[dev-dependencies]
criterion = "0.5"
""")
    deps, dev = _parse_cargo_toml(cargo)
    assert deps == 2
    assert dev == 1


def test_parse_go_mod(tmp_path):
    gomod = tmp_path / "go.mod"
    gomod.write_text("""\
module example.com/myapp

go 1.21

require (
\tgithub.com/gin-gonic/gin v1.9.1
\tgithub.com/lib/pq v1.10.9
)
""")
    deps, dev = _parse_go_mod(gomod)
    assert deps == 2
    assert dev == 0


def test_parse_pyproject_toml(tmp_path):
    toml = tmp_path / "pyproject.toml"
    # Parser looks for [*.dependencies] section headers, not inline arrays
    toml.write_text("""\
[tool.poetry.dependencies]
"python" = "^3.9"
"rich" = ">=13.0"

[tool.poetry.dev-dependencies]
"pytest" = "^7.0"
""")
    deps, dev = _parse_pyproject_toml(toml)
    assert deps == 2
    assert dev == 1


def test_analyze_dependencies_finds_files(tmp_path):
    pj = tmp_path / "package.json"
    pj.write_text(json.dumps({
        "dependencies": {"express": "^4"},
    }))
    report = analyze_dependencies(tmp_path)
    assert report.total_deps == 1
    assert len(report.files) == 1
    assert report.files[0].name == "package.json"


def test_analyze_dependencies_no_files(tmp_path):
    report = analyze_dependencies(tmp_path)
    assert report.total_deps == 0
    assert report.files == []


def test_analyze_dependencies_multiple_files(tmp_path):
    (tmp_path / "requirements.txt").write_text("flask\nrequests\n")
    (tmp_path / "package.json").write_text(json.dumps({
        "dependencies": {"express": "^4"},
    }))
    report = analyze_dependencies(tmp_path)
    assert report.total_deps == 3
    assert len(report.files) == 2
