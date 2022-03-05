import os
import json
from datetime import datetime

# Define health check type (can be all / or comma seperated string with
# services to check
HEALTH_CHECK_TYPE = os.getenv("HEALTH_CHECK_TYPE", "all")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "mqtt")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "anyrandompassword")
MQTT_HEALTH_CHECK_TOPIC = os.getenv("MQTT_HEALTH_CHECK_TOPIC", "health/check")

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "anyrandompassword")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

INFLUXDB_HOST = os.getenv("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.getenv("INFLUXDB_PORT", 8086))
DOCKER_INFLUXDB_INIT_ORG = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
DOCKER_INFLUXDB_INIT_BUCKET = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
INFLUXDB_URL = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


def is_mqtt_up():
    import paho.mqtt.client as mqtt

    print("Testing MQTT connexion")
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 1)
    mqtt_client.publish(
        MQTT_HEALTH_CHECK_TOPIC,
        json.dumps({"status": "ok", "utc_datetime": str(datetime.utcnow())}),
    )
    print("MQTT is ok")


def is_pg_up():
    import psycopg2

    print("testing Postgresql connexion")
    psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        connect_timeout=1,
    )
    print("Postgresql is ok")


def is_influxdb_up():
    from influxdb_client import InfluxDBClient

    print("Testing InfluxDB")
    InfluxDBClient(
        url=INFLUXDB_URL,
        token=DOCKER_INFLUXDB_INIT_ADMIN_TOKEN,
        org=DOCKER_INFLUXDB_INIT_ORG,
    ).ready()
    print("InfluxDB is ok")


def is_redis_up():
    from redis.client import Redis

    print("Testing Redis")
    if REDIS_USER and REDIS_PASSWORD:
        Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            username=REDIS_USER,
            password=REDIS_PASSWORD,
            socket_connect_timeout=1,
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
