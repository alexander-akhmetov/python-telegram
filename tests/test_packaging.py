"""
Covers hatch_build.py and scripts/check_dist.py, which nothing else runs: both
only execute during a release, and a silent failure there ships a wheel with no
binary or one pip installs where it cannot work.
"""

import hashlib
import json
from pathlib import Path

import pytest
from check_dist import check_dist, expected_wheel_tags

from hatch_build import LOCK_FILE_NAME, SOURCE_DIR_ENV_VAR, TARGET_ENV_VAR, apply_tdlib_target

ROOT = Path(__file__).parent.parent
TARGET = "macos-arm64"


@pytest.fixture
def lock_root(tmp_path):
    """A repo root whose tdlib.lock pins one target, with the asset next to it."""
    binary = tmp_path / "tdlib" / "libtdjson-macos-arm64.dylib"
    binary.parent.mkdir()
    binary.write_bytes(b"not really a dylib")

    lock = {
        "release_tag": "v1.8.66",
        "targets": {
            TARGET: {
                "asset": binary.name,
                "bundled_name": "libtdjson.dylib",
                "wheel_platform": "macosx_11_0_arm64",
                "sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
            }
        },
    }
    (tmp_path / LOCK_FILE_NAME).write_text(json.dumps(lock))

    return tmp_path


@pytest.fixture
def build_data():
    return {"force_include": {}}


def _set_target(monkeypatch, root, target=TARGET):
    monkeypatch.setenv(TARGET_ENV_VAR, target)
    monkeypatch.setenv(SOURCE_DIR_ENV_VAR, str(root / "tdlib"))


def test_no_target_leaves_the_wheel_pure(monkeypatch, build_data):
    monkeypatch.delenv(TARGET_ENV_VAR, raising=False)

    apply_tdlib_target(ROOT, build_data)

    assert build_data == {"force_include": {}}


def test_valid_target_retags_the_wheel_and_bundles_the_binary(monkeypatch, lock_root, build_data):
    _set_target(monkeypatch, lock_root)
    binary = lock_root / "tdlib" / "libtdjson-macos-arm64.dylib"

    apply_tdlib_target(lock_root, build_data)

    assert build_data["tag"] == "py3-none-macosx_11_0_arm64"
    assert build_data["pure_python"] is False
    assert build_data["infer_tag"] is False
    assert build_data["force_include"] == {str(binary): "telegram/lib/libtdjson.dylib"}


def test_checksum_mismatch_raises(monkeypatch, lock_root, build_data):
    _set_target(monkeypatch, lock_root)
    (lock_root / "tdlib" / "libtdjson-macos-arm64.dylib").write_bytes(b"a different binary")

    with pytest.raises(RuntimeError, match="pins"):
        apply_tdlib_target(lock_root, build_data)


def test_unknown_target_raises(monkeypatch, lock_root, build_data):
    _set_target(monkeypatch, lock_root, target="solaris-sparc")

    with pytest.raises(RuntimeError, match="solaris-sparc"):
        apply_tdlib_target(lock_root, build_data)


def test_missing_binary_raises(monkeypatch, lock_root, build_data):
    _set_target(monkeypatch, lock_root)
    (lock_root / "tdlib" / "libtdjson-macos-arm64.dylib").unlink()

    with pytest.raises(RuntimeError, match="does not exist"):
        apply_tdlib_target(lock_root, build_data)


def test_placeholder_checksum_raises(monkeypatch, lock_root, build_data):
    lock = json.loads((lock_root / LOCK_FILE_NAME).read_text())
    lock["targets"][TARGET]["sha256"] = "pending"
    (lock_root / LOCK_FILE_NAME).write_text(json.dumps(lock))
    _set_target(monkeypatch, lock_root)

    with pytest.raises(RuntimeError, match="has no sha256"):
        apply_tdlib_target(lock_root, build_data)


def test_every_shipped_lock_target_is_complete():
    """The committed lock is what the release workflow builds from."""
    lock = json.loads((ROOT / LOCK_FILE_NAME).read_text())

    assert set(lock["targets"]) == {"linux-x86_64", "linux-aarch64", "macos-arm64", "macos-x86_64"}

    for target, spec in lock["targets"].items():
        assert set(spec) >= {"asset", "bundled_name", "wheel_platform", "sha256"}, target
        assert spec["bundled_name"] in {"libtdjson.so", "libtdjson.dylib"}, target


@pytest.fixture
def built_dist(tmp_path):
    """A dist/ holding the sdist and every wheel tdlib.lock names."""
    (tmp_path / "python_telegram-1.1.0.tar.gz").touch()

    for tag in expected_wheel_tags():
        (tmp_path / f"python_telegram-1.1.0-{tag}.whl").touch()

    return tmp_path


def test_a_complete_dist_passes(built_dist):
    assert check_dist("1.1.0", built_dist) == []


def test_a_prerelease_tag_matches_its_normalized_filename(tmp_path):
    """PEP 440 normalizes a 1.1.0-rc1 tag to 1.1.0rc1 in the filename."""
    (tmp_path / "python_telegram-1.1.0rc1.tar.gz").touch()

    for tag in expected_wheel_tags():
        (tmp_path / f"python_telegram-1.1.0rc1-{tag}.whl").touch()

    assert check_dist("1.1.0-rc1", tmp_path) == []


def test_a_version_that_is_not_the_tag_is_rejected(built_dist):
    errors = check_dist("1.2.0", built_dist)

    assert len(errors) == 1 + len(expected_wheel_tags())
    assert all("tag is 1.2.0" in error for error in errors)


def test_a_pure_wheel_is_rejected(built_dist):
    (built_dist / "python_telegram-1.1.0-py3-none-any.whl").touch()

    errors = check_dist("1.1.0", built_dist)

    assert any("pure wheel" in error for error in errors)


def test_a_missing_wheel_is_rejected(built_dist):
    next(built_dist.glob("*macosx_11_0_arm64.whl")).unlink()

    errors = check_dist("1.1.0", built_dist)

    assert any("tdlib.lock expects" in error for error in errors)


def test_a_missing_sdist_is_rejected(built_dist):
    (built_dist / "python_telegram-1.1.0.tar.gz").unlink()

    errors = check_dist("1.1.0", built_dist)

    assert any("exactly one sdist" in error for error in errors)
