FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc python3-dev g++ make libffi-dev

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

RUN mkdir -p /src
COPY src /src/
COPY tests /tests/

WORKDIR /src

CMD uvicorn main:app --host 0.0.0.0 --port 80