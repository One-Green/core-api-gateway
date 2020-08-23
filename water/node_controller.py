import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

import orjson as json
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.utils import get_now
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from sprinkler.models import Sprinklers
from water.dict_def import WaterCtrlDict

CONTROLLED_DEVICE: str = "water"
MQTT_SENSOR_TOPIC: str = f'{CONTROLLED_DEVICE}/sensor'
MQTT_CONTROLLER_TOPIC: str = f'{CONTROLLED_DEVICE}/controller'


BONJOUR: str = f'''
M""MMM""MMM""M MMP"""""""MM M""""""""M MM""""""""`M MM"""""""`MM          MM'""""'YMM M""""""""M M""MMMMMMMM 
M  MMM  MMM  M M' .mmmm  MM Mmmm  mmmM MM  mmmmmmmM MM  mmmm,  M          M' .mmm. `M Mmmm  mmmM M  MMMMMMMM 
M  MMP  MMP  M M         `M MMMM  MMMM M`      MMMM M'        .M          M  MMMMMooM MMMM  MMMM M  MMMMMMMM 
M  MM'  MM' .M M  MMMMM  MM MMMM  MMMM MM  MMMMMMMM MM  MMMb. "M 88888888 M  MMMMMMMM MMMM  MMMM M  MMMMMMMM 
M  `' . '' .MM M  MMMMM  MM MMMM  MMMM MM  MMMMMMMM MM  MMMMM  M          M. `MMM' .M MMMM  MMMM M  MMMMMMMM 
M    .d  .dMMM M  MMMMM  MM MMMM  MMMM MM        .M MM  MMMMM  M          MM.     .dM MMMM  MMMM M         M 
MMMMMMMMMMMMMM MMMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMMM MMMMMMMMMMMM          MMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMM 
MM
MM {MQTT_HOST=}
MM {MQTT_PORT=}
MM {MQTT_SENSOR_TOPIC=}
MM {MQTT_CONTROLLER_TOPIC=}
MM ------------
Controller starting 
'''
print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}")
    client.subscribe(MQTT_SENSOR_TOPIC)


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

    d: dict = parse_line(msg.payload + b' 0')
    # TODO: Nutrient controller
    # TODO: pH downer controller
    pub_d: dict = WaterCtrlDict(
        water_pump_signal=Sprinklers().is_any_require_water(),
        nutrient_pump_signal=False,
        ph_downer_pump_signal=False
        )
    client.publish(
        MQTT_CONTROLLER_TOPIC,
        json.dumps(pub_d)
    )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
