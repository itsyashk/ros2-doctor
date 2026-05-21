from __future__ import annotations

from pathlib import Path

from ros2_doctor.diagnostics.error_classifier import classify_error


def find_latest_build_log(workspace: Path) -> Path | None:
    log_dir = workspace / "log"
    latest = log_dir / "latest_build"
    if latest.exists():
        return latest
    if not log_dir.is_dir():
        return None
    builds = sorted(log_dir.glob("build_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    return builds[0] if builds else None


def find_failing_package(workspace: Path) -> tuple[str | None, str]:
    latest = find_latest_build_log(workspace)
    if not latest:
        return None, ""

    stderr_files = list(latest.rglob("stderr.log"))
    for stderr in sorted(stderr_files, key=lambda p: p.stat().st_mtime, reverse=True):
        text = stderr.read_text(encoding="utf-8", errors="replace")
        if text.strip():
            pkg = stderr.parent.name
            return pkg, text
    return None, ""


def summarize_build_failure(workspace: Path, *, distro: str = "") -> dict:
    pkg, log_text = find_failing_package(workspace)
    matches = classify_error(log_text, distro=distro) if log_text else []
    return {
        "package": pkg,
        "log_excerpt": log_text[:2000] if log_text else "",
        "matches": matches,
        "log_dir": str(find_latest_build_log(workspace) or ""),
    }
