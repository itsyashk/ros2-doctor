from __future__ import annotations

import shutil

from ros2_doctor.core.subprocess_runner import CommandResult, run_command


def require_ros2() -> str | None:
    return shutil.which("ros2")


def ros2_topic_list() -> CommandResult:
    return run_command(["ros2", "topic", "list", "-t"], timeout=20.0)


def ros2_topic_info(topic: str) -> CommandResult:
    return run_command(["ros2", "topic", "info", topic, "-v"], timeout=15.0)


def ros2_node_list() -> CommandResult:
    return run_command(["ros2", "node", "list"], timeout=15.0)


def ros2_node_info(node: str) -> CommandResult:
    return run_command(["ros2", "node", "info", node], timeout=15.0)


def ros2_pkg_list() -> CommandResult:
    return run_command(["ros2", "pkg", "list"], timeout=60.0)
