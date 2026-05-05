# ros2-doctor

`ros2-doctor` is a Claude Code skill for debugging ROS 2 workspaces with a
deliberate, evidence-first workflow.

It helps Claude Code inspect a workspace, identify the ROS 2 distro and package
types, classify the error, choose a focused playbook, and recommend the smallest
safe fix with clear verification commands.

The repository is intentionally markdown-first. The only executable helper is an
optional Python workspace scanner that prints a deterministic markdown report and
does not modify files.

## Status

Initial v0.1 skill content. It focuses on practical diagnosis rather than
automated repair.

## What It Helps With

Use this skill for workspaces involving:

- Python packages using `ament_python`
- C++ packages using `ament_cmake`
- launch files
- custom messages, services, and actions
- URDF, xacro, mesh, and RViz assets
- colcon build and runtime logs
- workspace sourcing, overlays, underlays, and node discovery
- dependency and distro mismatch problems
- TF frame, timestamp, and `use_sim_time` issues

The skill should favor inspection and diagnosis over broad rewrites. It should
explain what it checked, what looks suspicious, and how to verify a fix.

## Installation

Clone this repository:

```bash
git clone https://github.com/itsyashk/ros2-doctor.git
```

Then copy or symlink the skill directory into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/ros2-doctor/.claude/skills/ros2-doctor ~/.claude/skills/ros2-doctor
```

If you prefer copying:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/ros2-doctor/.claude/skills/ros2-doctor ~/.claude/skills/
```

After installation, restart Claude Code or reload skills according to your local
Claude Code workflow.

## Philosophy

```text
Understand first. Edit second. Fix minimally. Verify clearly.
```

The skill is designed to avoid common debugging traps: guessing the distro,
deleting build artifacts too early, changing package names casually, or copying
forum fixes into a different workspace without checking the evidence.

## Repository layout

```text
.
|-- .claude/
|   `-- skills/
|       `-- ros2-doctor/
|           |-- SKILL.md
|           |-- checklists/
|           |-- playbooks/
|           |-- references/
|           |-- templates/
|           `-- scripts/
|-- CLAUDE.md
|-- LICENSE
|-- MOTIVATION.md
|-- README.md
`-- SOURCES.md
```

- `SKILL.md` is the concise Claude skill entrypoint.
- `playbooks/` contains focused diagnostic guides.
- `checklists/` contains first-pass and distro-specific checks.
- `templates/` contains report and fix-plan formats.
- `references/` contains source-backed background notes.
- `scripts/ros2_workspace_scan.py` prints a read-only markdown workspace scan.
- `SOURCES.md` preserves source attribution.
- `CLAUDE.md` contains repository maintenance notes for Claude Code agents.

## License

MIT. See [LICENSE](LICENSE).
