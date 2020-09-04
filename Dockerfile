FROM python:3.8.5

ENV PYTHONUNBUFFERED TRUE

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT []
