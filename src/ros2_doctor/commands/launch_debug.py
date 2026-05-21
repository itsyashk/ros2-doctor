from __future__ import annotations

import shutil
import sys

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, print_fix_commands, section, show_banner, status_line
from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.diagnostics.launch_log_parser import analyze_launch_output


def run_launch_debug(
    ctx: CliContext,
    launch_args: list[str],
    *,
    timeout: float = 15.0,
) -> int:
    if not ctx.no_banner:
        show_banner()

    if not launch_args:
        status_line(
            "launch-debug",
            Status.FAIL,
            "Pass launch args after --",
            "ros2-doctor launch-debug -- <pkg> <launch_file>",
        )
        return 1

    if not shutil.which("ros2"):
        status_line("ros2", Status.FAIL, "ros2 not found.")
        return 1

    cmd = ["ros2", "launch", *launch_args]
    section("Launch debug")
    status_line("Command", Status.INFO, " ".join(cmd))

    if ctx.dry_run:
        return 0

    proc = run_command(cmd, timeout=timeout)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)

    if proc.ok:
        status_line("Launch", Status.PASS, "Launch command exited successfully.")
        return 0

    status_line("Launch", Status.FAIL, "Launch failed — see output above.")
    matches = analyze_launch_output(proc.stdout, proc.stderr, distro=get_ros_distro())
    for m in matches[:3]:
        status_line(m.category, Status.WARN, m.cause, m.fix_command)
    print_fix_commands([m.fix_command for m in matches if m.fix_command])
    return proc.returncode or 1
