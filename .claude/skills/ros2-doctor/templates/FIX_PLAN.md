# ROS 2 Fix Plan

## Problem

- Failing command:
- Error signature:
- Expected behavior:

## Scope

- Package:
- Files to edit:
- Files to inspect only:

## Evidence

- Distro evidence:
- Package type:
- Relevant source-backed rule:

## Minimal Change

- Proposed edit:
- Why this is smaller than alternatives:

## Verification

```bash
source /opt/ros/<distro>/setup.bash
colcon build --symlink-install --packages-select <package_name>
source install/setup.bash
<run command>
```

## Rollback Notes

- How to undo this specific edit:
- Generated artifacts touched:
