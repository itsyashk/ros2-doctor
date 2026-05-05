# ROS 2 Package Structure

Use this reference after identifying the package involved in the failure.

## Common Package Types

`ament_python` packages usually contain:

- `package.xml`
- `setup.py`
- `setup.cfg`
- `resource/<package_name>`
- `<package_name>/__init__.py`
- optional `launch/`, `config/`, `test/`

`ament_cmake` packages usually contain:

- `package.xml`
- `CMakeLists.txt`
- `include/<package_name>/` for public headers
- `src/` for implementation
- optional `launch/`, `config/`, `msg/`, `srv/`, `action/`

Interface packages usually contain `msg/`, `srv/`, or `action/` files and use
`rosidl_generate_interfaces()` from CMake. It is common to keep interfaces in a
separate package from the nodes that consume them.

Robot description packages usually contain URDF, xacro, mesh, and RViz assets.
They still need package metadata and install rules so launch files can find
resources from the installed package share directory.

## Common Structure Faults

- `package.xml` package name differs from `project()` in `CMakeLists.txt`.
- `setup.py` package name differs from `package.xml`.
- Python module directory lacks `__init__.py`.
- `resource/<package_name>` is missing or not installed.
- Launch/config/URDF/mesh files exist in source but are not installed.
- Interface dependencies appear in `.msg` files but not in CMake/package metadata.

## Commands

```bash
find src -name package.xml -maxdepth 4
colcon list
ros2 pkg prefix <package_name>
ros2 pkg executables <package_name>
```

If ROS 2 is not installed, inspect files directly and use the scanner.
