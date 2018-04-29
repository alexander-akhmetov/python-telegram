# Changelog

## [0.3.1] - 2018-04-29

- Logging level in the examples changed to `INFO`.
- Added new `Makefile` command: `docker-echo-bot`.
- All `docker-` commands in the `Makefile` now mount `/tmp/` from host machine to store tdlib's files.

## [0.3.0] - 2018-04-28

- Added `Dockerfile` and `Makefile` with some examples.
- Changed directory for tdlib files to `/tmp/.tdlib_files_{self.phone}/`.
