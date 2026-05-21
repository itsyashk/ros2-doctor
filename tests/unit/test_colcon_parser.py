from __future__ import annotations

from ros2_doctor.diagnostics.colcon_log_parser import find_failing_package, summarize_build_failure


def test_find_failing_package(sample_colcon_log):
    pkg, text = find_failing_package(sample_colcon_log)
    assert pkg == "failing_pkg"
    assert "missing_dep" in text


def test_summarize_build_failure(sample_colcon_log):
    summary = summarize_build_failure(sample_colcon_log, distro="humble")
    assert summary["package"] == "failing_pkg"
    assert summary["matches"]
