from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from ros2_doctor.core.subprocess_runner import run_command


def check_tf_topics() -> dict:
    result = run_command(["ros2", "topic", "list"], timeout=15.0)
    topics = set(result.stdout.splitlines()) if result.ok else set()
    return {
        "has_tf": "/tf" in topics,
        "has_tf_static": "/tf_static" in topics,
        "topics": topics,
    }


def run_view_frames(timeout: float = 30.0) -> tuple[bool, str]:
    if not shutil.which("ros2"):
        return False, "ros2 not available"
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "frames"
        result = run_command(
            ["ros2", "run", "tf2_tools", "view_frames", "--", "-o", str(out)],
            timeout=timeout,
        )
        yaml_path = Path(f"{out}.yaml")
        if yaml_path.exists():
            return True, yaml_path.read_text(encoding="utf-8", errors="replace")
        return result.ok, result.stdout + result.stderr
