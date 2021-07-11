import redis
import time
import pickle
import json
import paho.mqtt.client as mqtt
from core.controller_default_config import WATER_CONTROLLER
from settings import REDIS_HOST, REDIS_PORT, MQTT_HOST, MQTT_PORT
from core.registry import REDIS_SPRINKLER_REGISTRY_KEY
import _pickle

_list = _pickle.load(open("sign_list.pkl", "rb"))

tag_list = ["tag-1", "tag-2", "tag-3", "tag-4", "tag-5"]


CONTROLLED_DEVICE: str = "sprinklers"

REDIS_CONTROLLER_CONFIG_KEY: str = f"{CONTROLLED_DEVICE}_config"
DEFAULT_CONFIG: dict = WATER_CONTROLLER

MQTT_SENSOR_TOPIC: str = f"{CONTROLLED_DEVICE}/sensor"
MQTT_CONTROLLER_TOPIC: str = f"{CONTROLLED_DEVICE}/controller"
MQTT_ADMISSION_TOPIC: str = f"config/sprinkler/admission"
MQTT_ADMISSION_VALIDATION_TOPIC_TEMPLATE: str = (
    "config/sprinkler/admission/validation/{tag}"
)


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
redis_client.delete(REDIS_SPRINKLER_REGISTRY_KEY)
registry = {"tag_list": tag_list}
redis_client.set(REDIS_SPRINKLER_REGISTRY_KEY, json.dumps(registry))

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

while True:
    for i in tag_list:
        for j in _list:
            mqtt_client.publish(
                MQTT_SENSOR_TOPIC, json.dumps({"tag": i, "soil_moisture": j * 100})
            )
            time.sleep(0.5)
    time.sleep(1)
