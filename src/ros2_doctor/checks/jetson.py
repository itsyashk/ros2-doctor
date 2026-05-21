from __future__ import annotations

import os
from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.environment import get_os_info


def run(workspace: Path | None) -> list[CheckResult]:
    _ = workspace
    results: list[CheckResult] = []
    os_info = get_os_info().lower()

    if "aarch64" not in os_info and "arm" not in os_info:
        return results

    tegra = Path("/etc/nv_tegra_release")
    if tegra.exists():
        text = tegra.read_text(encoding="utf-8", errors="replace")[:200]
        results.append(
            CheckResult(
                id="jetson_detected",
                title="Jetson / Tegra platform",
                status=CheckStatus.INFO,
                message=f"Detected embedded platform: {text.strip()[:80]}",
                category="jetson",
            )
        )

    ld = os.environ.get("LD_LIBRARY_PATH", "")
    if len(ld) > 500:
        results.append(
            CheckResult(
                id="jetson_ld_path",
                title="LD_LIBRARY_PATH length",
                status=CheckStatus.WARN,
                message="LD_LIBRARY_PATH is very long; sourcing order issues are common on Jetson.",
                fix_command="source /opt/ros/$ROS_DISTRO/setup.bash before workspace overlay",
                category="jetson",
            )
        )

    cuda = os.environ.get("CUDA_HOME") or os.environ.get("CUDA_PATH")
    if cuda and "ros" not in ld.lower():
        results.append(
            CheckResult(
                id="jetson_cuda",
                title="CUDA environment",
                status=CheckStatus.INFO,
                message=f"CUDA paths set ({cuda}); ensure ROS underlay is sourced after CUDA if imports fail.",
                category="jetson",
            )
        )

    return results
