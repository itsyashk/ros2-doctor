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

### Install as a Claude Code plugin marketplace

Add this repository as a plugin marketplace:

```text
/plugin marketplace add itsyashk/ros2-doctor
```

Install the plugin:

```text
/plugin install ros2-doctor@ros2-doctor
```

Restart Claude Code after installation if prompted.

For local marketplace testing from a clone:

```text
/plugin marketplace add /path/to/ros2-doctor
/plugin install ros2-doctor@ros2-doctor
```

### Install as a local skill

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

## How It Works

After installation, Claude Code can use `ros2-doctor` when a prompt involves
ROS 2 debugging. The skill gives Claude a strict workflow:

1. Inspect the workspace before editing.
2. Identify the ROS 2 distro from the environment, Docker/devcontainer files,
   CI, setup scripts, logs, and package metadata.
3. Classify package types such as `ament_python`, `ament_cmake`, interface
   packages, launch-only packages, and robot description packages.
4. Route the problem to a focused playbook.
5. Produce a diagnosis with evidence, a minimal fix, and exact verification
   commands.

For larger or unclear workspaces, the skill can use
`scripts/ros2_workspace_scan.py`. The scanner is read-only, uses only the Python
standard library, does not require ROS 2 to be installed, and prints markdown
that can be pasted into a debug report.

The guiding rule is still simple: understand first, edit second, fix minimally,
and verify clearly.

## Repository layout

```text
.
|-- .claude/
|   `-- skills/
|       `-- ros2-doctor/
|-- .claude-plugin/
|   `-- marketplace.json
|-- plugins/
|   `-- ros2-doctor/
|       |-- .claude-plugin/
|       |   `-- plugin.json
|       `-- skills/
|           `-- ros2-doctor/
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
- `.claude-plugin/marketplace.json` makes this repo installable as a Claude Code plugin marketplace.
- `plugins/ros2-doctor/` contains the marketplace plugin package.
- `SOURCES.md` preserves source attribution.
- `CLAUDE.md` contains repository maintenance notes for Claude Code agents.

## License

MIT. See [LICENSE](LICENSE).
