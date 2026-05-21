from __future__ import annotations

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, print_table, section, show_banner, status_line
from ros2_doctor.core.environment import (
    detect_sourced_setup_files,
    get_os_info,
    get_python_info,
    get_ros_distro,
    get_ros_env,
    get_shell_name,
    get_virtual_env,
)
from ros2_doctor.core.overlay import analyze_overlay
from ros2_doctor.core.workspace import find_workspace_root


def run_env(ctx: CliContext) -> int:
    if not ctx.no_banner:
        show_banner()

    section("System")
    status_line("OS", Status.INFO, get_os_info())
    status_line("Shell", Status.INFO, get_shell_name())
    py_exe, py_ver = get_python_info()
    venv = get_virtual_env()
    st = Status.WARN if venv else Status.PASS
    status_line("Python", st, f"{py_ver} — {py_exe}" + (f" (venv: {venv})" if venv else ""))

    section("ROS environment")
    distro = get_ros_distro()
    status_line(
        "ROS_DISTRO",
        Status.PASS if distro else Status.FAIL,
        distro or "not set",
        "source /opt/ros/humble/setup.bash" if not distro else "",
    )

    setup_files = detect_sourced_setup_files()
    for sf in setup_files[:5]:
        status_line("Sourced setup", Status.INFO, sf)

    root = ctx.workspace or find_workspace_root()
    if root:
        section("Workspace overlay")
        info = analyze_overlay(root)
        for issue in info["issues"]:
            status_line("Overlay", Status.WARN, issue)
        if not info["issues"]:
            status_line("Overlay", Status.PASS, "No obvious overlay issues detected.")

    section("Environment variables")
    rows = [[k, v[:80] + ("..." if len(v) > 80 else "")] for k, v in get_ros_env().items()]
    if rows:
        print_table("ROS-related variables", ["Variable", "Value"], rows)
    return 0
