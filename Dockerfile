FROM python:3.14.6-slim-trixie

# --only-binary: without it pip falls back to the binary-free sdist and the
# image ships an install that raises TDLibNotFoundError on first use.
RUN python3 -m pip install --only-binary=:all: python-telegram

ADD ./examples/*.py /app/examples/
