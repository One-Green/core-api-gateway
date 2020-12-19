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
from project.settings import MQTT_USER
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_SENSOR_TOPIC
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
from project.settings import MQTT_WATER_CONTROLLER_TELEGRAF_TOPIC
from project.settings import __repo__
from project.settings import __version__
from sprinkler.models import Sprinklers
from water.dict_def import WaterCtrlDict

CONTROLLED_DEVICE: str = "water"

BONJOUR: str = f'''
#=============================================================================#
#         wWWWw               wWWWw                          _                #
#   vVVVv (___) wWWWw         (___)  vVVVv                  | |               #
#   (___)  ~Y~  (___)  vVVVv   ~Y~   (___)  __      __ __ _ | |_  ___  _ __   #
#    ~Y~   \|    ~Y~   (___)    |/    ~Y~    \ \ /\ / // _` || __|/ _ \| '__| #
#    \|   \ |/   \| /  \~Y~/   \|    \ |/     \ V  V /| (_| || |_|  __/| |    #
#jgs^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   \_/\_/  \__,_| \__|\___||_|    #
#=============================================================================#

{MQTT_HOST=} 
{MQTT_PORT=}
INPUT={MQTT_WATER_SENSOR_TOPIC=}
OUTPUT={MQTT_WATER_CONTROLLER_TOPIC=}
VERSION={__version__}
REPO={__repo__}
Thanks to Joan G. Stark for ascii art https://www.asciiart.eu/plants/flowers

Controller started

'''
print(BONJOUR)


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}")
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

    d: dict = parse_line(msg.payload + b' 0')
    # TODO: Nutrient controller
    # TODO: pH downer controller
    pub_d: dict = WaterCtrlDict(
        water_pump_signal=Sprinklers().is_any_require_water(),
        nutrient_pump_signal=False,
        ph_downer_pump_signal=False
    )
    # TODO: just for testing
    txt = 'weather,location=us-midwest temperature=82'
    print(f"writing >> {txt} ")
    client.publish(
        MQTT_WATER_CONTROLLER_TELEGRAF_TOPIC,
        txt
    )
    client.publish(
        MQTT_WATER_CONTROLLER_TOPIC,
        json.dumps(pub_d)
    )


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
