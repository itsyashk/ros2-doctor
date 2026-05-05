# Playbook: Dependency errors

## When to use
Use for missing apt/rosdep dependencies, unresolved rosdep keys, wrong dependency tags, missing CMake/Python dependencies, or dependency graph build-order failures.

## Error signatures
- `Cannot locate rosdep definition for [<key>]`
- `No definition of [<key>] for OS version`
- `Unable to locate package ros-<distro>-<pkg>`
- `Could not find a package configuration file provided by '<dep>'`
- `ModuleNotFoundError: No module named '<dep>'`
- Header or library not found during build.

## Common causes
- Dependency missing from `package.xml`.
- ROS package is unreleased in the active distro.
- Wrong rosdep key, often from a ROS 1 package name or wrong branch.
- Stale rosdep cache.
- Unsupported OS/distro combination.
- Dependency exists in the workspace but `--ignore-src` or sourcing assumptions hide it.
- Pattern-based community fix: unresolved keys often mean wrong branch or unreleased key; verify in rosdistro before editing names.

## Files to inspect
- `package.xml`
- `CMakeLists.txt`
- `setup.py`, `requirements.txt`, `pyproject.toml`
- `.repos`
- `rosdep` output
- Dockerfile/CI dependency install steps

## Diagnosis workflow
1. Confirm distro and OS: `echo "$ROS_DISTRO"` and `. /etc/os-release && echo "$ID $VERSION_CODENAME"`.
2. Check rosdep from workspace root: `rosdep check --from-paths src --ignore-src --rosdistro <distro>`.
3. Update cache if key availability is suspect: `rosdep update`.
4. Check a key: `rosdep resolve <key> --rosdistro <distro>`.
5. Check released package availability: `apt-cache policy ros-<distro>-<pkg-with-dashes>`.
6. Search dependency declarations: `rg '<dep>|find_package\\(<dep>|import <dep>' src`.

## Minimal fix patterns
- Add build and runtime dependency with the narrowest correct tags:
  - C++ mixed build/run: `<depend><dep></depend>`
  - Runtime-only Python import: `<exec_depend><dep></exec_depend>`
  - Header exported to dependents: include `<build_export_depend><dep></build_export_depend>`
- Add CMake `find_package(<dep> REQUIRED)` and `ament_target_dependencies(<target> <dep>)`.
- After confirming missing system packages, run `rosdep install --from-paths src --ignore-src --rosdistro <distro>` without `-y` so package-manager changes remain visible before acceptance.
- If a key is unreleased for the distro, use the source package in `src/`, switch branch, or document a custom rosdep rule instead of guessing a key.
- If rosdep cache is stale, run `rosdep update` before changing package files.
- Warning before destructive commands: dependency errors should be fixed in metadata, environment, or installed packages; do not delete build artifacts first.

## Verification commands
- `rosdep check --from-paths src --ignore-src --rosdistro <distro>`
- `rosdep install --from-paths src --ignore-src --rosdistro <distro>`
- `colcon build --packages-select <pkg>`
- `ros2 pkg prefix <dep>`
- `python3 -c "import <module>"`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Package availability is distro-specific; check rosdistro/apt for the active distro before renaming dependencies.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Rosdep.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
- https://docs.ros.org/en/humble/How-To-Guides/Ament-CMake-Documentation.html
- https://www.ros.org/reps/rep-2000.html
- https://stackoverflow.com/questions/24187277/ros-ptam-cannot-locate-rosdep-definition
