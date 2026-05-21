from __future__ import annotations

from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.environment import (
    get_os_info,
    get_python_info,
    get_shell_name,
    get_virtual_env,
)


def run(workspace: Path | None) -> list[CheckResult]:
    _ = workspace
    results: list[CheckResult] = []

    results.append(
        CheckResult(
            id="os",
            title="Operating system",
            status=CheckStatus.INFO,
            message=get_os_info(),
            category="system",
        )
    )

    shell = get_shell_name()
    results.append(
        CheckResult(
            id="shell",
            title="Shell",
            status=CheckStatus.PASS if shell != "unknown" else CheckStatus.WARN,
            message=shell,
            category="system",
        )
    )

    py_exe, py_ver = get_python_info()
    py_status = CheckStatus.PASS
    py_msg = f"{py_ver} ({py_exe})"
    if "venv" in py_exe.lower() or get_virtual_env():
        py_status = CheckStatus.WARN
        venv = get_virtual_env() or "active venv"
        py_msg += f" — virtual environment detected ({venv}). This can conflict with system rclpy."
        fix = "deactivate && source /opt/ros/$ROS_DISTRO/setup.bash"
    else:
        fix = ""
    results.append(
        CheckResult(
            id="python",
            title="Python",
            status=py_status,
            message=py_msg,
            fix_command=fix,
            category="system",
        )
    )

    return results
