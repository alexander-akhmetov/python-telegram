FROM python:3.10.0-bullseye

RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
