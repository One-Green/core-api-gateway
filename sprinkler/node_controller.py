"""
MQTT based sprinklers controller

Purpose based on tag get confirmation from Redis
Use binary controller take action 0/1 to fill water
Subscribe to MQTT_SENSOR_TOPIC : except InfluxDB line protocol format
Publish to MQTT_CONTROLLER_TOPIC: published dict  {"tag":<>, "signal":<> }

Author: Shanmugathas Vigneswaran
mail: shanmugathas.vigneswaran@outlook.fr
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

import paho.mqtt.client as mqtt
from core.utils import get_now
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_SPRINKLER_SENSOR_TOPIC
from project.settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from tasks import node_controller

BONJOUR: str = f"""
#########################################
## {MQTT_HOST=}
## {MQTT_PORT=}
## {MQTT_SPRINKLER_SENSOR_TOPIC=}
## {MQTT_SPRINKLER_CONTROLLER_TOPIC=}
#########################################
Controller starting 
"""

print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [SPRINKLER] " f"Connected with result code {rc}")
    client.subscribe(MQTT_SPRINKLER_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    """
    accept Influx Line Protocol message
    sprinkler,tag=orchid soil_moisture_raw_adc=100i,soil_moisture=200i
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    print(f"[INFO][MQTT]  Message >> Sprinkler Celery Worker : {msg.payload}")
    node_controller.delay(msg.payload)


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
