#!/usr/bin/env python3
"""
Loads the real libtdjson and runs one synchronous request against it.

No network, no credentials, no api_id. It proves the whole ctypes surface: the
CDLL load (architecture, glibc, OpenSSL), the client lifecycle and the
deprecated td_json_client_execute / td_set_log_* symbols this library binds.

    python scripts/smoke_test.py [/path/to/libtdjson.so]

Run it from outside the repository when checking an installed wheel, otherwise
the working tree's telegram/ package shadows the installed one.
"""

from __future__ import annotations

import sys

from telegram.tdjson import TDJson

TEXT = "@telegram /test_command https://telegram.org"
EXPECTED_ENTITY_TYPES = {"textEntityTypeMention", "textEntityTypeBotCommand", "textEntityTypeUrl"}


def smoke_test(library_path: str | None = None) -> None:
    tdjson = TDJson(library_path=library_path, verbosity=0)

    try:
        result = tdjson.td_execute({"@type": "getTextEntities", "text": TEXT})
    finally:
        tdjson.stop()

    if result is None or result.get("@type") != "textEntities":
        raise AssertionError(f"getTextEntities returned {result!r}")

    entity_types = {entity["type"]["@type"] for entity in result["entities"]}

    if entity_types != EXPECTED_ENTITY_TYPES:
        raise AssertionError(f"getTextEntities found {sorted(entity_types)}, expected {sorted(EXPECTED_ENTITY_TYPES)}")


if __name__ == "__main__":
    smoke_test(sys.argv[1] if len(sys.argv) > 1 else None)
    print("libtdjson loads and answers getTextEntities")
