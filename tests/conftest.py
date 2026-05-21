from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def minimal_workspace(tmp_path: Path) -> Path:
    src = FIXTURES / "minimal_ws"
    dest = tmp_path / "ws"
    import shutil

    shutil.copytree(src, dest)
    return dest


@pytest.fixture
def sample_colcon_log(tmp_path: Path) -> Path:
    log_pkg = tmp_path / "log" / "latest_build" / "failing_pkg"
    log_pkg.mkdir(parents=True)
    (log_pkg / "stderr.log").write_text(
        'Could not find a package configuration file provided by "missing_dep"\n',
        encoding="utf-8",
    )
    return tmp_path
