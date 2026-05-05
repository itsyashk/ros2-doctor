# Sources

This file records sources used to shape `ros2-doctor`. Official ROS 2, colcon,
ament, and REP documentation is treated as the authority. Community sources are
used only to identify recurring real-world error signatures and are rewritten in
original wording throughout the skill.

## Source Quality Rules

- Prefer official ROS 2, colcon, ament, package, and REP documentation.
- Use Robotics StackExchange, Stack Overflow, ROS Discourse, GitHub issues,
  Reddit, and blogs only as pattern-discovery sources.
- Do not copy forum answers into playbooks.
- If official documentation and community advice conflict, follow the official
  documentation and note the uncertainty.
- Avoid unverifiable claims and avoid Quora.

## Official Sources

| Area | Source | Notes |
| --- | --- | --- |
| ROS 2 package structure | https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html | Minimum CMake and Python package contents. |
| ROS 2 package development | https://docs.ros.org/en/rolling/How-To-Guides/Developing-a-ROS-2-Package.html | `ament_python`, `ament_cmake`, launch and executable install examples. |
| `ament_cmake` | https://docs.ros.org/en/rolling/How-To-Guides/Ament-CMake-Documentation.html | CMake package layout, dependencies, targets, install rules, `ament_package()`. |
| `ament_cmake_python` | https://docs.ros.org/en/rolling/How-To-Guides/Ament-CMake-Python-Documentation.html | Mixed CMake/Python package background. |
| colcon build workflow | https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html | Workspace layout, underlay/overlay basics, build/install/log directories. |
| colcon workspace overview | https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html | Workspace terminology used by build playbooks. |
| colcon overlays and underlays | https://colcon.readthedocs.io/en/released/user/using-multiple-workspaces.html | Multiple workspace sourcing and override cautions. |
| colcon package overriding | https://colcon.readthedocs.io/en/released/user/overriding-packages.html | Overlay override cautions and ABI/header risks. |
| rosdep | https://docs.ros.org/en/rolling/Tutorials/Intermediate/Rosdep.html | Dependency keys, package.xml dependency role, workspace install command. |
| Launch overview | https://docs.ros.org/en/rolling/Tutorials/Intermediate/Launch/Launch-Main.html | Launch concepts and related tutorials. |
| Launch file formats | https://docs.ros.org/en/rolling/How-To-Guides/Launch-file-different-formats.html | Python, XML, and YAML launch file formats. |
| Launch files in packages | https://docs.ros.org/en/rolling/Tutorials/Intermediate/Launch/Launch-system.html | Installing launch files for Python and C++ packages. |
| TF2 overview | https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Tf2.html | Transform tree concepts and frame relationships. |
| TF2 intro tutorial | https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html | Tutorial-level TF2 command and frame context used in playbooks. |
| TF2 debugging | https://docs.ros.org/en/rolling/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html | `tf2_echo`, `tf2_monitor`, `view_frames`, frame and timestamp workflow. |
| URDF | https://docs.ros.org/en/rolling/Tutorials/Intermediate/URDF/URDF-Main.html | URDF overview and related tutorials. |
| xacro | https://docs.ros.org/en/rolling/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html | Macro-based URDF authoring. |
| RViz | https://docs.ros.org/en/rolling/Tutorials/Intermediate/RViz/RViz-Main.html | RViz overview and visualization tutorials. |
| RViz user guide | https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html | RViz fixed frame and display context used in visualization playbooks. |
| robot_state_publisher | https://docs.ros.org/en/rolling/p/robot_state_publisher/ | Publishing robot link poses from a kinematic tree. |
| robot_state_publisher tutorial | https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html | Python tutorial context for URDF publishing examples. |
| ROS 2 interfaces | https://docs.ros.org/en/rolling/Concepts/Basic/About-Interfaces.html | Message, service, and action interface concepts. |
| Custom msg/srv generation | https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html | `rosidl_generate_interfaces`, dependencies, package.xml tags. |
| Custom actions | https://docs.ros.org/en/rolling/Tutorials/Intermediate/Creating-an-Action.html | Action package structure and interface-package practice. |
| ROS 2 target platforms | https://www.ros.org/reps/rep-2000.html | Release support windows and target platform matrix. |
| Humble release | https://docs.ros.org/en/humble/Releases/Release-Humble-Hawksbill.html | Humble release and platform notes. |
| Jazzy release | https://docs.ros.org/en/jazzy/Releases/Release-Jazzy-Jalisco.html | Jazzy release and platform notes. |
| Kilted release | https://docs.ros.org/en/kilted/Releases/Release-Kilted-Kaiju.html | Kilted release and platform notes. |
| Rolling release | https://docs.ros.org/en/rolling/Releases/Release-Rolling-Ridley.html | Rolling development distribution notes. |
| Platform EOL policy | https://docs.ros.org/en/kilted/The-ROS2-Project/Platform-EOL-Policy.html | EOL and unsupported platform cautions. |
| Installation troubleshooting | https://docs.ros.org/en/humble/How-To-Guides/Installation-Troubleshooting.html | Python/environment compatibility troubleshooting. |
| Humble package structure | https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html | Humble-specific counterpart cited by playbooks. |
| Humble package development | https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html | Humble-specific package development guidance cited by playbooks. |
| Humble `ament_cmake` | https://docs.ros.org/en/humble/How-To-Guides/Ament-CMake-Documentation.html | Humble-specific CMake package guidance cited by playbooks. |
| Humble colcon workflow | https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html | Humble-specific workspace build guidance cited by playbooks. |
| Humble rosdep | https://docs.ros.org/en/humble/Tutorials/Intermediate/Rosdep.html | Humble-specific dependency guidance cited by playbooks. |
| Humble launch overview | https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html | Humble-specific launch guidance cited by playbooks. |
| Humble launch formats | https://docs.ros.org/en/humble/How-To-Guides/Launch-file-different-formats.html | Humble-specific launch format guidance cited by playbooks. |
| Humble launch package integration | https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-system.html | Humble-specific launch install guidance cited by playbooks. |
| Humble TF2 debugging | https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html | Humble-specific TF debug commands cited by playbooks. |
| Humble URDF | https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html | Humble-specific URDF guidance cited by playbooks. |
| Humble xacro | https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html | Humble-specific xacro guidance cited by playbooks. |
| Humble custom actions | https://docs.ros.org/en/humble/Tutorials/Intermediate/Creating-an-Action.html | Humble-specific action tutorial cited by playbooks. |

## Community Pattern Sources

| Pattern | Source | Trust | Notes |
| --- | --- | --- | --- |
| `ament_cmakeConfig.cmake` not found | https://robotics.stackexchange.com/questions/96454/ros2-colcon-build-fails-to-find-configuration-file-provided-by-ament-cmake | Medium | Pattern: underlay not sourced or CMake prefix cannot see ROS install. |
| Missing CMake package configs in source builds | https://github.com/ros2/ros2/issues/710 | High | Pattern: missing dependency workspace, partial source checkout, or stale copied artifacts. |
| Package not found after build | https://robotics.stackexchange.com/questions/95261/error-ros2-run-package-not-found | Medium | Pattern: built from wrong directory or sourced wrong overlay. |
| Package search path only includes underlay | https://robotics.stackexchange.com/questions/114590/ros-2-package-not-found-after-successful-build-ros2-pkg-list-not-detecting-pack | Medium | Pattern: current shell has not sourced the workspace overlay. |
| Missing Python package marker | https://robotics.stackexchange.com/questions/97794/ament-python-package-doesnt-explicitly-install-a-marker-in-the-package-index | Medium | Pattern: missing `resource/<pkg>` and package.xml install in `setup.py`. |
| Python executable not found by `ros2 run` | https://answers.ros.org/question/365683 | Medium | Pattern: missing `setup.cfg`, console entry point, or libexec install path. |
| Launch libexec executable mismatch | https://robotics.stackexchange.com/questions/114072/ros2-run-works-ok-but-ros2-launch-gives-executable-not-found-on-the-libexec-dir | Medium | Pattern: launch executable name differs from installed entry point. |
| Launch file missing from package share | https://robotics.stackexchange.com/questions/25013/ros2-launch-file-was-not-found-in-the-share-directory | Medium | Pattern: launch files not installed into package share directory. |
| Local package shadows ROS launch module | https://stackoverflow.com/questions/79109423/ros2-launch-error-when-installing-my-package | Medium | Pattern: local `launch` Python package conflicts with ROS 2 launch imports. |
| Launch substitution object used as executable | https://robotics.stackexchange.com/questions/111010/executable-launch-substitutions-text-substitution-textsubstitution-not-found | Medium | Pattern: launch substitutions not resolved into the intended command/string. |
| ROS 1 dependencies in ROS 2 workspace | https://robotics.stackexchange.com/questions/99330/rosdep-install-not-locating-definitions-rostime-catkin-rospy | Medium | Pattern: wrong branch or ROS 1 package source in ROS 2 workspace. |
| OS/distro support mismatch | https://robotics.stackexchange.com/questions/104586/cannot-locate-rosdep-definition-error-on-micro-ros | Medium | Pattern: tutorial or package branch does not match distro/platform. |
| Missing rosdep key | https://stackoverflow.com/questions/77899289/how-to-solve-the-error-cannot-locate-rosdep-definition-for-pcl | Medium | Pattern: dependency key is unreleased, stale, renamed, or should be sourced. |
| Missing rosdep definition | https://stackoverflow.com/questions/24187277/ros-ptam-cannot-locate-rosdep-definition | Medium | Pattern: rosdep key may be ROS-version-specific, absent, or provided by a different package source. |
| Gazebo integration package missing | https://www.reddit.com/r/ROS/comments/16rsnmc | Low | Anecdotal pattern: missing `gazebo_ros` integration for active distro. |
| Build killed by OOM | https://www.reddit.com/r/ROS/comments/1fy50x5 | Low | Anecdotal pattern: parallel build exceeds memory. |
| Python environment conflict | https://stackoverflow.com/questions/77351644/ros2-catkin-pkg-not-found-is-installed-and-using-version-3-8 | Medium | Pattern: wrong Python interpreter or environment selected during build. |
| Custom message field syntax | https://stackoverflow.com/questions/71970577/ros2-custom-messages-build-failed-with-invalidfielddefinition | Medium | Pattern: `.msg` field missing a variable name. |
| Interface type support import failure | https://github.com/ros2/examples/issues/303 | High/Medium | Pattern: generated type support missing or wrong Python/build artifacts. |
| External interface dependency missing | https://stackoverflow.com/questions/74930849/how-to-create-a-ros2-custom-message-that-contains-sensor-msgs-image-image | Medium | Pattern: external message package absent from CMake/package metadata. |
| TF extrapolation into future | https://robotics.stackexchange.com/questions/96614/nav2-teb-lookup-would-require-extrapolation-into-the-future | Medium | Pattern: transform publication timing/rate/tolerance issue. |
| TF extrapolation and sim time mismatch | https://robotics.stackexchange.com/questions/91993/tf2-transform-error-lookup-would-require-extrapolation-into-the-past | Medium | Pattern: mixed simulation time and wall time. |
| RViz fixed frame missing | https://robotics.stackexchange.com/questions/33352/no-transform-from-base-link-to-map | Medium | Pattern: fixed frame is absent from current TF tree. |
| Launch/share edits require rebuild | https://discourse.ros.org/t/colcon-build-from-any-directory-and-need-to-re-build-for-changes-in-launch-file/17353 | Medium | Pattern: installed launch/config files are stale or not symlink-installed. |
| `ament_python` boilerplate complexity | https://discourse.ros.org/t/why-is-there-no-ament-python-simple/42591 | Medium | Pattern: Python package discovery issues often come from partial boilerplate. |
