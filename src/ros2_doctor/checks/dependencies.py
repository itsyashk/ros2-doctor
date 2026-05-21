from __future__ import annotations

import shutil
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.core.workspace import find_workspace_root


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    root = workspace or find_workspace_root()
    if root is None:
        return results

    if not shutil.which("rosdep"):
        results.append(
            CheckResult(
                id="rosdep_check",
                title="rosdep dependency check",
                status=CheckStatus.SKIP,
                message="rosdep not available",
                category="dependencies",
            )
        )
        return results

    src = root / "src"
    if not src.is_dir():
        results.append(
            CheckResult(
                id="rosdep_check",
                title="rosdep dependency check",
                status=CheckStatus.SKIP,
                message="no src/ directory",
                category="dependencies",
            )
        )
        return results

    distro = get_ros_distro() or "humble"
    cmd = [
        "rosdep",
        "check",
        "--from-paths",
        "src",
        "--ignore-src",
        "--rosdistro",
        distro,
    ]
    proc = run_command(cmd, cwd=root, timeout=30.0)
    if proc.ok:
        results.append(
            CheckResult(
                id="rosdep_check",
                title="rosdep dependency check",
                status=CheckStatus.PASS,
                message="All dependencies satisfied (rosdep check).",
                category="dependencies",
            )
        )
    else:
        lines = (proc.stdout + proc.stderr).strip().splitlines()
        preview = "\n".join(lines[:5])
        results.append(
            CheckResult(
                id="rosdep_check",
                title="rosdep dependency check",
                status=CheckStatus.FAIL,
                message=preview or "rosdep reported missing dependencies",
                fix_command=f"rosdep install --from-paths src --ignore-src --rosdistro {distro}",
                category="dependencies",
            )
        )

    return results
