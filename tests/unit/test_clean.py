from __future__ import annotations

from ros2_doctor.core.safety import delete_workspace_artifacts


def test_clean_dry_run(minimal_workspace):
    for d in ("build", "install", "log"):
        (minimal_workspace / d).mkdir()
    results = delete_workspace_artifacts(minimal_workspace, dry_run=True)
    assert len(results) == 3
    assert all(msg == "would delete" for _, msg in results)
    assert (minimal_workspace / "build").exists()
