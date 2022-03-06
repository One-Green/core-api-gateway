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
from project.settings import MQTT_WATER_SENSOR_TOPIC
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
from project.settings import __repo__
from project.settings import __version__
from water.tasks import node_controller

CONTROLLED_DEVICE: str = "water"

BONJOUR: str = f"""
  ___  _ __   ___        __ _ _ __ ___  ___ _ __   (_) ___  
 / _ \| '_ \ / _ \_____ / _` | '__/ _ \/ _ \ '_ \  | |/ _ \ 
| (_) | | | |  __/_____| (_| | | |  __/  __/ | | |_| | (_) |
 \___/|_| |_|\___|      \__, |_|  \___|\___|_| |_(_)_|\___/ 
                        |___/                               
{MQTT_HOST=} 
{MQTT_PORT=}
{MQTT_WATER_SENSOR_TOPIC=}
{MQTT_WATER_CONTROLLER_TOPIC=}/<water-tag>
VERSION={__version__}
REPO={__repo__}
---------------------------------------------
Starting controller {CONTROLLED_DEVICE} ...
---------------------------------------------
"""
print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(
        f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}"
    )
    client.subscribe(MQTT_WATER_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    """
    Water supply pump I/O  callback
    Nutrient supply pump I/O callback
    pH down supply pump I/O callback
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    print(f"[INFO][MQTT]  Message >> Water Celery Worker : {msg.payload}")
    node_controller.delay(msg.payload)


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
