FROM akhmetov/tdlib

RUN apk update && apk add python3
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install python-telegram

ADD ./examples/*.py /app/examples/
