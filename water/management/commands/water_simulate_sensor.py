from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_SENSOR_TOPIC
import time
from influx_line_protocol import Metric

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

NODE_TAG = "default"


class Command(BaseCommand):
    help = "Start simulate water sensor pub on MQTT"

    def handle(self, *args, **kwargs):
        while True:
            metric = Metric("water")
            metric.add_tag("tag", NODE_TAG)

            for _ in range(0, 500):
                metric.add_value("ph_voltage", _)
                metric.add_value("tds_voltage", _)
                metric.add_value("ph_level", _)
                metric.add_value("tds_level", _)
                metric.add_value("water_tk_lvl", _)
                metric.add_value("nutrient_tk_lvl", _)
                metric.add_value("ph_downer_tk_lvl", _)
                mqtt_client.publish(MQTT_WATER_SENSOR_TOPIC, str(metric))
                print(str(metric))
                time.sleep(0.5)

            for _ in range(500, 0):
                metric.add_value("ph_voltage", _)
                metric.add_value("tds_voltage", _)
                metric.add_value("ph_level", _)
                metric.add_value("tds_level", _)
                metric.add_value("water_tk_lvl", _)
                metric.add_value("nutrient_tk_lvl", _)
                metric.add_value("ph_downer_tk_lvl", _)
                mqtt_client.publish(MQTT_WATER_SENSOR_TOPIC, str(metric))
                print(str(metric))
                time.sleep(0.5)
