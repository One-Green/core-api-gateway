from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
from core.utils import get_now
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_SPRINKLER_SENSOR_TOPIC
from project.settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from sprinkler.tasks import node_controller

CONTROLLED_DEVICE = "sprinkler"
BONJOUR: str = f"""
  ___  _ __   ___        __ _ _ __ ___  ___ _ __   (_) ___  
 / _ \| '_ \ / _ \_____ / _` | '__/ _ \/ _ \ '_ \  | |/ _ \ 
| (_) | | | |  __/_____| (_| | | |  __/  __/ | | |_| | (_) |
 \___/|_| |_|\___|      \__, |_|  \___|\___|_| |_(_)_|\___/ 
                        |___/                               
{MQTT_HOST=} 
{MQTT_PORT=}
{MQTT_SPRINKLER_SENSOR_TOPIC=}
{MQTT_SPRINKLER_CONTROLLER_TOPIC=}/<sprinkler-tag>
---------------------------------------------
Starting controller {CONTROLLED_DEVICE} ...
---------------------------------------------
"""
print(BONJOUR)


class Command(BaseCommand):
    help = (
        "Start Sprinkler controller "
        "(consume sensor MQTT topic > rules management > Produce into controller MQTT topic"
    )

    def on_connect(self, client, userdata, flags, rc):
        print(
            f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}"
        )

        client.subscribe(MQTT_SPRINKLER_SENSOR_TOPIC)

    def on_message(self, client, userdata, msg):
        """
        Water supply pump I/O  callback
        Nutrient supply pump I/O callback
        pH down supply pump I/O callback
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        print(f"[INFO][MQTT]  Message >> Water Celery Worker : {msg.payload}")
        node_controller.delay(msg.payload)

    def handle(self, *args, **kwargs):
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message
        mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
        mqtt_client.loop_forever()
