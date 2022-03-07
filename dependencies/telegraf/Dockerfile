FROM alpine/git as repo-clone
RUN git clone https://github.com/One-Green/core-api-gateway.git /core-api-gateway

FROM telegraf:1.20.4-alpine as runtime
COPY --from=repo-clone core-api-gateway/health_check.py health_check.py

RUN apk  add python3 py3-pip
RUN pip3 install paho-mqtt influxdb-client
