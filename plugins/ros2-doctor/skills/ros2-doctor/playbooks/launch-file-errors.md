# Playbook: Launch file errors

## When to use
Use when `ros2 launch` cannot find a launch file, launch imports fail, nodes do not start from launch, parameters are not found, or included launch files cannot be resolved.

## Error signatures
- `file '<file>.launch.py' was not found in the share directory of package '<pkg>'`
- `PackageNotFoundError: "<pkg>"`
- `ModuleNotFoundError: No module named 'launch'`
- `executable '<node>' not found on the libexec directory`
- `SubstitutionFailure`
- `No such file or directory: ... .yaml`

## Common causes
- Launch files not installed to `share/<pkg>/launch`.
- Config/RViz/URDF files referenced from source paths instead of installed share paths.
- Python package named `launch` shadows ROS 2 `launch`.
- Node executable name differs from `console_scripts` or CMake target install name.
- Overlay not sourced after build.
- Pattern-based community fix: missing `data_files` glob is common; verify installed layout before editing.

## Files to inspect
- `launch/*.launch.py`, `launch/*.launch.xml`, `launch/*.launch.yaml`
- `setup.py` or `CMakeLists.txt`
- `setup.cfg`
- `config/*.yaml`
- `rviz/*.rviz`
- `urdf/`, `description/`
- `install/<pkg>/share/<pkg>/`

## Diagnosis workflow
1. Confirm launch package discovery: `source install/setup.bash && ros2 pkg prefix <pkg>`.
2. Inspect installed files: `find install/<pkg>/share/<pkg> -maxdepth 3 -type f`.
3. Show launch arguments: `ros2 launch <pkg> <file.launch.py> --show-args`.
4. Trace imports: `python3 -c "import launch; print(launch.__file__)"`.
5. Check executable install: `ros2 pkg executables <pkg>` and `find install/<pkg>/lib/<pkg> -maxdepth 1 -type f -executable`.
6. Run with debug logs if needed: `ros2 launch <pkg> <file.launch.py> --debug`.

## Minimal fix patterns
- `ament_python`: add launch files to `setup.py` `data_files` under `share/<pkg>/launch`.
- `ament_cmake`: add `install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})` before `ament_package()`.
- Resolve package-relative resources with `get_package_share_directory('<pkg>')`.
- Rename a local Python package or file named `launch` if it shadows ROS 2 launch.
- Align launch `Node(executable='<name>')` with `console_scripts` or installed CMake target.
- Warning before destructive commands: do not remove generated directories just because launch cannot find a file; inspect `install/<pkg>/share/<pkg>` first.

## Verification commands
- `colcon build --packages-select <pkg> --symlink-install`
- `source install/setup.bash`
- `ros2 launch <pkg> <file.launch.py> --show-args`
- `ros2 launch <pkg> <file.launch.py>`
- `ros2 node list`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Launch APIs and examples differ slightly across distros; prefer the docs matching `$ROS_DISTRO` when checking substitutions and included launch descriptions.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html
- https://docs.ros.org/en/humble/How-To-Guides/Launch-file-different-formats.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-system.html
- https://robotics.stackexchange.com/questions/25013/ros2-launch-file-was-not-found-in-the-share-directory
