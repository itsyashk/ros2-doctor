from __future__ import annotations

from ros2_doctor.scan import emit_markdown, scan_workspace


def test_scan_workspace(minimal_workspace):
    data = scan_workspace(minimal_workspace)
    assert data["packages"]
    assert data["packages"][0].name == "demo_pkg"


def test_emit_markdown(minimal_workspace):
    md = emit_markdown(minimal_workspace)
    assert "demo_pkg" in md
    assert "ROS 2 Workspace Scan" in md
