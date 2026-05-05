# Playbook: Colcon build errors

## When to use
Use when `colcon build` fails, builds the wrong packages, cannot discover packages, or reports CMake/Python packaging errors from a ROS 2 workspace.

## Error signatures
- `Summary: 0 packages finished`
- `Package '<pkg>' not found`
- `Could not find a package configuration file provided by '<dep>'`
- `ModuleNotFoundError: No module named '<module>'`
- `stderr.log` shows failure before package-specific compile or install steps

## Common causes
- Command run from `src/` instead of the workspace root.
- Underlay or overlay not sourced before building dependent packages.
- Missing or incorrect `package.xml`, `CMakeLists.txt`, `setup.py`, or `setup.cfg`.
- Wrong ROS distro environment for the checked-out branch.
- Stale artifacts after package rename, entry point rename, or generated interface changes. Treat this as evidence-based, not the first guess.

## Files to inspect
- `package.xml`
- `CMakeLists.txt`
- `setup.py`
- `setup.cfg`
- `log/latest_build/<pkg>/stdout_stderr.log`
- `log/latest_build/<pkg>/command.log`
- `.repos`, Dockerfile, devcontainer, CI, README setup notes

## Diagnosis workflow
1. Confirm workspace root: `pwd`, `test -d src && rg --files src -g package.xml`.
2. Confirm environment: `echo "$ROS_DISTRO"`, `env | rg 'AMENT|COLCON|CMAKE_PREFIX|PYTHONPATH|ROS_'`.
3. List packages: `colcon list --paths-only`.
4. Read the first failing package log: `sed -n '1,220p' log/latest_build/<pkg>/stdout_stderr.log`.
5. Build only the failing package with direct output: `colcon build --packages-select <pkg> --event-handlers console_direct+`.
6. If a dependency config is missing, check whether the dependency exists in `src/`, the underlay, or apt: `ros2 pkg prefix <dep>`.

## Minimal fix patterns
- Wrong directory: `cd <workspace-root>` before `colcon build`.
- Unsourced underlay: `source /opt/ros/<distro>/setup.bash`, then rebuild the overlay.
- Unsourced local overlay after successful build: `source install/setup.bash`.
- Missing dependency metadata: add the dependency to `package.xml` and the relevant `find_package()`, `ament_target_dependencies()`, or `install_requires` location.
- Stale artifact path only when logs prove a rename or old generated file is being loaded: warn first, then remove the specific package artifact, for example `rm -rf build/<pkg> install/<pkg> log/latest_build/<pkg>`.
- Warning before destructive commands: deleting `build/`, `install/`, or `log/` removes generated artifacts and logs; prefer package-scoped deletion and only after evidence points to stale artifacts.

## Verification commands
- `colcon build --packages-select <pkg> --event-handlers console_direct+`
- `source install/setup.bash`
- `ros2 pkg prefix <pkg>`
- `colcon test --packages-select <pkg>`
- `colcon test-result --all --verbose`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Check `.repos`, branch names, Docker base images, and `ROS_DISTRO`; mismatches commonly surface as missing package configs or Python modules.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
- https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html
- https://colcon.readthedocs.io/en/released/user/using-multiple-workspaces.html
