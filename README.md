# ros2-doctor

Friendly ROS 2 developer diagnostics for workspaces, builds, dependencies, topics, nodes, and TF.

```text
██████╗  ██████╗ ███████╗██████╗       ██████╗  ██████╗  ██████╗████████╗ ██████╗ ██████╗
██╔══██╗██╔═══██╗██╔════╝██╔══██╗      ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║   ██║███████╗██║  ██║█████╗██║  ██║██║   ██║██║        ██║   ██║   ██║██████╔╝
██╔══██╗██║   ██║╚════██║██║  ██║╚════╝██║  ██║██║   ██║██║        ██║   ██║   ██║██╔══██╗
██║  ██║╚██████╔╝███████║██████╔╝      ██████╔╝╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝       ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

**Understand first. Edit second. Fix minimally. Verify clearly.**

## Install

```bash
pip install ros2-doctor
```

From a clone:

```bash
git clone https://github.com/itsyashk/ros2-doctor.git
cd ros2-doctor
pip install -e .
```

Requires Python 3.10+.

## Quickstart

From your ROS 2 workspace root:

```bash
source /opt/ros/humble/setup.bash   # or your distro
ros2-doctor doctor                  # full diagnostic pass
ros2-doctor env                     # ROS environment report
ros2-doctor deps                    # rosdep check (dry-run by default)
ros2-doctor build                   # colcon build --symlink-install + error summary
source install/setup.bash
ros2-doctor topics
ros2-doctor report -o debug-report.md
```

## Commands

| Command | Description |
|---------|-------------|
| `doctor` | Full workspace and environment checks |
| `env` | ROS env vars, overlay chain, warnings |
| `deps` | rosdep / package.xml dependency check |
| `build` | colcon wrapper with readable failure summary |
| `clean` | Remove `build/`, `install/`, `log/` (with confirmation) |
| `report` | Markdown diagnostic report (`-o file.md`) |
| `topics` | Cleaner topic list; `--expect /cmd_vel,...` |
| `nodes` | Active nodes; `--info /my_node` |
| `tf` | `/tf`, `/tf_static`, frame tree hints |
| `bag` | Inspect or record rosbag2 (with confirmation) |
| `launch-debug` | Run `ros2 launch` and classify errors |
| `explain-error` | Classify pasted or log errors (no LLM) |

Global options: `--workspace PATH`, `--no-banner`, `--dry-run` (where supported), `--version`.

## Safety

- Read-only by default for inspection commands
- `clean` and `deps --install` ask for confirmation (use `--yes` to skip)
- Never deletes outside the detected workspace root
- Does not modify shell dotfiles

## Optional workspace config

`.ros2-doctor.toml` in the workspace root:

```toml
[doctor]
expected_topics = ["/cmd_vel", "/scan"]

[bag]
default_topics = ["/tf", "/tf_static", "/rosout"]
max_duration_secs = 120
```

## Claude Code skill

This repo also ships a **Claude Code skill** (playbooks, checklists, templates) at [`.claude/skills/ros2-doctor/`](.claude/skills/ros2-doctor/).

- **Canonical skill source:** `.claude/skills/ros2-doctor/` only
- **Marketplace releases:** run `scripts/sync_plugin_skills.sh` to copy into `plugins/ros2-doctor/skills/` before publishing

Local skill install:

```bash
ln -s /path/to/ros2-doctor/.claude/skills/ros2-doctor ~/.claude/skills/ros2-doctor
```

Plugin marketplace:

```text
/plugin marketplace add itsyashk/ros2-doctor
/plugin install ros2-doctor@ros2-doctor
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
