from __future__ import annotations

import sys
from pathlib import Path

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import Status, print_fix_commands, section, show_banner, status_line
from ros2_doctor.core.environment import get_ros_distro
from ros2_doctor.diagnostics.error_classifier import classify_error


def run_explain_error(
    ctx: CliContext,
    text: str | None = None,
    file: Path | None = None,
) -> int:
    if not ctx.no_banner:
        show_banner()

    if file:
        content = file.read_text(encoding="utf-8", errors="replace")
    elif text:
        content = text
    else:
        content = sys.stdin.read()

    if not content.strip():
        status_line(
            "explain-error", Status.FAIL, "No input. Use --text, --file, or pipe log content."
        )
        return 1

    matches = classify_error(content, distro=get_ros_distro())
    section("Error analysis")

    if not matches:
        status_line(
            "Match",
            Status.WARN,
            "No known pattern matched. Paste more log context or check colcon stderr.log.",
        )
        return 1

    for m in matches[:5]:
        status_line(
            m.category,
            Status.WARN if m.category != "build" else Status.FAIL,
            f"{m.cause}\n  Matched: {m.matched_text[:120]}",
            m.fix_command,
        )
        if m.playbook:
            status_line(
                "Playbook", Status.INFO, f".claude/skills/ros2-doctor/playbooks/{m.playbook}.md"
            )

    print_fix_commands([m.fix_command for m in matches if m.fix_command])
    return 0
