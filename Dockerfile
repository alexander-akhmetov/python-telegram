FROM python:3.12.4-slim-bullseye

RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
