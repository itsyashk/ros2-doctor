from __future__ import annotations

import sys

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, section, show_banner, status_line
from ros2_doctor.graph.nodes import list_nodes, node_info


def run_nodes(ctx: CliContext, info_node: str | None = None) -> int:
    if not ctx.no_banner:
        show_banner()

    if info_node:
        section(f"Node info: {info_node}")
        sys.stdout.write(node_info(info_node))
        return 0

    nodes, err = list_nodes()
    if err:
        status_line("Nodes", Status.WARN, err)
        return 1

    section("ROS 2 nodes")
    if not nodes:
        status_line("Nodes", Status.WARN, "No active nodes.", "ros2 launch <pkg> <launch_file>")
        status_line(
            "Tip",
            Status.INFO,
            "Common causes: workspace not sourced, wrong ROS_DOMAIN_ID, or nothing launched yet.",
        )
        return 0

    for n in nodes:
        status_line(n, Status.PASS, "")
    return 0
