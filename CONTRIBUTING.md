# Contributing to ros2-doctor

Thank you for helping improve ros2-doctor.

## Development setup

```bash
git clone https://github.com/itsyashk/ros2-doctor.git
cd ros2-doctor
pip install -e ".[dev]"
pytest
```

## Where to edit

| Area | Location |
|------|----------|
| CLI commands | `src/ros2_doctor/commands/` |
| Doctor checks | `src/ros2_doctor/checks/` |
| Workspace scanner (stdlib) | `src/ros2_doctor/scan/` |
| Error patterns | `src/ros2_doctor/diagnostics/data/error_patterns.toml` |
| Claude skill (canonical) | `.claude/skills/ros2-doctor/` only |

Do **not** edit `plugins/ros2-doctor/skills/` directly. Run `scripts/sync_plugin_skills.sh` before marketplace releases.

## Pull requests

- Keep changes focused; match existing style
- Add tests for new behavior in `tests/`
- Run `pytest` and `ruff check src tests`
- Update `CHANGELOG.md` for user-visible changes

## Playbooks

When adding error patterns, prefer entries derived from playbooks in `.claude/skills/ros2-doctor/playbooks/` and cite sources in `SOURCES.md` for community-derived patterns.
