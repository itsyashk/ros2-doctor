# Playbook: C++ package errors

## When to use
Use for `ament_cmake` packages with CMake configure failures, compile errors, link errors, missing headers, missing executables, or exported library problems.

## Error signatures
- `Could not find a package configuration file provided by '<dep>'`
- `fatal error: <header>: No such file or directory`
- `undefined reference to`
- `No executable found`
- `cannot find -l<library>`
- Runtime loader error: `cannot open shared object file`

## Common causes
- Missing `find_package(<dep> REQUIRED)` or `ament_target_dependencies(<target> <dep>)`.
- Dependency declared in CMake but not in `package.xml`, or the reverse.
- Target not installed to `lib/${PROJECT_NAME}`.
- Public headers not installed or exported.
- Underlay not sourced before building.
- Overlay overriding an underlay package with incompatible headers or ABI. This is pattern-based; verify from include paths and sourced workspaces.

## Files to inspect
- `package.xml`
- `CMakeLists.txt`
- `include/<pkg>/`
- `src/`
- `log/latest_build/<pkg>/stdout_stderr.log`
- `install/<pkg>/include/`
- `install/<pkg>/lib/`

## Diagnosis workflow
1. Confirm package type: `rg 'ament_package|ament_cmake' <pkg-path>/CMakeLists.txt <pkg-path>/package.xml`.
2. Read the exact compiler/linker line: `sed -n '1,260p' log/latest_build/<pkg>/stdout_stderr.log`.
3. Check dependency presence: `ros2 pkg prefix <dep>` and `apt-cache policy ros-<distro>-<dep-with-dashes>`.
4. Check target install rules: `rg 'add_executable|add_library|install\\(|ament_target_dependencies|ament_export' <pkg-path>/CMakeLists.txt`.
5. Rebuild one package with direct output: `colcon build --packages-select <pkg> --event-handlers console_direct+`.

## Minimal fix patterns
- Add missing dependency:
  - `find_package(rclcpp REQUIRED)`
  - `ament_target_dependencies(<target> rclcpp <other_deps>)`
  - `<depend>rclcpp</depend>` in `package.xml`
- Install executables:
  - `install(TARGETS <target> DESTINATION lib/${PROJECT_NAME})`
- Install public headers:
  - `install(DIRECTORY include/ DESTINATION include)`
  - `ament_export_include_directories(include)`
- Export libraries when other packages link them:
  - `ament_export_targets(<export_name> HAS_LIBRARY_TARGET)`
  - `ament_export_dependencies(<deps>)`
- Keep `ament_package()` last after install/export declarations.
- Warning before destructive commands: use package-scoped artifact deletion only after proving stale CMake cache or old headers are involved.

## Verification commands
- `colcon build --packages-select <pkg> --event-handlers console_direct+`
- `source install/setup.bash`
- `ros2 run <pkg> <executable>`
- `colcon test --packages-select <pkg>`
- `ldd install/<pkg>/lib/<pkg>/<executable>` when runtime linking fails

## Distro-specific notes
If distro evidence is unclear, state: "Assumption: Humble is used as a practical default until evidence says otherwise."
C++ standard, dependency versions, and binary package availability vary by distro; check REP 2000 and the branch used by the workspace.

## Sources used
- https://docs.ros.org/en/humble/How-To-Guides/Ament-CMake-Documentation.html
- https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
- https://colcon.readthedocs.io/en/released/user/using-multiple-workspaces.html
- https://www.ros.org/reps/rep-2000.html
