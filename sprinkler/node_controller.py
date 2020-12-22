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

from django.core.exceptions import ObjectDoesNotExist
import orjson as json
import paho.mqtt.client as mqtt
from influxdb_client import Point
from line_protocol_parser import parse_line
from core.utils import get_now
from core.controller import BinaryController
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USER
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_SPRINKLER_SENSOR_TOPIC
from project.settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from sprinkler.models import Sprinklers
from sprinkler.dict_def import SprinklerCtrlDict

BONJOUR: str = f'''
#########################################
## {MQTT_HOST=}
## {MQTT_PORT=}
## {MQTT_SPRINKLER_SENSOR_TOPIC=}
## {MQTT_SPRINKLER_CONTROLLER_TOPIC=}
#########################################
Controller starting 
'''

print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(
        f"[{get_now()}] [MQTT] [SPRINKLER] "
        f"Connected with result code {rc}"
    )
    client.subscribe(MQTT_SPRINKLER_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    d: dict = parse_line(msg.payload + b' 0')
    tag: str = d['tags']['tag']
    s = Sprinklers()
    ctl = BinaryController()
    try:
        s.get_config(tag)
    except ObjectDoesNotExist:
        s.update_config(
            tag=tag,
            soil_moisture_min_level=30,
            soil_moisture_max_level=70
        )
        s.get_config(tag)
    ctl.set_conf(
        _min=s.soil_moisture_min_level,
        _max=s.soil_moisture_max_level,
        reverse=False
    )
    signal = ctl.get_signal(
        d['fields']['soil_moisture']
    )
    s.update_controller(
        tag=tag,
        water_valve_signal=bool(signal)
    )

    client.publish(
        MQTT_SPRINKLER_CONTROLLER_TOPIC,
        json.dumps(
            SprinklerCtrlDict(
                controller_type="sprinkler",
                tag=tag,
                water_valve_signal=bool(signal),
                soil_moisture_min_level=s.soil_moisture_min_level,
                soil_moisture_max_level=s.soil_moisture_max_level,
            )
        )
    )


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
