FROM python:3.9.6

ENV PYTHONUNBUFFERED TRUE

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT []
