FROM python:3.14.6-slim-trixie

RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
