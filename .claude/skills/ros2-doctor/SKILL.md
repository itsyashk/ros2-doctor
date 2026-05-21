---
name: ros2-doctor
description: Use this skill when debugging ROS 2 workspaces, including colcon build errors, package.xml/CMakeLists/setup.py issues, launch files, node discovery, topics, TF, URDF, RViz, dependency errors, workspace sourcing, distro mismatch, and message/service/action generation problems.
---

# ros2-doctor

## Philosophy

Understand first. Edit second. Fix minimally. Verify clearly.

Prefer workspace evidence over generic ROS advice. Treat prototype workspaces as
normal: inspect before editing, preserve user changes, and make the narrowest
repair that can be verified.

## Strict Workflow

1. Inspect workspace structure before editing.
2. Identify `ROS_DISTRO` using environment, Dockerfile, README, devcontainer, CI files, setup scripts, paths in logs, and package metadata.
3. Identify package types: `ament_python`, `ament_cmake`, mixed `ament_cmake_python`, interface package, launch-only package, robot description package.
4. Read relevant files before proposing fixes.
5. Classify the error into a playbook.
6. Produce a diagnosis with evidence.
7. Suggest the smallest safe fix.
8. Give exact rebuild, source, run, and verification commands.
9. Avoid broad refactors unless explicitly requested.
10. Leave a debug trail using the `templates/DEBUG_REPORT.md` template.

## Distro Detection Process

Collect distro evidence before choosing commands:

- Active shell: `echo $ROS_DISTRO`, `printenv | grep -E 'ROS|AMENT|COLCON'`.
- Files: Dockerfile, `.devcontainer`, README, CI, setup scripts, `.repos`, logs.
- Paths: `/opt/ros/<distro>`, `install/setup.*`, and package-manager names.
- Platform: OS release versus REP-2000 distro pairings.

If distro evidence conflicts, state the conflict and use the command
environment as the practical default. If no distro is detectable, say:
`Assumption: Humble is used as a practical default until evidence says otherwise.`

## Package Type Detection Process

Classify the relevant package before editing:

- `ament_python`: `package.xml` exports `ament_python`, with `setup.py`, `setup.cfg`, `resource/<pkg>`, and a Python module.
- `ament_cmake`: `package.xml` exports `ament_cmake`, with `CMakeLists.txt` and `ament_package()`.
- Mixed `ament_cmake_python`: CMake package that intentionally installs Python modules.
- Interface package: contains `msg/`, `srv/`, or `action/` and `rosidl_generate_interfaces()`.
- Launch-only package: mostly `launch/`, `config/`, resources, and install rules.
- Robot description package: URDF/xacro/mesh/RViz files, often with `robot_state_publisher`.

For mixed signals, inspect install rules, entry points, and `package.xml`
before deciding whether the failure is packaging, dependency, or runtime related.

## Resource Routing

Keep detailed procedures in supporting files. Load only the most relevant resource:

- `playbooks/colcon-build-errors.md`: build failures and colcon workflow.
- `playbooks/python-package-errors.md`: `ament_python`, entry points, resource markers.
- `playbooks/cpp-package-errors.md`: `ament_cmake`, targets, install rules.
- `playbooks/launch-file-errors.md`: launch syntax, installed launch files, executable lookup.
- `playbooks/workspace-sourcing-errors.md`: overlays, underlays, package discovery.
- `playbooks/distro-mismatch-errors.md`: OS/distro/branch mismatch and legacy packages.
- `playbooks/tf-errors.md`: TF frames, timestamps, extrapolation, `use_sim_time`.
- `playbooks/urdf-rviz-errors.md`: URDF, xacro, meshes, RViz fixed frame.
- `playbooks/message-service-action-errors.md`: `msg/`, `srv/`, `action`, rosidl generation.
- `playbooks/dependency-errors.md`: rosdep, missing packages, Python environments.
- `checklists/first-pass-triage.md`: initial scan before choosing a playbook.
- `references/`: source-backed background notes.

## When To Use the CLI or Scanner

Prefer the **`ros2-doctor` CLI** when installed (`pip install ros2-doctor`):

- `ros2-doctor doctor` — full diagnostic checks
- `ros2-doctor report -o DEBUG_REPORT.md` — markdown report
- `ros2-doctor explain-error --file log.txt` — classify errors without an LLM

Fallback: `scripts/ros2_workspace_scan.py` from the workspace root (read-only,
stdlib-only, no ROS 2 required). Use when the CLI is not installed.

Treat scanner/CLI output as evidence, not authority.

## Output Format

For substantive debugging responses, use:

1. Distro Assessment
2. Workspace Map
3. Error Classification
4. Likely Root Cause
5. Evidence
6. Minimal Fix
7. Verification Commands
8. Risk Notes
9. Debug Report

## Safety Rules

- Own only files needed for the requested fix; never revert unrelated edits.
- Read `package.xml` and relevant build/install files before editing.
- Do not recommend deleting `build/`, `install/`, or `log/` first unless evidence points to stale artifacts.
- Warn before destructive commands.
- Avoid changing package names, node names, topic names, frame IDs, or public interfaces without explaining impact.
- Prefer additive dependency, install, and launch fixes over restructuring.
- Prefer official docs over forum advice; mark community-derived fixes as pattern-based when uncertain.
- If hardware, simulators, sensors, or robots are involved, avoid commands that actuate motion unless the user confirms the environment is safe.
