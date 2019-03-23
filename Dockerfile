FROM python:3.7.2-alpine3.9

RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install python-telegram

RUN apk add --no-cache openssl libstdc++

ADD ./examples/*.py /app/examples/
