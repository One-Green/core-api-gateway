# test
FROM python:3.10.2-alpine3.15 as builder
WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk --no-cache add g++ cargo patchelf
RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 --no-cache-dir install -r /app/requirements.txt --target=/py-dependencies --no-dependencies

FROM python:3.10.2-alpine3.15 as run
WORKDIR /app

COPY . /app
COPY --from=builder /py-dependencies /py-dependencies
ENV PYTHONPATH="${PYTHONPATH}:/py-dependencies"

CMD []
ENTRYPOINT []
