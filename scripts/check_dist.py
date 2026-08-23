#!/usr/bin/env python3
"""
Checks a built dist/ before anything irreversible happens to it.

    python scripts/check_dist.py <tag> [dist_dir]

Every distribution must carry the tag's version, the wheel tags must be exactly
the ones tdlib.lock describes, and none of them may be py3-none-any: pip would
install a pure wheel on any platform the four do not cover and it would raise
on first use.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from packaging.utils import parse_sdist_filename, parse_wheel_filename
from packaging.version import Version

ROOT = Path(__file__).parent.parent


def expected_wheel_tags() -> set[str]:
    lock = json.loads((ROOT / "tdlib.lock").read_text())

    return {f"py3-none-{spec['wheel_platform']}" for spec in lock["targets"].values()}


def check_dist(tag: str, dist_dir: Path) -> list[str]:
    errors = []
    wheel_tags = set()
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    wheels = sorted(dist_dir.glob("*.whl"))

    for sdist in sdists:
        _, version = parse_sdist_filename(sdist.name)

        if version != Version(tag):
            errors.append(f"{sdist.name} is version {version}, tag is {tag}")

    for wheel in wheels:
        _, version, _, tags = parse_wheel_filename(wheel.name)

        if version != Version(tag):
            errors.append(f"{wheel.name} is version {version}, tag is {tag}")

        for parsed in tags:
            if parsed.platform == "any":
                errors.append(f"{wheel.name} is a pure wheel; pip would install it where no binary works")

            wheel_tags.add(str(parsed))

    if len(sdists) != 1:
        errors.append(f"expected exactly one sdist, found {len(sdists)}")

    expected = expected_wheel_tags()

    if wheel_tags != expected:
        errors.append(f"wheel tags are {sorted(wheel_tags)}, tdlib.lock expects {sorted(expected)}")

    return errors


def main() -> int:
    tag = sys.argv[1]
    dist_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "dist")
    errors = check_dist(tag, dist_dir)

    for error in errors:
        print(f"::error::{error}")

    if errors:
        return 1

    print(f"dist/ holds one sdist and {len(expected_wheel_tags())} platform wheels at version {tag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
