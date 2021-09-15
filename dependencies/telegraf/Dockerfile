FROM alpine/git as repo-clone
RUN git clone https://github.com/One-Green/core-api-gateway.git /core-api-gateway

FROM telegraf:1.19.3 as runtime
COPY --from=repo-clone core-api-gateway/health_check.py health_check.py

RUN apt update && apt install libpq-dev python3 python3-pip -y
RUN pip3 install psycopg2 paho-mqtt

