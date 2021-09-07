FROM telegraf:1.19.3

COPY health_check.py /tools/health_check.py

RUN apk add python python-pip
RUN pip install psycopg2 paho-mqtt

