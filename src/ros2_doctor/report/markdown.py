from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ros2_doctor.checks.registry import run_all_checks
from ros2_doctor.core.environment import (
    detect_sourced_setup_files,
    get_os_info,
    get_python_info,
    get_ros_distro,
    get_ros_env,
    get_shell_name,
)
from ros2_doctor.core.overlay import analyze_overlay
from ros2_doctor.core.workspace import find_workspace_root
from ros2_doctor.graph.nodes import list_nodes
from ros2_doctor.graph.tf_tree import check_tf_topics
from ros2_doctor.graph.topics import list_topics_with_status
from ros2_doctor.scan import emit_markdown


def generate_report(workspace: Path | None = None) -> str:
    root = workspace or find_workspace_root()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = [
        "# ros2-doctor Diagnostic Report",
        "",
        f"**Generated:** {now}",
        "",
        "## System",
        f"- OS: {get_os_info()}",
        f"- Shell: {get_shell_name()}",
    ]
    py_exe, py_ver = get_python_info()
    lines.append(f"- Python: {py_ver} (`{py_exe}`)")
    lines.append(f"- ROS distro: `{get_ros_distro() or 'not set'}`")
    if root:
        lines.append(f"- Workspace: `{root}`")
    lines.append("")

    lines.append("## Sourced setup files")
    for p in detect_sourced_setup_files() or ["(none detected)"]:
        lines.append(f"- `{p}`")
    lines.append("")

    if root:
        overlay = analyze_overlay(root)
        lines.append("## Overlay")
        for p in overlay["ament_prefix_path"][:10]:
            lines.append(f"- `{p}`")
        lines.append("")

    lines.append("## Environment variables")
    for k, v in get_ros_env().items():
        lines.append(f"- `{k}`={v[:120]}{'...' if len(v) > 120 else ''}")
    lines.append("")

    if root:
        lines.append("## Workspace scan")
        lines.append(emit_markdown(root))
        lines.append("")

    summary = run_all_checks(root)
    lines.append("## Doctor checks")
    for r in summary.results:
        icon = {"pass": "OK", "warn": "WARN", "fail": "FAIL", "skip": "SKIP", "info": "INFO"}.get(
            r.status.value, "?"
        )
        lines.append(f"- [{icon}] **{r.title}**: {r.message}")
        if r.fix_command:
            lines.append(f"  - Fix: `{r.fix_command}`")
    lines.append("")

    topics, _ = list_topics_with_status()
    nodes, _ = list_nodes()
    tf = check_tf_topics() if __import__("shutil").which("ros2") else {}

    lines.append("## ROS graph")
    lines.append(f"- Topics: {len(topics)}")
    lines.append(f"- Nodes: {len(nodes)}")
    if tf:
        lines.append(f"- /tf: {'yes' if tf.get('has_tf') else 'no'}")
        lines.append(f"- /tf_static: {'yes' if tf.get('has_tf_static') else 'no'}")
    lines.append("")

    fixes = summary.fix_commands()
    if fixes:
        lines.append("## Recommended fixes")
        for cmd in fixes:
            lines.append(f"```bash\n{cmd}\n```")
        lines.append("")

    return "\n".join(lines)
