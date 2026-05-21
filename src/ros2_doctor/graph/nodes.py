from __future__ import annotations

from ros2_doctor.graph.ros2_cli import ros2_node_info, ros2_node_list


def list_nodes() -> tuple[list[str], str | None]:
    import shutil

    if not shutil.which("ros2"):
        return [], "ros2 CLI not found."
    result = ros2_node_list()
    if not result.ok:
        return [], result.stderr
    nodes = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return nodes, None


def node_info(node: str) -> str:
    result = ros2_node_info(node)
    return result.stdout if result.ok else result.stderr
