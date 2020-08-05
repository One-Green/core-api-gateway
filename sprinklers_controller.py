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
import time
import pickle
import json
import paho.mqtt.client as mqtt
from core.utils import get_now
from core.controller_default_config import WATER_CONTROLLER
from settings import (
    REDIS_HOST, REDIS_PORT,
    MQTT_HOST, MQTT_PORT
)
from core.registry import REDIS_SPRINKLER_REGISTRY_KEY
from core.controller_default_config import SPRINKLER
from core.pk_dict import SprinklerCtrlDict
from core.controller import BinaryController

CONTROLLED_DEVICE: str = "sprinklers"

REDIS_CONTROLLER_CONFIG_KEY: str = f"{CONTROLLED_DEVICE}_config"
REDIS_CONTROLLER_SIGNAL_KEY_TEMPLATE: str = 'sprinkler_tag_eq_{tag}'
DEFAULT_CONFIG: dict = WATER_CONTROLLER

MQTT_SENSOR_TOPIC: str = f'{CONTROLLED_DEVICE}/sensor'
MQTT_CONTROLLER_TOPIC: str = f'{CONTROLLED_DEVICE}/controller'

BONJOUR: str = f'''
#########################################
## {REDIS_HOST=}
## {REDIS_PORT=}
## {REDIS_CONTROLLER_CONFIG_KEY=}
#########################################
## {MQTT_HOST=}
## {MQTT_PORT=}
## {MQTT_SENSOR_TOPIC=}
## {MQTT_CONTROLLER_TOPIC=}
#########################################
Controller starting 
'''

print(BONJOUR)
time.sleep(2)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def is_tag_in_registry(tag):
    """
    Check if sprinkler is registered
    :param tag:
    :return:
    """
    try:
        registry: dict = json.loads(
            redis_client.get(
                REDIS_SPRINKLER_REGISTRY_KEY
            )
        )
        if tag in registry['tag_list']:
            return True
    except KeyError:
        return False
    except TypeError:
        return False


def get_config(tag):
    """
    Get sprinkler configuration
    :param tag:
    :return:
    """
    try:
        registry: dict = json.loads(
            redis_client.get(
                REDIS_CONTROLLER_CONFIG_KEY
            )
        )
        return registry[tag]
    except KeyError:
        return SPRINKLER
    except TypeError:
        return SPRINKLER


def persist_signal(tag: str, signal: int):
    """
    Persist controller signal to Redis
    :param tag:
    :param signal:
    :return:
    """
    redis_client.set(
        REDIS_CONTROLLER_SIGNAL_KEY_TEMPLATE.format(tag=tag),
        signal
    )


def on_connect(client, userdata, flags, rc):
    print(
        f"[{get_now()}] [MQTT] [OK] "
        f"[{CONTROLLED_DEVICE}] "
        f"Connected with result code {rc}"
    )
    client.subscribe(MQTT_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    d: dict = json.loads(msg.payload)
    tag: str = d['tag']
    if is_tag_in_registry(tag):
        config: dict = get_config(tag)
        ctl = BinaryController()
        ctl.set_conf(
            _min=config["soil_moisture"]['min_level'],
            _max=config["soil_moisture"]['max_level'],
            reverse=False,
        )
        signal = ctl.get_signal(d['soil_moisture'])
        client.publish(
            MQTT_CONTROLLER_TOPIC,
            json.dumps(
                SprinklerCtrlDict(
                    tag=tag,
                    signal=bool(signal)
                )
            )
        )
        persist_signal(tag, signal)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
