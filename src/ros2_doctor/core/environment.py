from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path

ROS_ENV_PREFIXES = ("ROS_", "AMENT_", "CMAKE_PREFIX", "COLCON_", "RMW_", "RCUTILS_")
ROS_ENV_EXACT = ("PYTHONPATH", "LD_LIBRARY_PATH", "PATH")


def get_ros_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for key, value in os.environ.items():
        if any(key.startswith(p) for p in ROS_ENV_PREFIXES) or key in ROS_ENV_EXACT:
            env[key] = value
    return dict(sorted(env.items()))


def get_ros_distro() -> str:
    return os.environ.get("ROS_DISTRO", "").strip()


def get_shell_name() -> str:
    return os.environ.get("SHELL", "") or "unknown"


def get_python_info() -> tuple[str, str]:
    return (
        sys.executable,
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )


def get_virtual_env() -> str | None:
    return os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV")


def command_on_path(name: str) -> str | None:
    return shutil.which(name)


def get_os_info() -> str:
    return f"{platform.system()} {platform.release()} ({platform.machine()})"


def parse_prefix_path(var: str) -> list[str]:
    value = os.environ.get(var, "")
    if not value:
        return []
    # Try OS separator first, then colon (common in ROS docs even on Windows).
    parts: list[str] = []
    for sep in (os.pathsep, ":"):
        if sep in value:
            parts = [p for p in value.split(sep) if p]
            break
    return parts if parts else [value]


def detect_sourced_setup_files() -> list[str]:
    paths: list[str] = []
    for prefix in parse_prefix_path("AMENT_PREFIX_PATH"):
        for name in ("local_setup.bash", "local_setup.sh", "setup.bash", "setup.sh"):
            candidate = Path(prefix) / name
            if candidate.exists():
                paths.append(str(candidate))
    distro = get_ros_distro()
    if distro:
        for name in ("setup.bash", "setup.sh"):
            candidate = Path(f"/opt/ros/{distro}") / name
            if candidate.exists() and str(candidate) not in paths:
                paths.append(str(candidate))
    return paths
