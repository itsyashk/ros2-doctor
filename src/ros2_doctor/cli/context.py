from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CliContext:
    workspace: Path | None = None
    verbose: bool = False
    quiet: bool = False
    no_banner: bool = False
    dry_run: bool = False
