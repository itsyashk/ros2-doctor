# Humble Checklist

Assume Ubuntu 22.04 Jammy unless evidence says otherwise.

- Check `echo "$ROS_DISTRO"` is `humble`.
- Check source order: `/opt/ros/humble/setup.bash` before workspace `install/setup.bash`.
- Watch for Python 3.10 environment conflicts from conda, pyenv, or `/usr/local`.
- Confirm apt package names use `ros-humble-*`.
- If using older tutorials, verify APIs against Humble docs.
- For generated interfaces, verify `rosidl_default_generators`, `rosidl_default_runtime`, and `rosidl_interface_packages`.

Commands:

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```
