from __future__ import annotations

from ros2_doctor.diagnostics.error_classifier import classify_error


def analyze_launch_output(stdout: str, stderr: str, *, distro: str = "") -> list:
    combined = stdout + "\n" + stderr
    return classify_error(combined, distro=distro)
