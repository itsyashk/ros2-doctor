from __future__ import annotations

import shutil
from datetime import datetime

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, print_fix_commands, section, show_banner, status_line
from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.core.safety import confirm_action
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.core.workspace import require_workspace
from ros2_doctor.diagnostics.colcon_log_parser import summarize_build_failure


def run_build(
    ctx: CliContext,
    *,
    with_rosdep: bool = False,
    extra_args: list[str] | None = None,
) -> int:
    if not ctx.no_banner:
        show_banner()

    root = require_workspace(ctx.workspace)
    distro = get_ros_distro() or "humble"

    if not shutil.which("colcon"):
        status_line(
            "colcon",
            Status.FAIL,
            "colcon not found.",
            "sudo apt install python3-colcon-common-extensions",
        )
        return 1

    if with_rosdep and shutil.which("rosdep"):
        rosdep_cmd = [
            "rosdep",
            "install",
            "--from-paths",
            "src",
            "--ignore-src",
            "--rosdistro",
            distro,
        ]
        if ctx.dry_run:
            status_line("rosdep", Status.INFO, " ".join(rosdep_cmd))
        elif confirm_action("Run rosdep install before build?", assume_yes=False):
            run_command(rosdep_cmd, cwd=root, timeout=600.0)

    build_cmd = ["colcon", "build", "--symlink-install"]
    if extra_args:
        build_cmd.extend(extra_args)

    log_dir = root / "log"
    log_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    doctor_log = log_dir / f"ros2-doctor-build-{stamp}.log"

    section("Build")
    status_line("Command", Status.INFO, " ".join(build_cmd))

    if ctx.dry_run:
        status_line("Build", Status.INFO, "Dry run — build not executed.")
        return 0

    proc = run_command(build_cmd, cwd=root, timeout=3600.0)
    try:
        doctor_log.write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
    except OSError:
        pass

    if proc.ok:
        status_line("Build", Status.PASS, "colcon build succeeded.")
        status_line("Next", Status.INFO, "", "source install/setup.bash")
        return 0

    status_line("Build", Status.FAIL, "colcon build failed.")
    summary = summarize_build_failure(root, distro=distro)
    if summary["package"]:
        status_line("Failing package", Status.FAIL, summary["package"])
    if summary["log_dir"]:
        status_line("Logs", Status.INFO, summary["log_dir"])

    fixes = [m.fix_command for m in summary["matches"] if m.fix_command]
    if summary["package"]:
        fixes.insert(
            0,
            f"colcon build --packages-select {summary['package']} --event-handlers console_direct+",
        )
    fixes.append(f"sed -n '1,80p' log/latest_build/{summary['package'] or '<pkg>'}/stderr.log")
    print_fix_commands(fixes)
    return proc.returncode or 1
