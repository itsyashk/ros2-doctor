from __future__ import annotations

from ros2_doctor.core.environment import get_ros_env, parse_prefix_path


def test_get_ros_env(monkeypatch):
    monkeypatch.setenv("ROS_DISTRO", "humble")
    monkeypatch.setenv("AMENT_PREFIX_PATH", "/opt/ros/humble")
    env = get_ros_env()
    assert env["ROS_DISTRO"] == "humble"


def test_parse_prefix_path(monkeypatch):
    monkeypatch.setenv("AMENT_PREFIX_PATH", "/opt/ros/humble:/ws/install")
    paths = parse_prefix_path("AMENT_PREFIX_PATH")
    assert len(paths) == 2
