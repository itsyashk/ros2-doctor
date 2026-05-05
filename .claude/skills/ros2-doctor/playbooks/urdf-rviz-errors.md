# Playbook: URDF RViz errors

## When to use
Use when robot model visualization, xacro expansion, mesh loading, `robot_state_publisher`, joint states, or RViz fixed frame/model display fails.

## Error signatures
- RViz RobotModel: `No transform from [link] to [fixed_frame]`
- RViz: `Fixed Frame [<frame>] does not exist`
- `Error document empty` or xacro parse errors.
- `package '<pkg>' not found` while resolving `package://` mesh paths.
- Mesh appears missing or robot appears at origin with broken links.
- `No robot_description parameter`

## Common causes
- `robot_state_publisher` not running or missing `robot_description`.
- Xacro file path resolved from source instead of installed share directory.
- Meshes, URDF, or RViz files not installed to `share/<pkg>`.
- Joint states missing for non-fixed joints.
- RViz fixed frame not in TF tree.
- URDF link/joint names do not match TF or joint state names.

## Files to inspect
- `urdf/*.urdf`, `urdf/*.xacro`, `description/`
- `meshes/`
- `launch/*.launch.py`
- `rviz/*.rviz`
- `setup.py` or `CMakeLists.txt`
- `install/<pkg>/share/<pkg>/`

## Diagnosis workflow
1. Validate xacro: `ros2 run xacro xacro <path/to/file.urdf.xacro> > /tmp/robot.urdf`.
2. Check `robot_description`: `ros2 param get /robot_state_publisher robot_description`.
3. Check TF tree: `ros2 run tf2_tools view_frames`.
4. Check joint states: `ros2 topic echo /joint_states --once`.
5. Inspect installed assets: `find install/<pkg>/share/<pkg> -maxdepth 4 -type f`.
6. Launch RViz after sourcing: `source install/setup.bash && ros2 run rviz2 rviz2`.

## Minimal fix patterns
- Use `get_package_share_directory('<pkg>')` to build URDF/xacro/config paths in launch files.
- Install assets:
  - CMake: `install(DIRECTORY launch urdf meshes rviz DESTINATION share/${PROJECT_NAME})`
  - Python: add `data_files` entries for `launch`, `urdf`, `meshes`, and `rviz`.
- Pass robot description to `robot_state_publisher` from processed xacro output.
- Start `joint_state_publisher` or the real joint state source for movable joints.
- Set RViz fixed frame to an existing stable TF frame.
- Warning before destructive commands: asset path errors are usually install-rule or launch-path bugs; inspect installed share files before deleting artifacts.

## Verification commands
- `ros2 run xacro xacro <path/to/file.urdf.xacro> > /tmp/robot.urdf`
- `check_urdf /tmp/robot.urdf` if `urdfdom` tools are installed
- `ros2 launch <pkg> <display.launch.py>`
- `ros2 run tf2_tools view_frames`
- `ros2 topic echo /robot_description --once` if published as a topic by the setup

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
RViz and robot_state_publisher examples vary by distro and language; prefer installed share paths over source-relative paths across all distros.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html
