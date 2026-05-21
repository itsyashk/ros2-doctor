from __future__ import annotations

import shutil
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus


def run(workspace: Path | None) -> list[CheckResult]:
    _ = workspace
    results: list[CheckResult] = []

    for cmd, title in (("colcon", "colcon"), ("rosdep", "rosdep"), ("vcs", "vcstool")):
        found = shutil.which(cmd)
        if found:
            results.append(
                CheckResult(
                    id=cmd,
                    title=title,
                    status=CheckStatus.PASS,
                    message=f"available at {found}",
                    category="tooling",
                )
            )
        elif cmd == "vcs":
            results.append(
                CheckResult(
                    id=cmd,
                    title=title,
                    status=CheckStatus.INFO,
                    message="not on PATH (optional)",
                    category="tooling",
                )
            )
        else:
            results.append(
                CheckResult(
                    id=cmd,
                    title=title,
                    status=CheckStatus.FAIL,
                    message="not found on PATH",
                    fix_command=f"sudo apt install python3-{cmd}"
                    if cmd != "rosdep"
                    else "sudo apt install python3-rosdep",
                    category="tooling",
                )
            )

    return results
