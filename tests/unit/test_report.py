from __future__ import annotations

from ros2_doctor.report.markdown import generate_report


def test_generate_report(minimal_workspace):
    md = generate_report(minimal_workspace)
    assert "ros2-doctor Diagnostic Report" in md
    assert "demo_pkg" in md
