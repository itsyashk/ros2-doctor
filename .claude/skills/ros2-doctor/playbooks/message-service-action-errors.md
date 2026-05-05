# Playbook: Message service action errors

## When to use
Use when custom `.msg`, `.srv`, or `.action` files fail to parse, generate, import, or link from C++ or Python nodes.

## Error signatures
- `InvalidResourceName`
- `rosidl_adapter.parser.InvalidFieldDefinition`
- `The field name is invalid`
- `ModuleNotFoundError: No module named '<pkg>.msg'`
- `UnsupportedTypeSupport`
- `undefined reference to rosidl_typesupport`
- `ros2 interface show <pkg>/msg/<Name>` cannot find the interface

## Common causes
- `.msg` field missing a field name, for example `string` instead of `string name`.
- Interface package missing `rosidl_generate_interfaces()`.
- Missing `rosidl_default_generators` build tool dependency.
- Missing `<member_of_group>rosidl_interface_packages</member_of_group>`.
- Missing `DEPENDENCIES` in `rosidl_generate_interfaces()` for referenced message packages.
- Consumer package missing dependency on the interface package.
- Stale generated code after renaming interfaces. Treat as evidence-based.

## Files to inspect
- `msg/*.msg`
- `srv/*.srv`
- `action/*.action`
- Interface package `CMakeLists.txt`
- Interface package `package.xml`
- Consumer package `package.xml`
- Consumer `CMakeLists.txt` or Python imports

## Diagnosis workflow
1. Inspect interface syntax: `sed -n '1,160p' <pkg-path>/msg/<Name>.msg`.
2. Check generation rules: `rg 'rosidl_generate_interfaces|rosidl_default_generators|rosidl_interface_packages' <pkg-path>`.
3. Build interface package first: `colcon build --packages-select <interface_pkg> --event-handlers console_direct+`.
4. Source and verify: `source install/setup.bash && ros2 interface show <interface_pkg>/msg/<Name>`.
5. Build dependents: `colcon build --packages-up-to <consumer_pkg> --event-handlers console_direct+`.
6. If type support fails, inspect dependency declarations in both interface and consumer packages.

## Minimal fix patterns
- Correct message fields: `<type> <field_name>`, for example `string frame_id`.
- Add CMake generation:
  - `find_package(rosidl_default_generators REQUIRED)`
  - `rosidl_generate_interfaces(${PROJECT_NAME} "msg/Foo.msg" DEPENDENCIES std_msgs geometry_msgs)`
- Add package metadata:
  - `<buildtool_depend>rosidl_default_generators</buildtool_depend>`
  - `<exec_depend>rosidl_default_runtime</exec_depend>`
  - `<member_of_group>rosidl_interface_packages</member_of_group>`
- Add consumer dependencies on the interface package in `package.xml` and CMake/Python imports.
- Warning before destructive commands: after confirmed interface renames, delete only generated artifacts for the interface package and affected consumers, not the whole workspace by default.

## Verification commands
- `colcon build --packages-select <interface_pkg>`
- `source install/setup.bash`
- `ros2 interface list | rg '<interface_pkg>'`
- `ros2 interface show <interface_pkg>/msg/<Name>`
- `colcon build --packages-up-to <consumer_pkg>`

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
Action definitions require a CMake interface package; Python nodes can consume the generated interfaces after the interface package is built and sourced.

## Sources used
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
- https://docs.ros.org/en/humble/Tutorials/Intermediate/Creating-an-Action.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
