FROM python:3.7.1-alpine3.8

RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
