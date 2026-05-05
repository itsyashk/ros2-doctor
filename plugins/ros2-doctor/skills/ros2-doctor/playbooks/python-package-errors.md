# Playbook: Python package errors

## When to use
Use for `ament_python` packages when imports, entry points, `ros2 run`, launch installation, or Python dependency resolution fails.

## Error signatures
- `No executable found`
- `Package '<pkg>' not found`
- `ModuleNotFoundError: No module named '<pkg_or_dep>'`
- `importlib.metadata.PackageNotFoundError`
- `not found: .../share/<pkg>/local_setup.bash`
- Launch file missing from `install/<pkg>/share/<pkg>`

## Common causes
- Missing `resource/<package_name>` marker or missing marker entry in `setup.py`.
- Missing `package.xml` install entry in `setup.py`.
- Missing `setup.cfg` script install paths, so `ros2 run` cannot find executables under `lib/<pkg>`.
- `console_scripts` target points to the wrong module or function.
- Local file or directory shadows an installed package.
- Python version conflict between ROS distro and active virtual environment. Pattern-based community fix: verify with local paths before changing environments.

## Files to inspect
- `package.xml`
- `setup.py`
- `setup.cfg`
- `resource/<pkg>`
- `<pkg>/__init__.py`
- `launch/`, `config/`, `test/`
- `install/<pkg>/lib/<pkg>/`
- `install/<pkg>/share/<pkg>/`

## Diagnosis workflow
1. Confirm package type: `rg '<build_type>ament_python</build_type>|setup.py|setup.cfg' <pkg-path>`.
2. Inspect entry points: `sed -n '1,220p' <pkg-path>/setup.py`.
3. Inspect script destination: `sed -n '1,120p' <pkg-path>/setup.cfg`.
4. Build directly: `colcon build --packages-select <pkg> --symlink-install --event-handlers console_direct+`.
5. Source and inspect installed layout: `source install/setup.bash && ros2 pkg prefix <pkg> && find install/<pkg> -maxdepth 4 -type f`.
6. Check Python import path: `python3 -c "import sys; print('\n'.join(sys.path))"`.

## Minimal fix patterns
- Add marker and manifest install:
  - `('share/ament_index/resource_index/packages', ['resource/' + package_name])`
  - `(os.path.join('share', package_name), ['package.xml'])`
- Add `setup.cfg`:
  - `[develop] script_dir=$base/lib/<pkg>`
  - `[install] install_scripts=$base/lib/<pkg>`
- Fix entry point shape: `'<cmd> = <python_package>.<module>:main'`.
- Install launch/config files through `data_files`, for example `(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))`.
- If a virtualenv hides ROS Python modules, test in a clean shell sourced only with `/opt/ros/<distro>/setup.bash` before editing package files.
- Warning before destructive commands: only remove package-scoped `build/<pkg>` or `install/<pkg>` after confirming an old entry point or old installed file is still being loaded.

## Verification commands
- `colcon build --packages-select <pkg> --symlink-install`
- `source install/setup.bash`
- `ros2 run <pkg> <cmd>`
- `python3 -c "import <python_package>; print(<python_package>.__file__)"`
- `ros2 launch <pkg> <file.launch.py>` if launch files changed

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Match the active Python version to the ROS distro platform matrix; distro or virtualenv conflicts often appear as missing `catkin_pkg`, `rclpy`, or generated type support modules.

## Sources used
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- https://www.ros.org/reps/rep-2000.html
