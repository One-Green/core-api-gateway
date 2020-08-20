"""
MQTT based sprinklers controller

Purpose based on tag get confirmation from Redis
Use binary controller take action 0/1 to fill water
Subscribe to MQTT_SENSOR_TOPIC : excepted dict {"tag":<>, "soil_humidity":<> }
Publish to MQTT_CONTROLLER_TOPIC: published dict  {"tag":<>, "signal":<> }

Author: Shanmugathas Vigneswara
mail: shanmugathas.vigneswaran@outlook.fr
"""
import redis
import json
import rom
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.utils import get_now
from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import MQTT_HOST
from settings import MQTT_PORT
from settings import MQTT_SPRINKLER_SENSOR_TOPIC
from settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from core.pk_rom.sprinkler import Sprinklers
from core.pk_dict import SprinklerCtrlDict
from core.controller import BinaryController


BONJOUR: str = f'''
#########################################
## {REDIS_HOST=}
## {REDIS_PORT=}
#########################################
## {MQTT_HOST=}
## {MQTT_PORT=}
## {MQTT_SPRINKLER_SENSOR_TOPIC=}
## {MQTT_SPRINKLER_CONTROLLER_TOPIC=}
#########################################
Controller starting 
'''

print(BONJOUR)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
rom.util.set_connection_settings(host=REDIS_HOST, port=REDIS_PORT, db=0)


def on_connect(client, userdata, flags, rc):
    print(
        f"[{get_now()}] [MQTT] [SPRINKLER] "
        f"Connected with result code {rc}"
    )
    client.subscribe(MQTT_SPRINKLER_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    d: dict = parse_line(msg.payload)
    tag: str = d['tags']['tag']
    s = Sprinklers()
    ctl = BinaryController()
    try:
        s.get_config(tag)
    except AttributeError:
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
                tag=tag,
                water_valve_signal=bool(signal)
            )
        )
    )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
