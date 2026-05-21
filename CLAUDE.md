# ros2-doctor Repository Notes

This repository ships:

1. **`ros2-doctor` CLI** — installable Python package (`src/ros2_doctor/`).
2. **Claude Code skill** — canonical copy at `.claude/skills/ros2-doctor/`.

## Skill maintenance

- **Canonical source:** `.claude/skills/ros2-doctor/` only. Edit playbooks, checklists, and templates there.
- **Marketplace bundle:** `plugins/ros2-doctor/skills/` is generated at release time via `scripts/sync_plugin_skills.sh` (or `.ps1`). Do not edit the plugin copy directly.
- Keep community/forum material paraphrased with attribution in `SOURCES.md`.
- Prefer source-backed playbook updates over broad rewrites; preserve playbook section structure.

## Scanner / scan module

- Workspace file inspection lives in `src/ros2_doctor/scan/` (stdlib-only, no ROS 2 required).
- `.claude/skills/ros2-doctor/scripts/ros2_workspace_scan.py` is a thin wrapper for agents without pip install.

## CLI maintenance

- Destructive commands require confirmation; never delete outside the detected workspace root.
- Match existing naming and module layout when adding commands or checks.
