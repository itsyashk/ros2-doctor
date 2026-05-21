from __future__ import annotations

from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ros2_doctor import __version__
from ros2_doctor.cli.banner import BANNER, SUBTITLE

console = Console()


class Status(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    INFO = "info"
    SKIP = "skip"


STATUS_STYLE = {
    Status.PASS: ("green", "[OK]"),
    Status.WARN: ("yellow", "[!]"),
    Status.FAIL: ("red", "[X]"),
    Status.INFO: ("blue", "[i]"),
    Status.SKIP: ("dim", "[-]"),
}


def show_banner() -> None:
    console.print(BANNER, style="bold cyan")
    console.print(f"{SUBTITLE}  [dim]v{__version__}[/dim]\n")


def section(title: str) -> None:
    console.print(f"\n[bold]--- {title} ---[/bold]")


def status_line(
    title: str,
    status: Status,
    message: str = "",
    fix: str = "",
) -> None:
    color, icon = STATUS_STYLE[status]
    line = f"[{color}]{icon}[/{color}] {title}"
    if message:
        line += f"\n    {message}"
    if fix:
        line += f"\n    [cyan]Fix:[/cyan] [bold cyan]{fix}[/bold cyan]"
    console.print(line)


def print_fix_commands(commands: list[str], limit: int = 5) -> None:
    if not commands:
        return
    section("Try next")
    for i, cmd in enumerate(commands[:limit], 1):
        console.print(f"  {i}. [bold cyan]{cmd}[/bold cyan]")


def print_summary(passed: int, warned: int, failed: int, skipped: int = 0) -> None:
    section("Summary")
    parts = []
    if passed:
        parts.append(f"[green]{passed} passed[/green]")
    if warned:
        parts.append(f"[yellow]{warned} warnings[/yellow]")
    if failed:
        parts.append(f"[red]{failed} failed[/red]")
    if skipped:
        parts.append(f"[dim]{skipped} skipped[/dim]")
    console.print("  ".join(parts) if parts else "  No checks run.")


def print_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    table = Table(title=title, show_header=True, header_style="bold")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def print_panel(title: str, body: str, style: str = "") -> None:
    console.print(Panel(body, title=title, border_style=style or "blue"))
