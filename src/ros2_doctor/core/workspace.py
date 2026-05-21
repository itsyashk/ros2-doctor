from __future__ import annotations

from pathlib import Path

from ros2_doctor.scan._scanner import iter_package_xmls

WORKSPACE_MARKERS = ("src", "build", "install", "log")
CLEAN_DIRS = frozenset({"build", "install", "log"})


def find_workspace_root(start: Path | None = None, *, force: bool = False) -> Path | None:
    """Walk parents to find a colcon-style workspace root."""
    current = (start or Path.cwd()).resolve()
    home = Path.home().resolve()

    for candidate in [current, *current.parents]:
        if not force and candidate == home.parent:
            break
        if _looks_like_workspace(candidate):
            return candidate
    return None


def _looks_like_workspace(path: Path) -> bool:
    src = path / "src"
    if src.is_dir():
        xmls = [p for p in iter_package_xmls(path) if "src" in p.parts]
        if xmls:
            return True
    build = path / "build"
    install = path / "install"
    if build.is_dir() and install.is_dir():
        return True
    return False


def require_workspace(start: Path | None = None) -> Path:
    root = find_workspace_root(start)
    if root is None:
        raise WorkspaceNotFoundError(
            "Could not detect a ROS 2 workspace. Run from a directory with "
            "`src/` and package.xml files, or pass --workspace PATH."
        )
    return root


def workspace_child_paths(root: Path) -> list[Path]:
    return [root / name for name in CLEAN_DIRS if (root / name).exists()]


def dir_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return 0
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def format_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}" if unit != "B" else f"{num_bytes} B"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


class WorkspaceNotFoundError(Exception):
    pass
