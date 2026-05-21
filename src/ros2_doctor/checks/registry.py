from __future__ import annotations

from pathlib import Path

from ros2_doctor.checks import (
    artifacts,
    dependencies,
    graph,
    jetson,
    ros_install,
    system,
    tooling,
)
from ros2_doctor.checks import (
    overlay as overlay_checks,
)
from ros2_doctor.checks import (
    workspace as workspace_checks,
)
from ros2_doctor.checks.base import CheckSummary

CATEGORIES = {
    "system": ["system", "jetson"],
    "workspace": ["workspace", "artifacts"],
    "deps": ["dependencies", "tooling"],
    "graph": ["graph"],
    "ros": ["ros_install", "overlay"],
}


def run_all_checks(
    workspace: Path | None,
    *,
    category: str | None = None,
) -> CheckSummary:
    summary = CheckSummary()
    modules = [
        system.run,
        jetson.run,
        ros_install.run,
        overlay_checks.run,
        workspace_checks.run,
        artifacts.run,
        tooling.run,
        dependencies.run,
        graph.run,
    ]
    for run_fn in modules:
        for result in run_fn(workspace):
            if category and result.category != category:
                if not _category_match(category, result.category):
                    continue
            summary.results.append(result)
    return summary


def _category_match(filter_cat: str, result_cat: str) -> bool:
    allowed = CATEGORIES.get(filter_cat, [filter_cat])
    return result_cat in allowed
