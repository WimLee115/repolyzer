"""Tests for the structure analyzer."""

from repolyzer.analyzers.structure import StructureReport, analyze_structure


def test_size_human_bytes():
    r = StructureReport(total_size_bytes=500)
    assert r.size_human == "500.0 B"


def test_size_human_kb():
    r = StructureReport(total_size_bytes=2048)
    assert r.size_human == "2.0 KB"


def test_size_human_mb():
    r = StructureReport(total_size_bytes=5 * 1024 * 1024)
    assert r.size_human == "5.0 MB"


def test_analyze_structure_basic(tmp_path):
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.txt").write_text("world!")
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "file3.txt").write_text("nested")

    report = analyze_structure(tmp_path)

    assert report.total_files == 3
    assert report.total_dirs >= 1
    assert report.total_size_bytes > 0
    assert report.max_depth >= 1


def test_analyze_structure_empty_dir(tmp_path):
    report = analyze_structure(tmp_path)
    assert report.total_files == 0
    assert report.total_size_bytes == 0


def test_analyze_structure_skips_dirs(tmp_path):
    git = tmp_path / ".git"
    git.mkdir()
    (git / "HEAD").write_text("ref: refs/heads/main")
    (tmp_path / "src.py").write_text("x = 1")

    report = analyze_structure(tmp_path)
    # .git/HEAD should not be counted
    assert report.total_files == 1


def test_analyze_structure_largest_files(tmp_path):
    (tmp_path / "small.txt").write_text("a")
    (tmp_path / "big.txt").write_text("a" * 10000)
    (tmp_path / "medium.txt").write_text("a" * 100)

    report = analyze_structure(tmp_path)
    assert len(report.largest_files) == 3
    # Sorted largest first
    assert report.largest_files[0][1] >= report.largest_files[1][1]


def test_analyze_structure_deep_nesting(tmp_path):
    d = tmp_path
    for i in range(5):
        d = d / f"level{i}"
        d.mkdir()
    (d / "deep.txt").write_text("deep")

    report = analyze_structure(tmp_path)
    assert report.max_depth >= 5
