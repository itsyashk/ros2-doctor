from __future__ import annotations

from pathlib import Path

from ros2_doctor.checks.base import CheckResult, CheckStatus
from ros2_doctor.core.workspace import find_workspace_root
from ros2_doctor.scan._scanner import artifact_issues


def run(workspace: Path | None) -> list[CheckResult]:
    results: list[CheckResult] = []
    root = workspace or find_workspace_root()
    if root is None:
        return results

    for dirname in ("build", "install", "log"):
        path = root / dirname
        if path.exists():
            results.append(
                CheckResult(
                    id=f"artifact_{dirname}",
                    title=f"{dirname}/",
                    status=CheckStatus.INFO,
                    message="present",
                    category="artifacts",
                )
            )
        else:
            results.append(
                CheckResult(
                    id=f"artifact_{dirname}",
                    title=f"{dirname}/",
                    status=CheckStatus.INFO,
                    message="missing",
                    category="artifacts",
                )
            )

    for issue in artifact_issues(root)[:3]:
        results.append(
            CheckResult(
                id="stale_artifact",
                title="Build artifacts",
                status=CheckStatus.WARN,
                message=issue,
                fix_command="ros2-doctor clean --dry-run",
                category="artifacts",
            )
        )

    return results
