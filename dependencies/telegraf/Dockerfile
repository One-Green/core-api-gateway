FROM telegraf:1.19.3

COPY health_check.py health_check.py

RUN apt update && apt install libpq-dev python python-pip -y
RUN pip install psycopg2 paho-mqtt

