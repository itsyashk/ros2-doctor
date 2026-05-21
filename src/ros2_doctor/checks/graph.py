from __future__ import annotations

import shutil
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.packages import list_package_names
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.core.workspace import find_workspace_root


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    if not shutil.which("ros2"):
        results.append(
            CheckResult(
                id="ros_graph",
                title="ROS graph",
                status=CheckStatus.SKIP,
                message="ros2 CLI not available",
                category="graph",
            )
        )
        return results

    nodes = run_command(["ros2", "node", "list"], timeout=8.0)
    node_lines = [line.strip() for line in nodes.stdout.splitlines() if line.strip()]
    if node_lines:
        results.append(
            CheckResult(
                id="nodes",
                title="Active nodes",
                status=CheckStatus.PASS,
                message=f"{len(node_lines)} node(s): {', '.join(node_lines[:5])}",
                category="graph",
            )
        )
    else:
        results.append(
            CheckResult(
                id="nodes",
                title="Active nodes",
                status=CheckStatus.WARN,
                message="No nodes running.",
                fix_command="ros2 launch <pkg> <launch_file>",
                category="graph",
            )
        )

    topics = run_command(["ros2", "topic", "list"], timeout=8.0)
    topic_lines = [line.strip() for line in topics.stdout.splitlines() if line.strip()]
    results.append(
        CheckResult(
            id="topics",
            title="Active topics",
            status=CheckStatus.PASS if topic_lines else CheckStatus.INFO,
            message=f"{len(topic_lines)} topic(s)"
            if topic_lines
            else "No topics (graph may be idle).",
            category="graph",
        )
    )

    root = workspace or find_workspace_root()
    if root and shutil.which("ros2"):
        expected = list_package_names(root)
        if expected:
            pkg_list = run_command(["ros2", "pkg", "list"], timeout=15.0)
            if pkg_list.ok:
                installed = set(pkg_list.stdout.splitlines())
                missing = [p for p in expected if p not in installed]
                if missing:
                    results.append(
                        CheckResult(
                            id="pkg_visibility",
                            title="Package visibility",
                            status=CheckStatus.FAIL,
                            message=f"Not visible via ros2 pkg list: {', '.join(missing[:5])}",
                            fix_command="source install/setup.bash",
                            category="graph",
                        )
                    )
                else:
                    results.append(
                        CheckResult(
                            id="pkg_visibility",
                            title="Package visibility",
                            status=CheckStatus.PASS,
                            message="Workspace packages appear in ros2 pkg list.",
                            category="graph",
                        )
                    )

    return results
