from __future__ import annotations

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, section, show_banner, status_line
from ros2_doctor.core.safety import confirm_action, delete_workspace_artifacts
from ros2_doctor.core.workspace import (
    dir_size,
    format_size,
    require_workspace,
    workspace_child_paths,
)


def run_clean(ctx: CliContext, *, yes: bool = False) -> int:
    if not ctx.no_banner:
        show_banner()

    root = require_workspace(ctx.workspace)
    paths = workspace_child_paths(root)

    section("Clean workspace artifacts")
    if not paths:
        status_line("Clean", Status.INFO, "Nothing to delete (build/, install/, log/ missing).")
        return 0

    for path in paths:
        size = format_size(dir_size(path))
        action = "would delete" if ctx.dry_run else "pending"
        status_line(path.name, Status.WARN, f"{path} ({size}) — {action}")

    if ctx.dry_run:
        return 0

    if not confirm_action(
        f"Delete {len(paths)} director{'y' if len(paths) == 1 else 'ies'} under {root}?",
        assume_yes=yes,
    ):
        status_line("Clean", Status.INFO, "Cancelled.")
        return 0

    results = delete_workspace_artifacts(root, dry_run=False)
    for path, msg in results:
        status_line(path.name, Status.PASS if msg == "deleted" else Status.WARN, msg)
    return 0
