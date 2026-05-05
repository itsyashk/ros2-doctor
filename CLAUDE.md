# ros2-doctor Repository Notes

This repository packages a Claude Code skill. Keep the executable surface small:
the scanner should remain read-only, standard-library-only, and usable without a
ROS 2 installation.

When editing skill content, prefer source-backed playbook updates over broad
rewrites, preserve the documented playbook section structure, and keep
community/forum material paraphrased with attribution in `SOURCES.md`.

The skill exists in two install layouts:

- `.claude/skills/ros2-doctor/` for direct local skill installation.
- `plugins/ros2-doctor/skills/ros2-doctor/` for Claude Code plugin marketplace installation.

When changing skill files, keep both copies synchronized before committing.
