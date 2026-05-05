# Playbook: Workspace sourcing errors

## When to use
Use when built packages are not visible, wrong package versions are used, overlays/underlays behave unexpectedly, or shell environment variables point at the wrong ROS installation.

## Error signatures
- `Package '<pkg>' not found`
- `ros2: command not found`
- `PackageNotFoundError`
- `Could not find a package configuration file provided by '<dep>'`
- Running old code after rebuilding.
- `CMAKE_PREFIX_PATH` or `AMENT_PREFIX_PATH` references an unexpected workspace.

## Common causes
- New terminal did not source `/opt/ros/<distro>/setup.bash`.
- Overlay was built but `install/setup.bash` was not sourced.
- Overlay was built without sourcing the underlay it depends on.
- Sourcing order is reversed.
- Building and sourcing in the same terminal hides dependency problems.
- Overriding an underlay package without rebuilding dependents. This is pattern-based; inspect workspace chain before changing code.

## Files to inspect
- `install/setup.bash`
- `install/local_setup.bash`
- `.bashrc`, `.zshrc`, shell setup snippets
- Dockerfile/devcontainer/CI setup scripts
- `.repos`
- `log/latest_build/*/command.log`

## Diagnosis workflow
1. Print ROS environment: `env | sort | rg 'ROS_|AMENT|COLCON|CMAKE_PREFIX|PYTHONPATH|LD_LIBRARY_PATH'`.
2. Confirm package prefix: `ros2 pkg prefix <pkg>`.
3. Confirm executable source: `which ros2` and `ros2 pkg executables <pkg>`.
4. Check sourced order in `AMENT_PREFIX_PATH`: `python3 - <<'PY'\nimport os\nprint('\\n'.join(os.environ.get('AMENT_PREFIX_PATH','').split(':')))\nPY`
5. In a fresh terminal, source only the intended chain:
   - `source /opt/ros/<distro>/setup.bash`
   - `source <workspace>/install/setup.bash`
6. Rebuild overlays after sourcing underlays: `colcon build --packages-select <pkg>`.

## Minimal fix patterns
- For a single ROS install: `source /opt/ros/<distro>/setup.bash`.
- For an overlay: source underlay first, build overlay, then source only overlay `install/setup.bash` in new terminals.
- Use `install/local_setup.bash` only when intentionally avoiding automatic underlay sourcing.
- Remove stale auto-source lines from shell startup files only after showing they point to the wrong distro or workspace.
- Warning before destructive commands: environment fixes rarely require deleting `build/`, `install/`, or `log`; delete only package-scoped artifacts when stale installed files are proven.

## Verification commands
- `echo "$ROS_DISTRO"`
- `ros2 pkg prefix <pkg>`
- `ros2 run <pkg> <executable>`
- `colcon list`
- `colcon build --packages-select <pkg>`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Never mix sourced setup files from different ROS 2 distros in one shell unless diagnosing that mismatch deliberately.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- https://colcon.readthedocs.io/en/released/user/using-multiple-workspaces.html
- https://colcon.readthedocs.io/en/released/user/overriding-packages.html
- https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html
