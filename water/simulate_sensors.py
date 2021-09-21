import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.insert(0, os.path.abspath(".."))
django.setup()

import paho.mqtt.client as mqtt
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_SENSOR_TOPIC
import time
from random import randint
from influx_line_protocol import Metric

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

while True:
    metric = Metric("water")
    metric.add_tag("water", "default")
    metric.add_value("nutrient_level_cm", randint(20, 500))
    metric.add_value("ph_downer_level_cm", randint(20, 500))
    metric.add_value("ph_level", randint(20, 500))
    metric.add_value("tds_level", randint(20, 500))
    print(metric)
    mqtt_client.publish(MQTT_WATER_SENSOR_TOPIC, str(metric))
    time.sleep(0.5)
