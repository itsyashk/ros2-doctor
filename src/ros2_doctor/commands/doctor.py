from __future__ import annotations

from ros2_doctor.checks.base import CheckStatus
from ros2_doctor.checks.registry import run_all_checks
from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import (
    Status,
    print_fix_commands,
    print_summary,
    section,
    show_banner,
    status_line,
)
from ros2_doctor.core.workspace import find_workspace_root


def _map_status(s: CheckStatus) -> Status:
    return {
        CheckStatus.PASS: Status.PASS,
        CheckStatus.WARN: Status.WARN,
        CheckStatus.FAIL: Status.FAIL,
        CheckStatus.SKIP: Status.SKIP,
        CheckStatus.INFO: Status.INFO,
    }[s]


def run_doctor(ctx: CliContext, category: str | None = None) -> int:
    if not ctx.no_banner:
        show_banner()

    root = ctx.workspace or find_workspace_root()
    section("Doctor check")
    if root:
        status_line("Workspace", Status.INFO, str(root))
    else:
        status_line("Workspace", Status.WARN, "Not detected — some checks skipped.")

    summary = run_all_checks(root, category=category)
    for result in summary.results:
        status_line(
            result.title,
            _map_status(result.status),
            result.message,
            result.fix_command,
        )

    passed, warned, failed, skipped = summary.counts()
    print_summary(passed, warned, failed, skipped)
    print_fix_commands(summary.fix_commands())
    return 1 if failed else 0
