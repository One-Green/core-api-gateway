import os
import json
import requests
from datetime import datetime
import paho.mqtt.client as mqtt
import psycopg2
from redis.client import Redis

# Define health check type (can be all / or comma seperated string with
# services to check
HEALTH_CHECK_TYPE = os.getenv("HEALTH_CHECK_TYPE", "all")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "mqtt")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "anyrandompassword")
MQTT_HEALTH_CHECK_TOPIC = os.getenv("MQTT_HEALTH_CHECK_TOPIC", "health/check")

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "anyrandompassword")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

INFLUXDB_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.getenv("INFLUXDB_PORT", 8086))

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


def is_mqtt_up():
    print("Testing MQTT connexion")
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 1)
    mqtt_client.publish(
        MQTT_HEALTH_CHECK_TOPIC,
        json.dumps(
            {
                "status": "ok",
                "utc_datetime": str(datetime.utcnow())
            }
                   )
    )
    print("MQTT is ok")


def is_pg_up():
    print("testing Postgresql connexion")
    con = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        connect_timeout=1
    )
    print("Postgresql is ok")


def is_influxdb_up():
    print("Testing Influxdb")
    r = requests.get(f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}", timeout=1)
    print("Influx db is ok")


def is_redis_up():
    print("Testing Redis")
    if REDIS_USER and REDIS_PASSWORD:
        Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            username=REDIS_USER,
            password=REDIS_PASSWORD,
            socket_connect_timeout=1
        ).ping()
    Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=1).ping()
    print("Redis is ok")


if __name__ == "__main__":
    if HEALTH_CHECK_TYPE.lower().strip() == "all":
        is_mqtt_up()
        is_pg_up()
        is_influxdb_up()
        is_redis_up()
    else:
        for _ in HEALTH_CHECK_TYPE.lower().split(","):
            if "mqtt" in _:
                is_mqtt_up()
            if "pg" in _:
                is_pg_up()
            if "influxdb" in _:
                is_influxdb_up()
            if "redis" in _:
                is_redis_up()
