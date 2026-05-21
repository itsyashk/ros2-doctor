from __future__ import annotations

import os
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.overlay import analyze_overlay


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    info = analyze_overlay(workspace)

    ament = os.environ.get("AMENT_PREFIX_PATH", "")
    if ament:
        results.append(
            CheckResult(
                id="ament_prefix",
                title="AMENT_PREFIX_PATH",
                status=CheckStatus.PASS,
                message=f"{len(info['ament_prefix_path'])} entries",
                category="overlay",
            )
        )
    else:
        results.append(
            CheckResult(
                id="ament_prefix",
                title="AMENT_PREFIX_PATH",
                status=CheckStatus.FAIL,
                message="Not set — ROS workspace is likely not sourced.",
                fix_command="source /opt/ros/$ROS_DISTRO/setup.bash",
                category="overlay",
            )
        )

    cmake = os.environ.get("CMAKE_PREFIX_PATH", "")
    results.append(
        CheckResult(
            id="cmake_prefix",
            title="CMAKE_PREFIX_PATH",
            status=CheckStatus.PASS if cmake else CheckStatus.WARN,
            message="set" if cmake else "not set",
            category="overlay",
        )
    )

    ros_pkg = os.environ.get("ROS_PACKAGE_PATH", "")
    if ros_pkg:
        results.append(
            CheckResult(
                id="ros_package_path",
                title="ROS_PACKAGE_PATH",
                status=CheckStatus.WARN,
                message="ROS_PACKAGE_PATH is set (ROS 1 legacy); usually not needed in ROS 2.",
                category="overlay",
            )
        )

    if info["has_underlay"]:
        results.append(
            CheckResult(
                id="underlay",
                title="ROS underlay sourced",
                status=CheckStatus.PASS,
                message="Underlay appears in prefix path.",
                category="overlay",
            )
        )
    elif ament:
        results.append(
            CheckResult(
                id="underlay",
                title="ROS underlay sourced",
                status=CheckStatus.WARN,
                message="Underlay may be missing from AMENT_PREFIX_PATH.",
                fix_command="source /opt/ros/$ROS_DISTRO/setup.bash",
                category="overlay",
            )
        )

    if workspace and (workspace / "install").exists():
        if info["has_overlay"]:
            results.append(
                CheckResult(
                    id="overlay",
                    title="Workspace overlay sourced",
                    status=CheckStatus.PASS,
                    message="Workspace install/ is in AMENT_PREFIX_PATH.",
                    category="overlay",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="overlay",
                    title="Workspace overlay sourced",
                    status=CheckStatus.FAIL,
                    message="install/ exists but workspace overlay may not be sourced.",
                    fix_command="source install/setup.bash",
                    category="overlay",
                )
            )

    for issue in info["issues"]:
        results.append(
            CheckResult(
                id="overlay_issue",
                title="Overlay issue",
                status=CheckStatus.WARN,
                message=issue,
                category="overlay",
            )
        )

    return results
