# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-05-20

### Added

- Installable `ros2-doctor` CLI (Python 3.10+, Typer + Rich)
- Commands: `doctor`, `env`, `deps`, `build`, `clean`, `report`, `topics`, `nodes`, `tf`, `bag`, `launch-debug`, `explain-error`
- Doctor check registry (system, ROS install, overlay, workspace, tooling, deps, graph)
- Stdlib workspace scanner in `ros2_doctor.scan`
- Rule-based `explain-error` classifier from playbook signatures
- colcon log parser and build failure summaries
- Safe workspace clean with `--dry-run` and `--yes`
- Markdown report generator
- pytest suite and GitHub Actions CI
- Single canonical Claude skill at `.claude/skills/ros2-doctor/` with release sync script

### Changed

- Removed duplicated committed plugin skill tree; marketplace bundle generated at release time
