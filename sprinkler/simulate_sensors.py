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
from project.settings import MQTT_SPRINKLER_SENSOR_TOPIC
import time
from random import randint
from rest_framework.test import APIRequestFactory
from influx_line_protocol import Metric
from sprinkler.views import RegistryView

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

sprinklers = ["tomato", "eggplant", "watermelon", "potato"]
factory = APIRequestFactory()
view = RegistryView.as_view()

for _ in sprinklers:
    view(factory.delete("sprinkler/registry", {"tag": _}))
    view(factory.post("sprinkler/registry", {"tag": _}))

while True:
    for _ in sprinklers:
        metric = Metric("sprinkler")
        metric.add_tag("tag", _)
        metric.add_value("soil_moisture_raw_adc", randint(20, 500))
        metric.add_value("soil_moisture", randint(20, 500))
        print(metric)
        mqtt_client.publish(MQTT_SPRINKLER_SENSOR_TOPIC, str(metric))
        time.sleep(1)
