FROM python:3.10.2-alpine3.15 as run

ENV PYTHONUNBUFFERED TRUE

COPY . /app

RUN apk --no-cache add g++ \
    && pip3 --no-cache-dir install --upgrade pip \
    && pip3 --no-cache-dir install -r /app/requirements.txt

ENTRYPOINT []
