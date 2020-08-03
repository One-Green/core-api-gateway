import os
import redis
import time
import pickle
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from core.utils import get_now
from random import randint
from pprint import pprint
from controller_default_config import WATER_CONTROLLER
from settings import (
    REDIS_HOST, REDIS_PORT,
    MQTT_HOST, MQTT_PORT
)
from registry import REDIS_SPRINKLER_REGISTRY_KEY
CONTROLLED_DEVICE: str = "water"

REDIS_CONTROLLER_CONFIG_KEY: str = f"{CONTROLLED_DEVICE}_config"
DEFAULT_CONFIG: dict = WATER_CONTROLLER

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
MM {REDIS_HOST=}
MM {REDIS_PORT=}
MM {REDIS_CONTROLLER_CONFIG_KEY=}
MM
MM -------------
MM
MM {MQTT_HOST=}
MM {MQTT_PORT=}
MM {MQTT_SENSOR_TOPIC=}
MM {MQTT_CONTROLLER_TOPIC=}
MM
MM ------------

Controller starting 
'''

print(BONJOUR)
time.sleep(2)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
controller_config = redis_client.get(REDIS_CONTROLLER_CONFIG_KEY)
if not controller_config:
    print(
        f"[{get_now()}] [REDIS] [ERROR] [{CONTROLLED_DEVICE}]"
        f" Cannot find configuration for key {REDIS_CONTROLLER_CONFIG_KEY=}"
    )
    redis_client.get(REDIS_CONTROLLER_CONFIG_KEY)
    redis_client.set(
        REDIS_CONTROLLER_CONFIG_KEY,
        pickle.dumps(DEFAULT_CONFIG)
    )
    print(
        f"[{get_now()}] [REDIS] [{CONTROLLED_DEVICE}]"
        f" Using default configuration"
    )
    pprint(
        pickle.loads(
            redis_client.get(
                REDIS_CONTROLLER_CONFIG_KEY
            )
        )
    )


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}")
    client.subscribe(MQTT_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    sprinkler_reg: dict = pickle.loads(
        redis_client.get(
            REDIS_SPRINKLER_REGISTRY_KEY
        )
    )
    water_config: dict = pickle.loads(
        redis_client.get(
            REDIS_CONTROLLER_CONFIG_KEY
        )
    )

    client.publish(MQTT_CONTROLLER_TOPIC, randint(0, 100))


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()
