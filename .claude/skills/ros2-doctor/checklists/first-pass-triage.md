# First-Pass Triage

Use this checklist before editing.

- Capture the failing command and exact error signature.
- Identify the workspace root and confirm whether it has `src/`.
- Record distro evidence: `$ROS_DISTRO`, Docker/devcontainer, CI, README, logs.
- List packages and build types from `package.xml`, `setup.py`, and `CMakeLists.txt`.
- Inspect relevant launch files, package install rules, and generated interface folders.
- Check whether the active shell sourced the ROS underlay and workspace overlay.
- Classify into one playbook.
- State the smallest hypothesis and the command that would verify it.

Useful commands:

```bash
pwd
find src -name package.xml -maxdepth 4
echo "$ROS_DISTRO"
colcon list
ros2 pkg list | grep <package_name>
```
