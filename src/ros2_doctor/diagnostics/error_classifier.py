from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass
class ErrorMatch:
    id: str
    category: str
    playbook: str
    cause: str
    fix_command: str
    matched_text: str
    confidence: float


def _load_patterns() -> list[dict]:
    data_path = Path(__file__).parent / "data" / "error_patterns.toml"
    with data_path.open("rb") as f:
        data = tomllib.load(f)
    return data.get("pattern", [])


def classify_error(text: str, *, distro: str = "") -> list[ErrorMatch]:
    patterns = _load_patterns()
    matches: list[ErrorMatch] = []
    for entry in patterns:
        regex = entry.get("regex", "")
        if not regex:
            continue
        try:
            pat = re.compile(regex, re.IGNORECASE | re.MULTILINE)
        except re.error:
            continue
        m = pat.search(text)
        if not m:
            continue
        groups = m.groupdict()
        fix = entry.get("fix_template", "")
        for key, val in groups.items():
            fix = fix.replace("{" + key + "}", val)
        fix = fix.replace("$ROS_DISTRO", distro or "humble")
        matches.append(
            ErrorMatch(
                id=entry.get("id", "unknown"),
                category=entry.get("category", "general"),
                playbook=entry.get("playbook", ""),
                cause=entry.get("cause", ""),
                fix_command=fix,
                matched_text=m.group(0)[:200],
                confidence=0.9,
            )
        )
    matches.sort(key=lambda x: x.confidence, reverse=True)
    return matches
