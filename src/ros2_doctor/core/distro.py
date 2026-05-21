from __future__ import annotations

from pathlib import Path

from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.scan._scanner import KNOWN_DISTROS, find_distro_hints

__all__ = ["KNOWN_DISTROS", "detect_distro", "distro_install_path"]


def detect_distro(root: Path | None = None) -> tuple[str, dict[str, list[Path]]]:
    env = get_ros_distro()
    hints = find_distro_hints(root) if root else {}
    if env:
        return env, hints
    if hints:
        return next(iter(sorted(hints)), ""), hints
    return "", hints


def distro_install_path(distro: str) -> Path:
    return Path(f"/opt/ros/{distro}")


def is_known_distro(distro: str) -> bool:
    return distro.lower() in KNOWN_DISTROS
