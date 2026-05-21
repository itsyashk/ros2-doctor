from __future__ import annotations

import shutil

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, section, show_banner, status_line
from ros2_doctor.core.config import load_config
from ros2_doctor.core.safety import confirm_action
from ros2_doctor.core.subprocess_runner import run_command
from ros2_doctor.core.workspace import find_workspace_root


def run_bag(
    ctx: CliContext,
    *,
    path: str | None = None,
    record: bool = False,
    duration: int = 30,
) -> int:
    if not ctx.no_banner:
        show_banner()

    if not shutil.which("ros2"):
        status_line("rosbag2", Status.SKIP, "ros2 not available.")
        return 1

    if path:
        section("Bag inspect")
        proc = run_command(["ros2", "bag", "info", path], timeout=30.0)
        print(proc.stdout or proc.stderr)
        return 0 if proc.ok else 1

    if not record:
        status_line(
            "bag", Status.INFO, "Use --record to start recording or pass PATH to inspect a bag."
        )
        status_line("Tip", Status.INFO, "ros2-doctor bag --record --dry-run")
        return 0

    root = ctx.workspace or find_workspace_root()
    cfg = load_config(root)
    topics = cfg.get("bag", {}).get(
        "default_topics",
        ["/tf", "/tf_static", "/rosout"],
    )
    cmd = ["ros2", "bag", "record", "-o", "ros2_doctor_bag", "--duration", str(duration), *topics]
    section("Record plan")
    status_line("Command", Status.INFO, " ".join(cmd))

    if ctx.dry_run:
        return 0

    if not confirm_action(f"Record {len(topics)} topics for {duration}s?", assume_yes=False):
        return 0

    proc = run_command(cmd, timeout=float(duration + 30))
    status_line("Record", Status.PASS if proc.ok else Status.FAIL, proc.stderr[:200] or "done")
    return 0 if proc.ok else 1
