from __future__ import annotations

from ros2_doctor.core.safety import ALLOWED_DELETE_NAMES, is_safe_workspace_child
from ros2_doctor.core.workspace import find_workspace_root


def test_find_workspace_root(minimal_workspace):
    root = find_workspace_root(minimal_workspace)
    assert root == minimal_workspace.resolve()


def test_find_workspace_none(tmp_path):
    assert find_workspace_root(tmp_path) is None


def test_safe_delete(minimal_workspace):
    for name in ALLOWED_DELETE_NAMES:
        path = minimal_workspace / name
        path.mkdir()
        assert is_safe_workspace_child(minimal_workspace, path)
    assert not is_safe_workspace_child(minimal_workspace, minimal_workspace / "src")
