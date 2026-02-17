"""Tests for the TODO/FIXME analyzer."""

from repolyzer.analyzers.todos import analyze_todos


def test_analyze_todos_finds_markers(tmp_path):
    (tmp_path / "app.py").write_text("""\
# TODO: fix this
x = 1
# FIXME: broken
# HACK: workaround
""")
    report = analyze_todos(tmp_path)
    assert report.total == 3
    assert report.counts["TODO"] == 1
    assert report.counts["FIXME"] == 1
    assert report.counts["HACK"] == 1


def test_analyze_todos_empty_project(tmp_path):
    report = analyze_todos(tmp_path)
    assert report.total == 0
    assert report.items == []


def test_analyze_todos_ignores_non_code(tmp_path):
    (tmp_path / "data.csv").write_text("TODO,value\n1,2\n")
    report = analyze_todos(tmp_path)
    assert report.total == 0


def test_analyze_todos_skips_dirs(tmp_path):
    nm = tmp_path / "node_modules"
    nm.mkdir()
    (nm / "dep.js").write_text("// TODO: something\n")
    (tmp_path / "app.js").write_text("// TODO: real todo\n")

    report = analyze_todos(tmp_path)
    assert report.total == 1


def test_analyze_todos_max_items(tmp_path):
    lines = "\n".join(f"# TODO: item {i}" for i in range(50))
    (tmp_path / "big.py").write_text(lines)
    report = analyze_todos(tmp_path, max_items=5)
    assert report.total == 50
    assert len(report.items) == 5


def test_analyze_todos_case_insensitive(tmp_path):
    (tmp_path / "app.py").write_text("# todo: lower\n# Todo: mixed\n")
    report = analyze_todos(tmp_path)
    assert report.counts["TODO"] == 2


def test_analyze_todos_one_marker_per_line(tmp_path):
    (tmp_path / "app.py").write_text("# TODO FIXME both on one line\n")
    report = analyze_todos(tmp_path)
    # Only one marker counted per line (first match wins)
    assert report.total == 1


def test_analyze_todos_item_content(tmp_path):
    (tmp_path / "app.py").write_text("# BUG: memory leak in parser\n")
    report = analyze_todos(tmp_path)
    assert report.items[0].marker == "BUG"
    assert "memory leak" in report.items[0].text
    assert report.items[0].line == 1
