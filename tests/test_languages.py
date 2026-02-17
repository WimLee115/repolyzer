"""Tests for the languages analyzer."""

from pathlib import Path

from repolyzer.analyzers.languages import (
    EXTENSION_MAP,
    LanguageReport,
    LanguageStats,
    _count_lines,
    analyze_languages,
)


def test_extension_map_has_common_languages():
    assert EXTENSION_MAP[".py"] == "Python"
    assert EXTENSION_MAP[".rs"] == "Rust"
    assert EXTENSION_MAP[".js"] == "JavaScript"
    assert EXTENSION_MAP[".ts"] == "TypeScript"
    assert EXTENSION_MAP[".go"] == "Go"


def test_count_lines(tmp_path):
    f = tmp_path / "hello.py"
    f.write_text("line1\nline2\nline3\n")
    assert _count_lines(f) == 3


def test_count_lines_empty_file(tmp_path):
    f = tmp_path / "empty.py"
    f.write_text("")
    assert _count_lines(f) == 0


def test_count_lines_nonexistent():
    assert _count_lines(Path("/nonexistent/file.py")) == 0


def test_analyze_languages_single_file(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')\nprint('world')\n")
    report = analyze_languages(tmp_path)

    assert report.total_files == 1
    assert report.total_lines == 2
    assert len(report.languages) == 1
    assert report.languages[0].name == "Python"
    assert report.languages[0].files == 1
    assert report.languages[0].lines == 2


def test_analyze_languages_multiple_languages(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\ny = 2\nz = 3\n")
    (tmp_path / "lib.rs").write_text("fn main() {}\n")
    report = analyze_languages(tmp_path)

    assert report.total_files == 2
    assert report.total_lines == 4
    assert len(report.languages) == 2
    # Sorted by lines descending
    assert report.languages[0].name == "Python"
    assert report.languages[1].name == "Rust"


def test_analyze_languages_skips_dirs(tmp_path):
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "dep.js").write_text("var x = 1;\n")
    (tmp_path / "app.js").write_text("console.log('hi');\n")
    report = analyze_languages(tmp_path)

    assert report.total_files == 1
    assert report.languages[0].name == "JavaScript"


def test_analyze_languages_empty_dir(tmp_path):
    report = analyze_languages(tmp_path)
    assert report.total_files == 0
    assert report.total_lines == 0
    assert report.languages == []


def test_analyze_languages_ignores_unknown_extensions(tmp_path):
    (tmp_path / "data.xyz").write_text("some data\n")
    report = analyze_languages(tmp_path)
    assert report.total_files == 0


def test_tsx_jsx_mapped(tmp_path):
    (tmp_path / "comp.tsx").write_text("export default () => <div/>;\n")
    (tmp_path / "comp.jsx").write_text("export default () => <div/>;\n")
    report = analyze_languages(tmp_path)

    names = {lang.name for lang in report.languages}
    assert "TypeScript" in names
    assert "JavaScript" in names
