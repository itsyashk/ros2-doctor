# Playbook: TF errors

## When to use
Use for missing transforms, disconnected frame trees, extrapolation errors, RViz TF display errors, or inconsistent `use_sim_time` behavior.

## Error signatures
- `Lookup would require extrapolation into the future`
- `Lookup would require extrapolation into the past`
- `frame does not exist`
- `Could not transform from [a] to [b]`
- RViz: `Fixed Frame [map] does not exist`
- `TF_REPEATED_DATA`

## Common causes
- Transform broadcaster not running or publishing wrong frame IDs.
- Fixed frame is absent from the TF tree.
- `use_sim_time` differs across nodes.
- `/clock` missing while nodes use simulated time.
- Timestamp latency, low publish rate, or future-dated messages.
- Static transform published with reversed parent/child.

## Files to inspect
- Launch files that start broadcasters/listeners.
- Node code calling `sendTransform()` or `lookupTransform()`.
- Parameter YAML files containing `use_sim_time`.
- URDF/xacro frame names.
- RViz config fixed frame.

## Diagnosis workflow
1. List frames: `ros2 run tf2_tools view_frames`.
2. Echo the failing transform: `ros2 run tf2_ros tf2_echo <target_frame> <source_frame>`.
3. Monitor timing: `ros2 run tf2_ros tf2_monitor <target_frame> <source_frame>`.
4. Check clock: `ros2 topic echo /clock --once` and `ros2 param get <node> use_sim_time`.
5. Check active broadcasters: `ros2 topic info /tf -v` and `ros2 topic info /tf_static -v`.
6. Compare frame IDs in code, URDF, and launch parameters exactly; frame IDs are case-sensitive.

## Minimal fix patterns
- Start or respawn the missing broadcaster.
- Set consistent `use_sim_time` on all relevant nodes when running simulation.
- Use `tf2::TimePointZero` or equivalent only when latest transform is acceptable.
- Increase broadcaster rate or correct message timestamps when extrapolation is caused by timing.
- Fix parent/child order for static transforms.
- Update RViz fixed frame to an existing stable frame such as `map`, `odom`, or `world`.
- Warning before destructive commands: TF issues are runtime graph issues; do not delete build artifacts unless a code/package rename is proven stale.

## Verification commands
- `ros2 run tf2_tools view_frames`
- `ros2 run tf2_ros tf2_echo <target_frame> <source_frame>`
- `ros2 run tf2_ros tf2_monitor <target_frame> <source_frame>`
- `ros2 topic hz /tf`
- `ros2 param get <node> use_sim_time`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Use the TF2 debugging docs for the active distro; command names are stable, but tutorial package names and examples may differ.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html
