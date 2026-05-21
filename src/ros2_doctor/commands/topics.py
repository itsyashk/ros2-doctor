from __future__ import annotations

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, print_table, section, show_banner, status_line
from ros2_doctor.core.config import load_config
from ros2_doctor.core.workspace import find_workspace_root
from ros2_doctor.graph.topics import check_expected_topics, list_topics_with_status


def run_topics(ctx: CliContext, expect: list[str] | None = None) -> int:
    if not ctx.no_banner:
        show_banner()

    topics, err = list_topics_with_status()
    if err:
        status_line("Topics", Status.WARN, err, "source /opt/ros/$ROS_DISTRO/setup.bash")
        return 1

    section("ROS 2 topics")
    rows = [[t.name, t.types] for t in sorted(topics, key=lambda x: x.name)]
    print_table("Topics", ["Name", "Type"], rows[:50])

    root = ctx.workspace or find_workspace_root()
    cfg = load_config(root)
    expected = expect or cfg.get("doctor", {}).get("expected_topics", [])
    if expected:
        missing = check_expected_topics(expected, topics)
        for m in missing:
            status_line("Missing topic", Status.WARN, m)

    if not topics:
        status_line("Graph", Status.WARN, "No topics — launch nodes or check ROS_DOMAIN_ID.")
    return 0
