# Jazzy Checklist

Assume Ubuntu 24.04 Noble unless evidence says otherwise.

- Check `echo "$ROS_DISTRO"` is `jazzy`.
- Confirm apt package names use `ros-jazzy-*`.
- Verify Python package metadata and entry points carefully; packaging behavior is stricter than many old tutorials imply.
- Check launch files use ROS 2 launch APIs supported by Jazzy.
- If a package was written for Humble, inspect distro-specific dependency names and APIs before editing.

Commands:

```bash
source /opt/ros/jazzy/setup.bash
ros2 doctor --report
colcon build --symlink-install
```
