from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: float | None = 120.0,
    env: dict[str, str] | None = None,
) -> CommandResult:
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return CommandResult(
            command=args,
            returncode=proc.returncode,
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            command=args,
            returncode=-1,
            stdout=exc.stdout or "" if exc.stdout else "",
            stderr=(exc.stderr or "") + "\n(timed out)",
            timed_out=True,
        )
    except FileNotFoundError:
        return CommandResult(
            command=args,
            returncode=127,
            stdout="",
            stderr=f"Command not found: {args[0]}",
        )
