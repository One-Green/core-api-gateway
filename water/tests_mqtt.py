import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

import paho.mqtt.client as mqtt
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USER
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_SENSOR_TOPIC
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
import orjson as json
from pprint import pprint

influx_template = (
    "water,tag=test "
    "nutrient_level_cm={nutrient_level_cm}i,"
    "ph_downer_level_cm={ph_downer_level_cm}i,"
    "ph_level={ph_level}i,"
    "tds_level={tds_level}i"
)
i = 10
callback_lst = []


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_WATER_CONTROLLER_TOPIC)
    for _ in range(10):
        mqtt_client.publish(
            MQTT_WATER_SENSOR_TOPIC,
            influx_template.format(
                nutrient_level_cm=12,
                ph_downer_level_cm=20,
                ph_level=10,
                tds_level=1000
            )
        )


def on_message(client, userdata, msg):
    global i
    i += 1

    print(f"response from topic {MQTT_WATER_CONTROLLER_TOPIC}")
    d = json.loads(msg.payload)
    callback_lst.append(d)
    if i > 19:
        client.disconnect()


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()

pprint(callback_lst)
