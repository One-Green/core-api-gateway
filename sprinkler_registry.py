"""
Handle Sprinkler Node registration based on tag

author : Shanmugathas Vigneswaran
mail: shanmugathas.vigneswaran@outlook.fr
"""
import redis
import json
import rom
import paho.mqtt.client as mqtt
from core.utils import get_now
from core.pk_rom.sprinkler import Sprinklers
from settings import (
    REDIS_HOST,
    REDIS_PORT,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_SPRINKLER_REGISTRY_TOPIC,
    MQTT_SPRINKLER_REGISTRY_VALIDATION_TOPIC_TEMPLATE
)

BONJOUR: str = f'''
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM      Sprinkler Node registry         MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
Purpose: Register from MQTT topic new Sprinkler TAG to Redis if not exist.
         Response 1 to Node if registered
         Response 0 to Node if TAG already exist 
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   Settings   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
{REDIS_HOST=}
{REDIS_PORT=}
-------------
{MQTT_HOST=}
{MQTT_PORT=}
{MQTT_SPRINKLER_REGISTRY_TOPIC=} 
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
'''
print(BONJOUR)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
rom.util.set_connection_settings(host=REDIS_HOST, port=REDIS_PORT, db=0)


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] Connected with result code {rc}")
    client.subscribe(MQTT_SPRINKLER_REGISTRY_TOPIC)


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
    if Sprinklers().is_tag_in_registry(tag):
        # Tag is already exist
        r = {"acknowledge": False}
        # 3/ Publish (1) to topic "sprinkler/config/registry/validation/{tag}"
        client.publish(
            MQTT_SPRINKLER_REGISTRY_VALIDATION_TOPIC_TEMPLATE.format(tag=tag),
            json.dumps(r)
        )
        print(
            f"[{get_now()}] [MQTT] [WARNING] "
            f"This tag {tag=} is already in registry"
        )
    else:
        r = {"acknowledge": True}
        # Publish (0) to topic "sprinkler/config/registry/validation/{tag}"
        client.publish(
            MQTT_SPRINKLER_REGISTRY_VALIDATION_TOPIC_TEMPLATE.format(tag=tag),
            json.dumps(r)
        )
        Sprinklers().add_tag_in_registry(tag)
        print(
            f"[{get_now()}] [MQTT] [OK] "
            f"New Sprinkler with {tag=} "
        )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
