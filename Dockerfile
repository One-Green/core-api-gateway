FROM python:3.10.2

ENV PYTHONUNBUFFERED TRUE

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT []
