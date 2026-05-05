# Rolling Checklist

Rolling is a development distribution. Verify current official docs and
REP-2000 before making platform assumptions.

- Check `echo "$ROS_DISTRO"` is `rolling`.
- Confirm the workspace intentionally targets Rolling, not a stable distro.
- Expect package versions and APIs to move faster than Humble, Jazzy, or Kilted.
- Prefer source-backed checks over forum advice.
- If a fix depends on distro behavior, state that Rolling may change.

Commands:

```bash
source /opt/ros/rolling/setup.bash
rosdep check --from-paths src --ignore-src --rosdistro rolling
colcon build --symlink-install
```
