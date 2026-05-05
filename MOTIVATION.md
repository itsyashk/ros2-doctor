# Motivation

ROS 2 is powerful, but debugging ROS 2 workspaces can be painfully confusing.

A simple issue can hide across many layers: `package.xml`, `CMakeLists.txt`, `setup.py`, launch files, sourced environments, missing dependencies, topic names, TF frames, URDF paths, RViz configs, and runtime logs. For beginners, researchers, and robotics teams, this often turns into hours of guessing, rebuilding, re-sourcing, and searching through scattered forum posts.

`ros2-doctor` exists to make that process more systematic.

The goal of this skill is to help Claude Code act like a careful ROS 2 debugging assistant. Instead of randomly editing files or giving generic advice, it should first inspect the workspace, understand the package structure, identify the ROS 2 build system being used, read the relevant configuration files, and then produce a clear diagnosis with the smallest safe fix.

This skill is especially designed for people working in robotics research, student projects, labs, hackathons, and early-stage prototypes, where codebases are often messy, documentation is incomplete, and the fastest path to progress is understanding what is actually broken.

`ros2-doctor` should help with problems like:

- `colcon build` errors
- missing dependencies
- broken Python ROS 2 packages
- broken C++ ROS 2 packages
- launch file issues
- node discovery problems
- topic publishing and subscribing bugs
- TF tree errors
- URDF, xacro, mesh, and RViz visualization issues
- workspace sourcing problems
- message, service, and action generation errors
- confusing runtime logs

The philosophy is simple:

```text
Understand first. Edit second. Fix minimally. Verify clearly.
```

That philosophy matters because robotics debugging is rarely about a single
file. A broken demo can involve package metadata, generated interfaces, launch
arguments, sourced overlays, environment variables, stale build artifacts, and a
runtime graph that only exists after nodes are running.

`ros2-doctor` should help make those layers visible. It should encourage Claude
Code to gather evidence, state uncertainty plainly, and avoid changing code
until the likely cause is understood.

The long-term aim is not to replace ROS 2 expertise. It is to make that
expertise easier to apply in real workspaces, especially when someone is tired,
under deadline, or staring at an error message that hides the useful clue three
directories away.
