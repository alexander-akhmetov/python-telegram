"""
Build hook that turns the pure wheel into a platform wheel carrying one libtdjson.

Set PYTHON_TELEGRAM_TDLIB_TARGET to a target named in tdlib.lock, and
PYTHON_TELEGRAM_TDLIB_DIR to the directory holding the release assets. With
neither set the hook does nothing and the build produces the binary-free pure
wheel that `pip install -e .` needs.

    PYTHON_TELEGRAM_TDLIB_TARGET=macos-arm64 PYTHON_TELEGRAM_TDLIB_DIR=tdlib \
        python -m build --wheel

The hook is registered under the wheel target only, so the sdist never sees it.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

TARGET_ENV_VAR = "PYTHON_TELEGRAM_TDLIB_TARGET"
SOURCE_DIR_ENV_VAR = "PYTHON_TELEGRAM_TDLIB_DIR"
LOCK_FILE_NAME = "tdlib.lock"


def _read_lock(root: Path) -> dict[str, Any]:
    lock_path = root / LOCK_FILE_NAME

    try:
        content = lock_path.read_text()
    except FileNotFoundError:
        raise RuntimeError(f"{lock_path} is missing, so no target can be resolved") from None

    lock: dict[str, Any] = json.loads(content)

    return lock


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as binary:
        for chunk in iter(lambda: binary.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def apply_tdlib_target(root: Path, build_data: dict[str, Any]) -> None:
    """
    Bundles the binary for PYTHON_TELEGRAM_TDLIB_TARGET and retags the wheel.

    Returns without touching build_data when no target is set. Every other
    failure raises: falling back to a pure wheel would publish a
    `py3-none-any` distribution that pip installs everywhere and that raises
    on first use.
    """
    target = os.environ.get(TARGET_ENV_VAR)

    if not target:
        return

    lock = _read_lock(root)
    targets = lock["targets"]

    if target not in targets:
        raise RuntimeError(f"{TARGET_ENV_VAR}={target} is not in {LOCK_FILE_NAME}: {', '.join(sorted(targets))}")

    spec = targets[target]
    expected = spec["sha256"]

    if len(expected) != 64 or not all(character in "0123456789abcdef" for character in expected):
        raise RuntimeError(
            f"{LOCK_FILE_NAME} has no sha256 for {target} (it says {expected!r}). "
            f"Fill it in from the BUILD-INFO.json of the {lock['release_tag']} release."
        )

    # Against root, not the process cwd: a wheel built from an unpacked sdist
    # runs the backend in a temporary directory.
    source = root / os.environ.get(SOURCE_DIR_ENV_VAR, "tdlib") / spec["asset"]

    if not source.is_file():
        raise RuntimeError(f"{source} does not exist; download the {lock['release_tag']} assets first")

    actual = _sha256(source)

    if actual != expected:
        raise RuntimeError(f"{source} is sha256 {actual}, but {LOCK_FILE_NAME} pins {expected} for {target}")

    build_data["tag"] = f"py3-none-{spec['wheel_platform']}"
    build_data["pure_python"] = False
    build_data["infer_tag"] = False
    build_data["force_include"][str(source)] = f"telegram/lib/{spec['bundled_name']}"


class TDLibBinaryBuildHook(BuildHookInterface):  # type: ignore[type-arg]
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        apply_tdlib_target(Path(self.root), build_data)
