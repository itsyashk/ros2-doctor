from __future__ import annotations

from dataclasses import dataclass

from ros2_doctor.graph.ros2_cli import ros2_topic_list


@dataclass
class TopicInfo:
    name: str
    types: str
    publishers: int = 0
    subscribers: int = 0


def parse_topic_list(output: str) -> list[TopicInfo]:
    topics: list[TopicInfo] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("/rosout"):
            continue
        if "[" in line and "]" in line:
            name, rest = line.split("[", 1)
            types = rest.rstrip("]").strip()
            topics.append(TopicInfo(name=name.strip(), types=types))
        else:
            topics.append(TopicInfo(name=line, types=""))
    return topics


def list_topics_with_status() -> tuple[list[TopicInfo], str | None]:
    if not __import__("shutil").which("ros2"):
        return [], "ros2 CLI not found. Source your ROS 2 underlay first."
    result = ros2_topic_list()
    if not result.ok:
        return [], result.stderr or "ros2 topic list failed"
    return parse_topic_list(result.stdout), None


def check_expected_topics(expected: list[str], topics: list[TopicInfo]) -> list[str]:
    names = {t.name for t in topics}
    return [e for e in expected if e not in names]
