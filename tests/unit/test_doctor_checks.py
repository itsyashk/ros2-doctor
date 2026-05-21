from __future__ import annotations

from ros2_doctor.checks.registry import run_all_checks


def test_run_all_checks(minimal_workspace, monkeypatch):
    monkeypatch.delenv("ROS_DISTRO", raising=False)
    summary = run_all_checks(minimal_workspace)
    assert summary.results
    titles = {r.title for r in summary.results}
    assert "Workspace root" in titles
