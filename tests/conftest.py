"""Puts scripts/ on sys.path so the release scripts can be imported as modules."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
