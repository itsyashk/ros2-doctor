from __future__ import annotations

import shutil

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, section, show_banner, status_line
from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.core.safety import confirm_action
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.core.workspace import require_workspace


def run_deps(
    ctx: CliContext,
    *,
    install: bool = False,
) -> int:
    if not ctx.no_banner:
        show_banner()

    root = require_workspace(ctx.workspace)
    distro = get_ros_distro() or "humble"

    if not shutil.which("rosdep"):
        status_line(
            "rosdep",
            Status.FAIL,
            "rosdep not found on PATH.",
            "sudo apt install python3-rosdep && sudo rosdep init",
        )
        return 1

    section("Dependency check")
    cmd = ["rosdep", "check", "--from-paths", "src", "--ignore-src", "--rosdistro", distro]
    if ctx.dry_run:
        status_line("Plan", Status.INFO, " ".join(cmd))
        return 0

    proc = run_command(cmd, cwd=root, timeout=300.0)
    output = (proc.stdout + proc.stderr).strip()
    if proc.ok:
        status_line("rosdep check", Status.PASS, "All dependencies satisfied.")
        return 0

    status_line("rosdep check", Status.FAIL, output[:500])
    fix = f"rosdep install --from-paths src --ignore-src --rosdistro {distro}"
    status_line("Suggested fix", Status.INFO, "", fix)

    if install:
        if ctx.dry_run:
            status_line("Install", Status.INFO, f"Would run: {fix}")
            return 0
        if not confirm_action("Run rosdep install (may use apt)?", assume_yes=ctx.quiet):
            return 1
        inst = run_command(fix.split(), cwd=root, timeout=600.0)
        if inst.ok:
            status_line("rosdep install", Status.PASS, "Completed.")
            return 0
        status_line("rosdep install", Status.FAIL, inst.stderr[:400])
        return 1

    return 1
