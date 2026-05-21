from __future__ import annotations

import os
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.distro import detect_distro, distro_install_path, is_known_distro
from ros2_doctor.core.environment import command_on_path, get_ros_distro


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    distro, hints = detect_distro(workspace)
    env_distro = get_ros_distro()

    if env_distro:
        status = CheckStatus.PASS if is_known_distro(env_distro) else CheckStatus.WARN
        results.append(
            CheckResult(
                id="ros_distro",
                title="ROS_DISTRO",
                status=status,
                message=f"ROS_DISTRO={env_distro}",
                category="ros_install",
            )
        )
        install = distro_install_path(env_distro)
        if install.exists():
            results.append(
                CheckResult(
                    id="ros_install_path",
                    title="ROS 2 installation",
                    status=CheckStatus.PASS,
                    message=f"Found {install}",
                    category="ros_install",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="ros_install_path",
                    title="ROS 2 installation",
                    status=CheckStatus.WARN,
                    message=f"/opt/ros/{env_distro} not found on disk.",
                    fix_command=f"sudo apt install ros-{env_distro}-desktop",
                    category="ros_install",
                )
            )
    else:
        results.append(
            CheckResult(
                id="ros_distro",
                title="ROS_DISTRO",
                status=CheckStatus.FAIL,
                message="ROS_DISTRO is not set.",
                fix_command="source /opt/ros/humble/setup.bash",
                category="ros_install",
            )
        )

    ros2 = command_on_path("ros2")
    if ros2:
        results.append(
            CheckResult(
                id="ros2_cli",
                title="ros2 CLI",
                status=CheckStatus.PASS,
                message=f"Available at {ros2}",
                category="ros_install",
            )
        )
    else:
        results.append(
            CheckResult(
                id="ros2_cli",
                title="ros2 CLI",
                status=CheckStatus.FAIL,
                message="ros2 not found on PATH.",
                fix_command="source /opt/ros/$ROS_DISTRO/setup.bash",
                category="ros_install",
            )
        )

    rmw = os.environ.get("RMW_IMPLEMENTATION", "")
    results.append(
        CheckResult(
            id="rmw",
            title="RMW implementation",
            status=CheckStatus.INFO,
            message=rmw or "(default — not explicitly set)",
            category="ros_install",
        )
    )

    domain = os.environ.get("ROS_DOMAIN_ID", "")
    if domain and domain != "0":
        results.append(
            CheckResult(
                id="ros_domain",
                title="ROS_DOMAIN_ID",
                status=CheckStatus.WARN,
                message=f"ROS_DOMAIN_ID={domain} — nodes on other domains will not see each other.",
                category="ros_install",
            )
        )
    else:
        results.append(
            CheckResult(
                id="ros_domain",
                title="ROS_DOMAIN_ID",
                status=CheckStatus.PASS,
                message=domain or "0 (default)",
                category="ros_install",
            )
        )

    if hints and env_distro:
        other = [d for d in hints if d != env_distro.lower()]
        if other:
            results.append(
                CheckResult(
                    id="distro_hints",
                    title="Distro hints in files",
                    status=CheckStatus.WARN,
                    message=f"Files mention other distros: {', '.join(other)}",
                    category="ros_install",
                )
            )

    return results
