"""
Loads a real libtdjson, which every other test mocks away.

Skips when no library can be resolved, so a checkout with no bundled binary and
no system tdlib still runs a green suite.
"""

import pytest
from smoke_test import smoke_test

from telegram.tdjson import TDLibNotFoundError, _resolve_tdjson_library


def test_real_library_answers_get_text_entities():
    try:
        library_path, source = _resolve_tdjson_library()
    except TDLibNotFoundError as error:
        pytest.skip(str(error))

    print(f"using {library_path} ({source})")
    smoke_test(library_path)
