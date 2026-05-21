from __future__ import annotations

import os
from pathlib import Path

from ros2_doctor.core.distro import distro_install_path
from ros2_doctor.core.environment import parse_prefix_path


def analyze_overlay(workspace: Path | None = None) -> dict:
    ament = parse_prefix_path("AMENT_PREFIX_PATH")
    cmake = parse_prefix_path("CMAKE_PREFIX_PATH")
    distro = os.environ.get("ROS_DISTRO", "")
    underlay = str(distro_install_path(distro)) if distro else ""
    ws_install = str(workspace / "install") if workspace else ""

    has_underlay = any(underlay and underlay in p for p in ament) if underlay else False
    has_overlay = any(ws_install and ws_install in p for p in ament) if ws_install else False

    issues: list[str] = []
    if distro and not has_underlay and ament:
        issues.append(
            "ROS underlay may not be sourced (AMENT_PREFIX_PATH missing /opt/ros/<distro>)."
        )
    if workspace and (workspace / "install").exists() and not has_overlay:
        issues.append("Workspace install/ exists but overlay may not be sourced.")

    distros_in_path = set()
    for p in ament:
        if "/opt/ros/" in p:
            part = p.split("/opt/ros/")[-1].split("/")[0]
            distros_in_path.add(part)
    if len(distros_in_path) > 1:
        issues.append(
            f"Multiple ROS distros in AMENT_PREFIX_PATH: {', '.join(sorted(distros_in_path))}"
        )

    return {
        "ament_prefix_path": ament,
        "cmake_prefix_path": cmake,
        "has_underlay": has_underlay,
        "has_overlay": has_overlay,
        "issues": issues,
    }
