from __future__ import annotations

from ros2_doctor.diagnostics.error_classifier import classify_error


def test_cmake_missing_dep():
    text = 'Could not find a package configuration file provided by "nav2_msgs"'
    matches = classify_error(text, distro="humble")
    assert matches
    assert matches[0].category == "build"
    assert "nav2_msgs" in matches[0].fix_command or "nav2_msgs" in matches[0].matched_text


def test_rosdep_key():
    text = "Cannot locate rosdep definition for [my_custom_key]"
    matches = classify_error(text)
    assert matches[0].category == "dependency"


def test_module_not_found():
    text = "ModuleNotFoundError: No module named 'rclpy'"
    matches = classify_error(text)
    assert any(m.category == "python" for m in matches)
