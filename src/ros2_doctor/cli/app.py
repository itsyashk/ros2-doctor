from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

import typer

from ros2_doctor import __version__
from ros2_doctor.cli.context import CliContext
from ros2_doctor.commands import (
    bag,
    build,
    clean,
    deps,
    doctor,
    env,
    explain_error,
    launch_debug,
    nodes,
    report_cmd,
    tf,
    topics,
)

app = typer.Typer(
    name="ros2-doctor",
    help="Friendly ROS 2 workspace diagnostics — doctor, build, deps, topics, TF, and more.",
    no_args_is_help=True,
    add_completion=False,
)


def _ctx(
    workspace: Path | None,
    verbose: bool,
    quiet: bool,
    no_banner: bool,
    dry_run: bool,
) -> CliContext:
    no_banner = no_banner or bool(os.environ.get("ROS2_DOCTOR_NO_BANNER"))
    return CliContext(
        workspace=workspace,
        verbose=verbose,
        quiet=quiet,
        no_banner=no_banner,
        dry_run=dry_run,
    )


@app.callback()
def main_callback(
    version: Annotated[
        bool | None,
        typer.Option("--version", "-V", help="Show version and exit."),
    ] = None,
) -> None:
    if version:
        typer.echo(f"ros2-doctor {__version__}")
        raise typer.Exit()


@app.command("doctor")
def cmd_doctor(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    category: Annotated[
        str | None, typer.Option("--category", help="Filter: system, workspace, deps, graph, ros")
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", "-q")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Run full workspace and environment diagnostics."""
    raise typer.Exit(doctor.run_doctor(_ctx(workspace, verbose, quiet, no_banner, False), category))


@app.command("env")
def cmd_env(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Show ROS environment, overlay chain, and warnings."""
    raise typer.Exit(env.run_env(_ctx(workspace, False, False, no_banner, False)))


@app.command("deps")
def cmd_deps(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    install: Annotated[
        bool, typer.Option("--install", help="Run rosdep install after check (asks confirmation).")
    ] = False,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Show commands without running.")
    ] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Check rosdep dependencies and suggest install commands."""
    raise typer.Exit(
        deps.run_deps(_ctx(workspace, False, False, no_banner, dry_run), install=install)
    )


@app.command("build")
def cmd_build(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    rosdep: Annotated[
        bool, typer.Option("--rosdep", help="Optionally run rosdep install first.")
    ] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
    colcon_args: Annotated[
        list[str] | None, typer.Argument(help="Extra args passed to colcon after --")
    ] = None,
) -> None:
    """Build workspace with colcon and summarize failures."""
    raise typer.Exit(
        build.run_build(
            _ctx(workspace, False, False, no_banner, dry_run),
            with_rosdep=rosdep,
            extra_args=colcon_args,
        )
    )


@app.command("clean")
def cmd_clean(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Skip confirmation.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Remove build/, install/, and log/ from workspace (with confirmation)."""
    raise typer.Exit(clean.run_clean(_ctx(workspace, False, False, no_banner, dry_run), yes=yes))


@app.command("report")
def cmd_report(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    output: Annotated[
        Path | None, typer.Option("-o", "--output", help="Write markdown report to file.")
    ] = None,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Generate a markdown diagnostic report."""
    raise typer.Exit(report_cmd.run_report(_ctx(workspace, False, False, no_banner, False), output))


@app.command("topics")
def cmd_topics(
    workspace: Annotated[Path | None, typer.Option("--workspace", "-w")] = None,
    expect: Annotated[
        list[str] | None, typer.Option("--expect", help="Warn if topic missing.")
    ] = None,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """List ROS 2 topics with cleaner formatting."""
    raise typer.Exit(
        topics.run_topics(_ctx(workspace, False, False, no_banner, False), expect=expect)
    )


@app.command("nodes")
def cmd_nodes(
    info: Annotated[
        str | None, typer.Option("--info", help="Show ros2 node info for NODE.")
    ] = None,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """List active ROS 2 nodes."""
    raise typer.Exit(nodes.run_nodes(_ctx(None, False, False, no_banner, False), info_node=info))


@app.command("tf")
def cmd_tf(
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Check /tf, /tf_static, and frame connectivity."""
    raise typer.Exit(tf.run_tf(_ctx(None, False, False, no_banner, dry_run)))


@app.command("bag")
def cmd_bag(
    path: Annotated[str | None, typer.Argument(help="Bag path to inspect.")] = None,
    record: Annotated[
        bool, typer.Option("--record", help="Record a short bag (asks confirmation).")
    ] = False,
    duration: Annotated[int, typer.Option("--duration", help="Record duration in seconds.")] = 30,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Inspect or record rosbag2 (with safety prompts)."""
    raise typer.Exit(
        bag.run_bag(
            _ctx(None, False, False, no_banner, dry_run),
            path=path,
            record=record,
            duration=duration,
        )
    )


@app.command("launch-debug")
def cmd_launch_debug(
    launch_args: Annotated[
        list[str] | None, typer.Argument(help="ros2 launch args: <pkg> <file> ...")
    ] = None,
    timeout: Annotated[
        float, typer.Option("--timeout", help="Seconds before stopping launch probe.")
    ] = 15.0,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Run ros2 launch and classify common errors."""
    raise typer.Exit(
        launch_debug.run_launch_debug(
            _ctx(None, False, False, no_banner, dry_run),
            launch_args or [],
            timeout=timeout,
        )
    )


@app.command("explain-error")
def cmd_explain_error(
    text: Annotated[
        str | None, typer.Option("--text", "-t", help="Error text to classify.")
    ] = None,
    file: Annotated[Path | None, typer.Option("--file", "-f", help="Log file to read.")] = None,
    no_banner: Annotated[bool, typer.Option("--no-banner")] = False,
) -> None:
    """Explain colcon, rosdep, launch, or TF errors without an LLM."""
    raise typer.Exit(
        explain_error.run_explain_error(
            _ctx(None, False, False, no_banner, False), text=text, file=file
        )
    )


def main() -> None:
    import sys

    if "--version" in sys.argv or "-V" in sys.argv:
        typer.echo(f"ros2-doctor {__version__}")
        raise SystemExit(0)
    app()


if __name__ == "__main__":
    main()
