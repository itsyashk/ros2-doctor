from __future__ import annotations

from ros2_doctor.core.packages import collect_packages, parse_package_xml


def test_parse_package_xml(minimal_workspace):
    xml = minimal_workspace / "src" / "demo_pkg" / "package.xml"
    name, build_type = parse_package_xml(xml)
    assert name == "demo_pkg"
    assert build_type == "ament_python"


def test_collect_packages(minimal_workspace):
    packages, issues = collect_packages(minimal_workspace)
    assert len(packages) == 1
    assert packages[0].name == "demo_pkg"
