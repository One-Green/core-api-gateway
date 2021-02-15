"""
MQTT based light controller
Use Time controller take action on/off light
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

from datetime import time
from django.core.exceptions import ObjectDoesNotExist
import orjson as json
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.utils import get_now
from core.controller import TimeRangeController
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USER
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_LIGHT_TOPIC
from project.settings import MQTT_LIGHT_CONTROLLER_TOPIC
from light.models import Light
from light.dict_def import LightCtrlDict

BONJOUR: str = f'''
#########################################
## {MQTT_HOST=}
## {MQTT_PORT=}
## {MQTT_LIGHT_TOPIC=}
## {MQTT_LIGHT_CONTROLLER_TOPIC=}
#########################################
Controller starting 
'''

print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(
        f"[{get_now()}] [MQTT] [LIGHT] "
        f"Connected with result code {rc}"
    )
    client.subscribe(MQTT_LIGHT_TOPIC)


def on_message(client, userdata, msg):
    d: dict = parse_line(msg.payload + b' 0')
    tag: str = d['tags']['tag']
    light = Light()
    ctl = TimeRangeController()
    try:
        light.get_config(tag)
    except ObjectDoesNotExist:
        light.update_config(
            tag=tag,
            on_time_at=time(hour=9, minute=0, second=0),
            off_time_at=time(hour=18, minute=0, second=0)
        )
        light.get_config(tag)
    ctl.set_conf(
        start_at=light.on_time_at,
        end_at=light.off_time_at,
    )
    signal = ctl.get_signal()

    light.update_controller(
        tag=tag,
        light_signal=bool(signal)
    )

    client.publish(
        MQTT_LIGHT_CONTROLLER_TOPIC,
        json.dumps(
            LightCtrlDict(
                controller_type="light",
                tag=tag,
                on_time_at="",
                off_time_at="",
                light_signal=bool(signal)
            )
        )
    )


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
