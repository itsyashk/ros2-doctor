#!/usr/bin/env python3
"""Thin wrapper around ros2_doctor.scan for skill checkout without pip install."""

from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap() -> None:
    repo_root = Path(__file__).resolve().parents[4]
    src = repo_root / "src"
    if src.is_dir() and str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main() -> int:
    _bootstrap()
    from ros2_doctor.scan import emit_markdown

    sys.stdout.write(emit_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
