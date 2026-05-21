from __future__ import annotations

from pathlib import Path

from ros2_doctor.scan._scanner import (
    Package,
    collect_packages,
    iter_package_xmls,
    parse_package_xml,
)

__all__ = [
    "Package",
    "collect_packages",
    "parse_package_xml",
    "iter_package_xmls",
    "list_package_names",
]


def list_package_names(root: Path) -> list[str]:
    packages, _ = collect_packages(root)
    return [p.name for p in packages]
