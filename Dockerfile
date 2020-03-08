FROM python:3.8.1-slim-buster

RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
