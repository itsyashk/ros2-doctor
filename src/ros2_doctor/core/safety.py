from __future__ import annotations

import shutil
from pathlib import Path

from ros2_doctor.core.workspace import CLEAN_DIRS

ALLOWED_DELETE_NAMES = CLEAN_DIRS


def is_safe_workspace_child(root: Path, target: Path) -> bool:
    root = root.resolve()
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return False
    if target == root:
        return False
    if target.name not in ALLOWED_DELETE_NAMES:
        return False
    if target.is_symlink():
        return False
    return target.parent == root


def delete_workspace_artifacts(
    root: Path,
    *,
    dry_run: bool = False,
) -> list[tuple[Path, str]]:
    results: list[tuple[Path, str]] = []
    for name in sorted(ALLOWED_DELETE_NAMES):
        path = root / name
        if not path.exists():
            continue
        if not is_safe_workspace_child(root, path):
            results.append((path, "skipped (unsafe path)"))
            continue
        if dry_run:
            results.append((path, "would delete"))
        else:
            shutil.rmtree(path)
            results.append((path, "deleted"))
    return results


def confirm_action(prompt: str, *, assume_yes: bool = False) -> bool:
    if assume_yes:
        return True
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer in ("y", "yes")
