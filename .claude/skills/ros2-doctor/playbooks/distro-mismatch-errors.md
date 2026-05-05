# Playbook: Distro mismatch errors

## When to use
Use when errors suggest the workspace, OS, Python version, apt packages, branch names, or sourced setup files belong to different ROS 2 distributions.

## Error signatures
- `Unable to locate package ros-<distro>-<pkg>`
- `ModuleNotFoundError: No module named 'rclpy'`
- Missing generated type support after switching branches.
- `Could not find ...Config.cmake` for a package expected in another distro.
- Python ABI/import errors after changing ROS distro or virtualenv.
- Code uses launch, QoS, or message APIs not available in the active distro.

## Common causes
- Wrong `/opt/ros/<distro>/setup.bash` sourced.
- Git branch targets a different ROS distro than the environment.
- OS release is unsupported or Tier 3 for the selected distro.
- apt package name exists in one distro but not another.
- Python virtualenv uses a Python version outside the distro platform matrix.
- ROS 1 package or branch used in a ROS 2 workspace.

## Files to inspect
- `.repos`
- `README.md`, install docs, scripts
- Dockerfile/devcontainer
- CI workflow files
- `package.xml`
- `requirements.txt`, `pyproject.toml`, virtualenv activation scripts
- `/etc/os-release`

## Diagnosis workflow
1. Check active distro: `echo "$ROS_DISTRO"` and `which ros2`.
2. Check OS: `. /etc/os-release && echo "$PRETTY_NAME"`.
3. Check Python: `python3 --version` and `python3 -c "import sys; print(sys.executable)"`.
4. Search branch clues: `rg -n 'humble|iron|jazzy|kilted|rolling|foxy|galactic|noetic' README.md .github Dockerfile .devcontainer .repos src 2>/dev/null`.
5. Check apt package availability: `apt-cache policy ros-<distro>-<pkg-with-dashes>`.
6. Compare with REP 2000 and the selected docs version.

## Minimal fix patterns
- Source the matching distro: `source /opt/ros/<distro>/setup.bash`.
- Check out the branch matching the active distro.
- Use the OS targeted by the distro, or build from source with the risk called out.
- Use a fresh shell without virtualenv if ROS Python modules vanish.
- For ROS 1 branches, switch to the ROS 2 branch or stop and ask before porting.
- Warning before destructive commands: when switching distros, do not delete artifacts first; confirm mismatch, then use package-scoped cleanup if old generated files still load.

## Verification commands
- `echo "$ROS_DISTRO"`
- `ros2 doctor --report`
- `ros2 pkg prefix <pkg>`
- `colcon build --packages-select <pkg>`
- `python3 -c "import rclpy; print(rclpy.__file__)"`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Humble targets Ubuntu Jammy and has support through May 2027; Jazzy targets Ubuntu Noble and has support through May 2029. Always verify current target platforms in REP 2000.

## Sources used
- https://www.ros.org/reps/rep-2000.html
- https://docs.ros.org/en/humble/
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
