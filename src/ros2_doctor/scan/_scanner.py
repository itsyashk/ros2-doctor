#!/usr/bin/env python3
"""Read-only ROS 2 workspace scanner.

Run this script from a workspace root. It uses only the Python standard library
and does not require ROS 2 to be installed.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

KNOWN_DISTROS = ("humble", "jazzy", "kilted", "rolling")
LAUNCH_SUFFIXES = (
    ".launch.py",
    ".launch.xml",
    ".launch.yaml",
    ".launch.yml",
    ".launch",
)
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
    "build",
    "install",
    "log",
}
TEXT_EXTENSIONS = {
    "",
    ".cmake",
    ".cfg",
    ".launch",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class Package:
    name: str
    path: Path
    build_type: str
    package_xml: Path
    has_cmakelists: bool
    has_setup_py: bool
    has_setup_cfg: bool
    has_pyproject: bool
    exec_names: tuple[str, ...] = field(default_factory=tuple)
    python_modules: tuple[Path, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class LaunchRef:
    launch_file: Path
    package: str
    executable: str


def rel(path: Path, root: Path) -> str:
    try:
        text = path.relative_to(root).as_posix()
    except ValueError:
        text = path.as_posix()
    return "." if text == "" else text


def read_text(path: Path, limit: int = 512_000) -> str:
    try:
        with path.open("rb") as handle:
            data = handle.read(limit + 1)
    except OSError:
        return ""
    if len(data) > limit:
        data = data[:limit]
    return data.decode("utf-8", errors="replace")


def iter_files(root: Path, include_build_artifacts: bool = False) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        kept = []
        for dirname in dirnames:
            if dirname in SKIP_DIRS and not (
                include_build_artifacts
                and current == root
                and dirname in {"build", "install", "log"}
            ):
                continue
            kept.append(dirname)
        dirnames[:] = sorted(kept)
        for filename in sorted(filenames):
            yield current / filename


def iter_package_xmls(root: Path) -> list[Path]:
    found: set[Path] = set()
    for candidate_root in (root, root / "src"):
        if not candidate_root.exists():
            continue
        for file_path in iter_files(candidate_root):
            if file_path.name == "package.xml":
                found.add(file_path)
    return sorted(found, key=lambda path: rel(path, root))


def parse_package_xml(path: Path) -> tuple[str, str]:
    text = read_text(path)
    fallback_name = path.parent.name
    if not text.strip():
        return fallback_name, "unknown"
    try:
        package = ET.fromstring(text)
    except ET.ParseError:
        name_match = re.search(r"<name>\s*([^<]+?)\s*</name>", text, re.IGNORECASE)
        build_match = re.search(r"<build_type>\s*([^<]+?)\s*</build_type>", text, re.IGNORECASE)
        return (
            name_match.group(1).strip() if name_match else fallback_name,
            build_match.group(1).strip() if build_match else "unknown",
        )

    name = package.findtext("name") or fallback_name
    build_type = "ament_cmake"
    for export in package.findall("export"):
        exported = export.findtext("build_type")
        if exported and exported.strip():
            build_type = exported.strip()
            break
    return name.strip(), build_type


def string_values(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values: list[str] = []
        for item in node.elts:
            values.extend(string_values(item))
        return values
    return []


def parse_setup_py(path: Path) -> tuple[tuple[str, ...], bool, bool]:
    text = read_text(path)
    entry_points: list[str] = []
    has_console_scripts = "console_scripts" in text
    has_resource_marker = "share/ament_index/resource_index/packages" in text
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return (), has_resource_marker, has_console_scripts

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func_name = getattr(node.func, "id", "") or getattr(node.func, "attr", "")
        if func_name != "setup":
            continue
        for keyword in node.keywords:
            if keyword.arg == "data_files":
                has_resource_marker = has_resource_marker or any(
                    "share/ament_index/resource_index/packages" in value
                    for value in string_values(keyword.value)
                )
            if keyword.arg == "entry_points":
                parsed = parse_entry_points(keyword.value)
                entry_points.extend(parsed)
                has_console_scripts = has_console_scripts or bool(parsed)
    return tuple(sorted(set(entry_points))), has_resource_marker, has_console_scripts


def parse_entry_points(node: ast.AST) -> list[str]:
    names: list[str] = []
    if not isinstance(node, ast.Dict):
        return names
    for key, value in zip(node.keys, node.values):
        key_values = string_values(key) if key else []
        if "console_scripts" not in key_values:
            continue
        for item in string_values(value):
            script_name = item.split("=", 1)[0].strip()
            if script_name:
                names.append(script_name)
    return names


def parse_setup_cfg(path: Path) -> tuple[str, ...]:
    text = read_text(path)
    names: list[str] = []
    in_console_scripts = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_console_scripts = False
        if stripped == "console_scripts" or stripped.startswith("console_scripts ="):
            in_console_scripts = True
            continue
        if in_console_scripts:
            if not line.startswith((" ", "\t")) or not stripped:
                if stripped:
                    in_console_scripts = False
                continue
            script_name = stripped.split("=", 1)[0].strip()
            if script_name:
                names.append(script_name)
    return tuple(sorted(set(names)))


def parse_pyproject(path: Path) -> tuple[str, ...]:
    text = read_text(path)
    names: list[str] = []
    in_scripts = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            in_scripts = stripped == "[project.scripts]"
            continue
        if in_scripts and "=" in stripped:
            names.append(stripped.split("=", 1)[0].strip().strip("'\""))
    return tuple(sorted(set(name for name in names if name)))


def parse_cmakelists(path: Path) -> tuple[str, ...]:
    text = strip_cmake_comments(read_text(path))
    names: set[str] = set()
    for match in re.finditer(r"\badd_executable\s*\(\s*([A-Za-z0-9_.+-]+)", text, re.IGNORECASE):
        names.add(match.group(1))
    for match in re.finditer(
        r"\brclcpp_components_register_node\s*\([^)]*\bEXECUTABLE\s+([A-Za-z0-9_.+-]+)",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        names.add(match.group(1))
    for match in re.finditer(
        r"\binstall\s*\(\s*PROGRAMS\s+(.*?)\bDESTINATION\s+lib",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        for token in re.split(r"\s+", match.group(1).strip()):
            if token and not token.startswith("$"):
                names.add(Path(token).name)
    return tuple(sorted(names))


def strip_cmake_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        lines.append(line.split("#", 1)[0])
    return "\n".join(lines)


def find_python_package_dirs(package_dir: Path) -> tuple[Path, ...]:
    candidates: set[Path] = set()
    for setup_file in (
        package_dir / "setup.py",
        package_dir / "setup.cfg",
        package_dir / "pyproject.toml",
    ):
        if not setup_file.exists():
            continue
        text = read_text(setup_file)
        for match in re.finditer(r"packages\s*=\s*\[([^\]]+)\]", text):
            for name in re.findall(r"['\"]([A-Za-z_][A-Za-z0-9_.]*)['\"]", match.group(1)):
                candidates.add(package_dir / Path(name.replace(".", "/")))
        for match in re.finditer(r"['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", text):
            possible = package_dir / match.group(1)
            if possible.is_dir() and possible.name not in {"test", "tests"}:
                candidates.add(possible)

    for child in sorted(package_dir.iterdir() if package_dir.exists() else []):
        if (
            child.is_dir()
            and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", child.name)
            and child.name not in {"launch", "resource", "test", "tests"}
            and any(file_path.suffix == ".py" for file_path in child.glob("*.py"))
        ):
            candidates.add(child)
    return tuple(sorted(candidates))


def collect_packages(root: Path) -> tuple[list[Package], list[str]]:
    packages: list[Package] = []
    issues: list[str] = []
    package_xmls = iter_package_xmls(root)
    package_dirs = {path.parent for path in package_xmls}

    for package_xml in package_xmls:
        package_dir = package_xml.parent
        name, build_type = parse_package_xml(package_xml)
        has_setup_py = (package_dir / "setup.py").exists()
        has_setup_cfg = (package_dir / "setup.cfg").exists()
        has_pyproject = (package_dir / "pyproject.toml").exists()
        has_cmakelists = (package_dir / "CMakeLists.txt").exists()

        exec_names: list[str] = []
        setup_resource_marker = True
        setup_console_scripts = True
        if has_setup_py:
            parsed, setup_resource_marker, setup_console_scripts = parse_setup_py(
                package_dir / "setup.py"
            )
            exec_names.extend(parsed)
        if has_setup_cfg:
            exec_names.extend(parse_setup_cfg(package_dir / "setup.cfg"))
        if has_pyproject:
            exec_names.extend(parse_pyproject(package_dir / "pyproject.toml"))
        if has_cmakelists:
            exec_names.extend(parse_cmakelists(package_dir / "CMakeLists.txt"))

        packages.append(
            Package(
                name=name,
                path=package_dir,
                build_type=build_type,
                package_xml=package_xml,
                has_cmakelists=has_cmakelists,
                has_setup_py=has_setup_py,
                has_setup_cfg=has_setup_cfg,
                has_pyproject=has_pyproject,
                exec_names=tuple(sorted(set(exec_names))),
                python_modules=find_python_package_dirs(package_dir),
            )
        )

        if not has_setup_py and not has_cmakelists:
            suffix = " Only `pyproject.toml` was found." if has_pyproject else ""
            issues.append(
                f"`{rel(package_xml, root)}` has no `setup.py` or `CMakeLists.txt` nearby.{suffix}"
            )
        if build_type == "ament_python" and not (has_setup_py or has_pyproject):
            issues.append(f"`{name}` declares `ament_python` but no Python build file was found.")
        if build_type == "ament_cmake" and not has_cmakelists:
            issues.append(f"`{name}` appears to be `ament_cmake` but has no `CMakeLists.txt`.")
        if has_setup_py and not setup_resource_marker:
            issues.append(
                f"`{rel(package_dir / 'setup.py', root)}` may be missing the ament resource marker in `data_files`."
            )
        if has_setup_py and not setup_console_scripts:
            issues.append(
                f"`{rel(package_dir / 'setup.py', root)}` has no detected `console_scripts` entry point; this matters only if the package should expose nodes with `ros2 run`."
            )
        for module_dir in find_python_package_dirs(package_dir):
            if not (module_dir / "__init__.py").exists():
                issues.append(
                    f"`{rel(module_dir, root)}` looks like a Python package dir but lacks `__init__.py`."
                )

    for package_dir in package_dirs:
        nested = sorted(
            other for other in package_dirs if other != package_dir and package_dir in other.parents
        )
        for nested_dir in nested:
            issues.append(
                f"Nested package detected: `{rel(nested_dir, root)}` is inside `{rel(package_dir, root)}`."
            )

    return sorted(packages, key=lambda pkg: (pkg.name, rel(pkg.path, root))), sorted(set(issues))


def is_launch_file(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in LAUNCH_SUFFIXES)


def collect_by_kind(root: Path) -> dict[str, list[Path]]:
    result = {
        "launch": [],
        "interfaces": [],
        "robot_descriptions": [],
        "rviz": [],
        "docker": [],
        "devcontainer": [],
        "workflows": [],
        "build_artifacts": [],
    }
    for file_path in iter_files(root, include_build_artifacts=True):
        lower = file_path.name.lower()
        try:
            parts = file_path.relative_to(root).parts
        except ValueError:
            parts = file_path.parts
        if is_launch_file(file_path):
            result["launch"].append(file_path)
        if file_path.suffix in {".msg", ".srv", ".action"} and any(
            part in {"msg", "srv", "action"} for part in parts
        ):
            result["interfaces"].append(file_path)
        if file_path.suffix in {".urdf", ".xacro"} or lower.endswith(".urdf.xacro"):
            result["robot_descriptions"].append(file_path)
        if file_path.suffix == ".rviz":
            result["rviz"].append(file_path)
        if lower in {"dockerfile", "dockerfile.dev"} or lower.startswith("dockerfile."):
            result["docker"].append(file_path)
        if ".devcontainer" in parts:
            result["devcontainer"].append(file_path)
        if len(parts) >= 3 and parts[0] == ".github" and parts[1] == "workflows":
            result["workflows"].append(file_path)
        if parts and parts[0] in {"build", "install", "log"}:
            result["build_artifacts"].append(file_path)
    return {key: sorted(value, key=lambda path: rel(path, root)) for key, value in result.items()}


def find_distro_hints(root: Path) -> dict[str, list[Path]]:
    hints: dict[str, set[Path]] = {distro: set() for distro in KNOWN_DISTROS}
    interesting_names = {
        "package.xml",
        "cmakelists.txt",
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "dockerfile",
        "devcontainer.json",
    }
    for file_path in iter_files(root):
        lower_name = file_path.name.lower()
        lower_path = rel(file_path, root).lower()
        if file_path.suffix.lower() not in TEXT_EXTENSIONS and lower_name not in interesting_names:
            continue
        if not (
            lower_name in interesting_names
            or ".github/workflows/" in lower_path
            or ".devcontainer/" in lower_path
            or lower_name.startswith("dockerfile")
        ):
            continue
        text = read_text(file_path, limit=128_000).lower()
        combined = f"{lower_path}\n{text}"
        for distro in KNOWN_DISTROS:
            if re.search(rf"(?<![a-z0-9_]){re.escape(distro)}(?![a-z0-9_])", combined):
                hints[distro].add(file_path)
    return {
        distro: sorted(paths, key=lambda path: rel(path, root))
        for distro, paths in hints.items()
        if paths
    }


def collect_launch_refs(root: Path, launch_files: list[Path]) -> list[LaunchRef]:
    refs: list[LaunchRef] = []
    node_patterns = [
        re.compile(
            r"Node\s*\((?P<body>.*?)\)",
            re.DOTALL,
        ),
        re.compile(
            r"<node\b(?P<body>[^>]*?)>",
            re.DOTALL,
        ),
    ]
    attr_patterns = {
        "package": [
            re.compile(r"package\s*=\s*['\"]([^'\"]+)['\"]"),
            re.compile(r"pkg\s*=\s*['\"]([^'\"]+)['\"]"),
            re.compile(r"\bpackage=['\"]([^'\"]+)['\"]"),
            re.compile(r"\bpkg=['\"]([^'\"]+)['\"]"),
        ],
        "executable": [
            re.compile(r"executable\s*=\s*['\"]([^'\"]+)['\"]"),
            re.compile(r"exec\s*=\s*['\"]([^'\"]+)['\"]"),
            re.compile(r"\bexecutable=['\"]([^'\"]+)['\"]"),
            re.compile(r"\bexec=['\"]([^'\"]+)['\"]"),
            re.compile(r"\btype=['\"]([^'\"]+)['\"]"),
        ],
    }
    for launch_file in launch_files:
        text = read_text(launch_file, limit=256_000)
        for node_pattern in node_patterns:
            for match in node_pattern.finditer(text):
                body = match.group("body")
                package = first_match(body, attr_patterns["package"])
                executable = first_match(body, attr_patterns["executable"])
                if package and executable and "$" not in package + executable:
                    refs.append(LaunchRef(launch_file, package, executable))
    return sorted(
        set(refs), key=lambda item: (rel(item.launch_file, root), item.package, item.executable)
    )


def first_match(text: str, patterns: list[re.Pattern[str]]) -> str:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return ""


def launch_reference_issues(
    root: Path, packages: list[Package], refs: list[LaunchRef]
) -> list[str]:
    by_name = {package.name: package for package in packages}
    issues: list[str] = []
    for ref in refs:
        package = by_name.get(ref.package)
        location = rel(ref.launch_file, root)
        if package is None:
            issues.append(
                f"`{location}` references package `{ref.package}` executable `{ref.executable}`, but that package was not found in this workspace."
            )
            continue
        known_execs = set(package.exec_names)
        likely_binary_paths = [
            package.path / ref.executable,
            package.path / "scripts" / ref.executable,
            package.path / "nodes" / ref.executable,
            package.path / package.name / ref.executable,
            package.path / package.name / f"{ref.executable}.py",
            package.path / "src" / ref.executable,
        ]
        if known_execs and ref.executable not in known_execs:
            issues.append(
                f"`{location}` references `{ref.package}/{ref.executable}`, which was not found in detected console scripts: {', '.join(f'`{name}`' for name in sorted(known_execs))}."
            )
        elif not known_execs and not any(path.exists() for path in likely_binary_paths):
            issues.append(
                f"`{location}` references `{ref.package}/{ref.executable}`, but no obvious script or binary path was detected."
            )
    return sorted(set(issues))


def artifact_issues(root: Path) -> list[str]:
    issues: list[str] = []
    src_files = [
        path
        for path in iter_files(root)
        if path.name in {"package.xml", "CMakeLists.txt", "setup.py", "setup.cfg", "pyproject.toml"}
    ]
    newest_source = max(
        (path.stat().st_mtime for path in src_files if safe_stat(path)), default=None
    )
    for dirname in ("build", "install", "log"):
        path = root / dirname
        if not path.exists():
            continue
        stat = safe_stat(path)
        if stat is None:
            continue
        child_count = sum(1 for _ in path.iterdir()) if path.is_dir() else 0
        stamp = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        if newest_source and stat.st_mtime < newest_source:
            issues.append(
                f"`{dirname}/` exists ({child_count} entries, modified {stamp}) and may be older than source metadata."
            )
        else:
            issues.append(
                f"`{dirname}/` exists ({child_count} entries, modified {stamp}); verify it is not stale before debugging."
            )
    return issues


def safe_stat(path: Path):
    try:
        return path.stat()
    except OSError:
        return None


def command_status() -> list[str]:
    rows = []
    for command in ("ros2", "colcon", "vcs"):
        found = shutil.which(command)
        rows.append(
            f"`{command}`: {'available at `' + found + '`' if found else 'not found on PATH'}"
        )
    return rows


def distro_mismatch_issues(env_distro: str, hints: dict[str, list[Path]]) -> list[str]:
    issues: list[str] = []
    hinted = set(hints)
    if env_distro:
        lower_env = env_distro.lower()
        if lower_env in KNOWN_DISTROS:
            other_hints = sorted(hinted - {lower_env})
            if other_hints:
                issues.append(
                    f"`ROS_DISTRO={env_distro}` but files mention other ROS distros: {', '.join(f'`{item}`' for item in other_hints)}."
                )
        elif hinted:
            issues.append(
                f"`ROS_DISTRO={env_distro}` is not one of {', '.join(KNOWN_DISTROS)}, while files mention {', '.join(f'`{item}`' for item in sorted(hinted))}."
            )
    elif len(hinted) > 1:
        issues.append(
            f"Multiple distro hints found with no `ROS_DISTRO` set: {', '.join(f'`{item}`' for item in sorted(hinted))}."
        )
    return issues


def bullet_list(items: Iterable[str], empty: str = "None found.") -> list[str]:
    values = list(items)
    if not values:
        return [f"- {empty}"]
    return [f"- {item}" for item in values]


def scan_workspace(root: Path) -> dict:
    """Run workspace scan and return structured data."""
    root = root.resolve()
    src = root / "src"

    packages, package_issues = collect_packages(root)
    found = collect_by_kind(root)
    distro_hints = find_distro_hints(root)
    launch_refs = collect_launch_refs(root, found["launch"])

    issues: list[str] = []
    if not src.exists():
        issues.append("`src/` is missing. ROS 2 workspaces commonly keep packages under `src/`.")
    elif not src.is_dir():
        issues.append("`src` exists but is not a directory.")
    issues.extend(package_issues)
    issues.extend(launch_reference_issues(root, packages, launch_refs))
    issues.extend(distro_mismatch_issues(os.environ.get("ROS_DISTRO", ""), distro_hints))
    issues.extend(artifact_issues(root))
    issues = sorted(set(issues))

    lines: list[str] = []
    lines.append("# ROS 2 Workspace Scan")
    lines.append("")

    lines.append("## Distro Evidence")
    env_distro = os.environ.get("ROS_DISTRO", "")
    lines.extend(
        bullet_list(
            [
                f"`ROS_DISTRO`: `{env_distro}`" if env_distro else "`ROS_DISTRO`: not set",
                f"`AMENT_PREFIX_PATH`: {'set' if os.environ.get('AMENT_PREFIX_PATH') else 'not set'}",
                f"`CMAKE_PREFIX_PATH`: {'set' if os.environ.get('CMAKE_PREFIX_PATH') else 'not set'}",
                *command_status(),
            ]
        )
    )
    if distro_hints:
        for distro, paths in sorted(distro_hints.items()):
            shown = ", ".join(f"`{rel(path, root)}`" for path in paths[:8])
            extra = f" (+{len(paths) - 8} more)" if len(paths) > 8 else ""
            lines.append(f"- `{distro}` hints: {shown}{extra}")
    else:
        lines.append("- No Humble/Jazzy/Kilted/Rolling hints found in common config files.")
    lines.append("")

    lines.append("## Workspace Structure")
    structure_items = [
        f"Root: `{root}`",
        f"`src/`: {'present' if src.is_dir() else 'missing'}",
        f"`build/`: {'present' if (root / 'build').exists() else 'missing'}",
        f"`install/`: {'present' if (root / 'install').exists() else 'missing'}",
        f"`log/`: {'present' if (root / 'log').exists() else 'missing'}",
        f"Docker files: {len(found['docker'])}",
        f"Devcontainer files: {len(found['devcontainer'])}",
        f"GitHub workflow files: {len(found['workflows'])}",
    ]
    lines.extend(bullet_list(structure_items))
    lines.append("")

    lines.append("## Packages Found")
    if packages:
        for package in packages:
            files = []
            if package.has_cmakelists:
                files.append("CMakeLists.txt")
            if package.has_setup_py:
                files.append("setup.py")
            if package.has_setup_cfg:
                files.append("setup.cfg")
            if package.has_pyproject:
                files.append("pyproject.toml")
            file_text = ", ".join(files) if files else "no build files detected"
            lines.append(
                f"- `{package.name}` at `{rel(package.path, root)}` (`{package.build_type}`; {file_text})"
            )
    else:
        lines.append("- None found.")
    lines.append("")

    lines.append("## Build Types")
    if packages:
        build_counts: dict[str, int] = {}
        for package in packages:
            build_counts[package.build_type] = build_counts.get(package.build_type, 0) + 1
        for build_type, count in sorted(build_counts.items()):
            names = ", ".join(
                f"`{package.name}`" for package in packages if package.build_type == build_type
            )
            lines.append(f"- `{build_type}`: {count} package(s): {names}")
    else:
        lines.append("- None found.")
    lines.append("")

    lines.append("## Launch Files")
    lines.extend(bullet_list(f"`{rel(path, root)}`" for path in found["launch"]))
    if launch_refs:
        lines.append("")
        lines.append("Detected launch executable references:")
        for ref in launch_refs:
            lines.append(f"- `{rel(ref.launch_file, root)}` -> `{ref.package}/{ref.executable}`")
    lines.append("")

    lines.append("## Robot Description Files")
    robot_items = [f"`{rel(path, root)}`" for path in found["robot_descriptions"]]
    robot_items.extend(f"`{rel(path, root)}`" for path in found["rviz"])
    lines.extend(bullet_list(sorted(robot_items)))
    lines.append("")

    lines.append("## Interface Files")
    lines.extend(bullet_list(f"`{rel(path, root)}`" for path in found["interfaces"]))
    lines.append("")

    lines.append("## Possible Issues")
    lines.extend(bullet_list((issue for issue in issues), empty="No obvious issues detected."))
    lines.append("")

    lines.append("## Suggested Next Commands")
    suggested = [
        "`find src -name package.xml -print`",
        "`colcon list`",
        "`rosdep check --from-paths src --ignore-src --rosdistro <distro>`",
        "`colcon build --symlink-install`",
        "`source install/setup.bash`",
        "`ros2 launch <package> <launch_file>`",
    ]
    if not src.exists():
        suggested.insert(
            0, "Create `src/` only if this directory is intended to be a ROS 2 workspace."
        )
    if shutil.which("ros2") is None:
        suggested.append("Install or source a ROS 2 distribution before running ROS commands.")
    lines.extend(f"- {item}" for item in suggested)

    return {
        "root": root,
        "packages": packages,
        "found": found,
        "distro_hints": distro_hints,
        "launch_refs": launch_refs,
        "issues": issues,
        "lines": lines,
        "env_distro": env_distro,
    }


def emit_markdown(root: Path | None = None) -> str:
    data = scan_workspace(root or Path.cwd())
    return "\n".join(data["lines"]) + "\n"
