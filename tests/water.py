import time
from random import randint
import json
import paho.mqtt.client as mqtt
from settings import (
    MQTT_HOST, MQTT_PORT
)

CONTROLLED_DEVICE: str = "water"
MQTT_SENSOR_TOPIC: str = f'{CONTROLLED_DEVICE}/sensor'
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

while True:
    mqtt_client.publish(
        MQTT_SENSOR_TOPIC,
        json.dumps({
            'test': randint(0, 100)
        })
    )
    time.sleep(1)
