# Colcon Basics

Use this reference for build, sourcing, and workspace layout problems.

## Workspace Layout

A typical ROS 2 workspace root contains `src/`. After a build it usually also
contains `build/`, `install/`, and `log/`.

Build from the workspace root:

```bash
colcon build --symlink-install
```

Source the underlay first, then the overlay:

```bash
source /opt/ros/<distro>/setup.bash
source install/setup.bash
```

## Diagnosis Checks

- Was `colcon build` run from the workspace root, not from `src/`?
- Does the active shell show the intended `ROS_DISTRO`?
- Does `CMAKE_PREFIX_PATH` or `AMENT_PREFIX_PATH` include the intended underlay?
- Does `ros2 pkg prefix <package>` point into the expected workspace?
- Are launch/config files installed or symlinked into `install/share/<package>`?

## Clean Build Caution

Do not start by deleting `build/`, `install/`, and `log/`. First inspect whether
the problem is stale generated content. If cleaning is justified, warn the user:

```bash
# Destructive: removes generated build artifacts for this workspace.
rm -rf build install log
```
