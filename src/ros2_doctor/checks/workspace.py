from __future__ import annotations

from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.packages import collect_packages
from ros2_doctor.core.workspace import find_workspace_root


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    root = workspace or find_workspace_root()

    if root is None:
        results.append(
            CheckResult(
                id="workspace_root",
                title="Workspace root",
                status=CheckStatus.FAIL,
                message="Could not detect workspace root.",
                fix_command="cd <workspace-root> or pass --workspace PATH",
                category="workspace",
            )
        )
        return results

    results.append(
        CheckResult(
            id="workspace_root",
            title="Workspace root",
            status=CheckStatus.PASS,
            message=str(root),
            category="workspace",
        )
    )

    src = root / "src"
    if src.is_dir():
        results.append(
            CheckResult(
                id="src_dir",
                title="src/ directory",
                status=CheckStatus.PASS,
                message="present",
                category="workspace",
            )
        )
    else:
        results.append(
            CheckResult(
                id="src_dir",
                title="src/ directory",
                status=CheckStatus.WARN,
                message="missing — typical colcon workspaces use src/",
                category="workspace",
            )
        )

    packages, issues = collect_packages(root)
    if packages:
        names = ", ".join(p.name for p in packages[:8])
        extra = f" (+{len(packages) - 8} more)" if len(packages) > 8 else ""
        results.append(
            CheckResult(
                id="packages",
                title="Packages found",
                status=CheckStatus.PASS,
                message=f"{len(packages)} package(s): {names}{extra}",
                category="workspace",
            )
        )
    else:
        results.append(
            CheckResult(
                id="packages",
                title="Packages found",
                status=CheckStatus.FAIL,
                message="No package.xml files found.",
                fix_command="find src -name package.xml",
                category="workspace",
            )
        )

    for issue in issues[:5]:
        results.append(
            CheckResult(
                id="package_issue",
                title="Package issue",
                status=CheckStatus.WARN,
                message=issue,
                category="workspace",
            )
        )

    return results
