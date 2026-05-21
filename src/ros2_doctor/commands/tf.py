from __future__ import annotations

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, section, show_banner, status_line
from ros2_doctor.graph.tf_tree import check_tf_topics, run_view_frames


def run_tf(ctx: CliContext) -> int:
    if not ctx.no_banner:
        show_banner()

    import shutil

    if not shutil.which("ros2"):
        status_line("TF", Status.SKIP, "ros2 not available.")
        return 1

    section("TF topics")
    tf = check_tf_topics()
    status_line(
        "/tf",
        Status.PASS if tf["has_tf"] else Status.WARN,
        "present" if tf["has_tf"] else "missing — start a transform broadcaster",
    )
    status_line(
        "/tf_static",
        Status.PASS if tf["has_tf_static"] else Status.WARN,
        "present" if tf["has_tf_static"] else "missing (ok if no static transforms)",
    )

    if ctx.dry_run:
        status_line("view_frames", Status.INFO, "Would run: ros2 run tf2_tools view_frames")
        return 0

    section("Frame tree")
    ok, text = run_view_frames()
    if ok and text.strip():
        for line in text.splitlines()[:30]:
            status_line("frames", Status.INFO, line[:100])
    else:
        status_line(
            "view_frames",
            Status.WARN,
            "Could not generate frame graph.",
            "sudo apt install ros-$ROS_DISTRO-tf2-tools",
        )
    return 0
