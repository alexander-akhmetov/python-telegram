FROM python:3.6.5-alpine3.7

RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
