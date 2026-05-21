from __future__ import annotations

import sys
from pathlib import Path

from ros2_doctor.cli.context import CliContext
from ros2_doctor.cli.output import show_banner
from ros2_doctor.core.workspace import find_workspace_root
from ros2_doctor.report.markdown import generate_report


def run_report(ctx: CliContext, output: Path | None = None) -> int:
    if not ctx.no_banner:
        show_banner()

    root = ctx.workspace or find_workspace_root()
    md = generate_report(root)

    if output:
        output.write_text(md, encoding="utf-8")
        print(f"Report written to {output}")
    else:
        sys.stdout.write(md)
    return 0
