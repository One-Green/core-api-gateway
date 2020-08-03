"""
Handle Sprinkler Node registration based on tag

author : Shanmugathas Vigneswaran
mail: shanmugathas.vigneswaran@outlook.fr
"""
import redis
import time
import json
import pickle
import paho.mqtt.client as mqtt
from core.utils import get_now
from registry import REDIS_SPRINKLER_REGISTRY_KEY
from settings import (
    REDIS_HOST, REDIS_PORT,
    MQTT_HOST, MQTT_PORT
)

MQTT_ADMISSION_TOPIC: str = f'config/sprinkler/admission'
MQTT_ADMISSION_VALIDATION_TOPIC_TEMPLATE: str = 'config/sprinkler/admission/validation/{tag}'

BONJOUR: str = f'''
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   Sprinkler Node admission controller  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
Purpose: Register from MQTT topic new Sprinkler TAG to Redis if not exist.
         Response 1 to Node if registered
         Response 0 to Node if TAG already exist 
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   Settings   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
{REDIS_HOST=}
{REDIS_PORT=}
-------------
{MQTT_HOST=}
{MQTT_PORT=}
{MQTT_ADMISSION_TOPIC=} 
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
'''

print(BONJOUR)
time.sleep(2)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
controller_config = redis_client.get(REDIS_SPRINKLER_REGISTRY_KEY)


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] Connected with result code {rc}")
    client.subscribe(MQTT_ADMISSION_TOPIC)


def on_message(client, userdata, msg):
    """
    1/ Read message
    2/ Parse json to dict
    3/ Check if tag exist in Redis
        3.1/ If not exist append -> return registered
        3.2/ If already exist -> return error, already exist
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    print(f"[{get_now()}] [MQTT] [INFO] New message received {msg.payload=}")
    d = json.loads(msg.payload)
    tag = d['tag']
    print(
        f"[{get_now()}] [MQTT] [INFO] "
        f"New Sprinkler with {tag=} "
        f"wan't to register ..."
    )

    try:
        registry: dict = pickle.loads(
            redis_client.get(
                REDIS_SPRINKLER_REGISTRY_KEY
            )
        )
    except:
        registry = {
            'tag_list': []
        }

    if tag not in registry['tag_list']:
        # 1/ Append tag
        registry['tag_list'].append(tag)
        # 2/ Save to Redis
        redis_client.set(
            REDIS_SPRINKLER_REGISTRY_KEY,
            pickle.dumps(registry)
        )
        # 3/ Publish (1) to topic "config/sprinkler/registry/validation/{tag}"
        client.publish(
            MQTT_ADMISSION_VALIDATION_TOPIC_TEMPLATE.format(tag=tag),
            1
        )

        print(
            f"[{get_now()}] [MQTT] [OK] "
            f"New Sprinkler with {tag=} "
            f"if registered successfully => {registry=}"
        )
    else:
        # Tag is already exist
        # Publish (0) to topic "config/sprinkler/registry/validation/{tag}"
        client.publish(
            MQTT_ADMISSION_VALIDATION_TOPIC_TEMPLATE.format(tag=tag),
            0
        )
        print(
            f"[{get_now()}] [MQTT] [ERROR] "
            f"New Sprinkler with {tag=} "
            f"not registered, tag already in Redis => {registry=} ! "
        )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()
