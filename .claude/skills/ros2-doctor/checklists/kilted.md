# Kilted Checklist

Assume Ubuntu 24.04 Noble unless evidence says otherwise.

- Check `echo "$ROS_DISTRO"` is `kilted`.
- Confirm apt package names use `ros-kilted-*`.
- Prefer Kilted docs for current behavior, but cross-check REP-2000 for platform support.
- Treat Rolling-only package behavior as unstable unless the workspace explicitly targets Rolling.
- Verify dependencies exist for Kilted before assuming a missing package should be installed by apt.

Commands:

```bash
source /opt/ros/kilted/setup.bash
rosdep check --from-paths src --ignore-src --rosdistro kilted
colcon build --symlink-install
```
