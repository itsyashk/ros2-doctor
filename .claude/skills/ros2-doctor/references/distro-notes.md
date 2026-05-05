# Distro Notes

Use official release pages and REP-2000 as the source of truth when this file is
stale.

## Supported Scope

- Humble Hawksbill: Ubuntu 22.04 Jammy is the common Tier 1 Linux pairing.
- Jazzy Jalisco: Ubuntu 24.04 Noble is the common Tier 1 Linux pairing.
- Kilted Kaiju: Ubuntu 24.04 Noble is the common Tier 1 Linux pairing.
- Rolling Ridley: rolling development distribution; target platforms can change.

## Practical Detection

Check:

```bash
echo "$ROS_DISTRO"
lsb_release -a
printenv | grep -E 'ROS|AMENT|COLCON'
```

Then inspect:

- Dockerfile and `.devcontainer/`
- CI workflows
- README/setup scripts
- `/opt/ros/<distro>` paths in logs
- apt package names such as `ros-humble-*` or `ros-jazzy-*`

## Mismatch Signals

- `rospy`, `roscpp`, `catkin`, or `rostime` in a ROS 2 `rosdep` failure.
- Ubuntu version does not match the distro's expected platform.
- Package branch or Docker image names mention a different distro than the shell.
- `source /opt/ros/<distro>/setup.bash` differs from dependency package names.

If unclear, say: `Assumption: Humble is used as a practical default until evidence says otherwise.`
