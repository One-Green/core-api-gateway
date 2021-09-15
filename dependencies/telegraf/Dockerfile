FROM telegraf:1.19.3

COPY health_check.py health_check.py

RUN apt update && apt install libpq-dev python3 python3-pip -y
RUN pip3 install psycopg2 paho-mqtt

