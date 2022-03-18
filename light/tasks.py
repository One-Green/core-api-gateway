"""
Celery + Redis async tasks
"""
import os.path
from line_protocol_parser import parse_line
from light.models import (
    Device,
    Sensor,
    ConfigType,
    DailyTimeRange,
    CalendarRange,
    Controller,
    ForceController
)
from light.dict_def import LightCtrlDict
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_LIGHT_CONTROLLER_TOPIC
from celery import shared_task
import paho.mqtt.client as mqtt
import orjson as json



mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)


@shared_task(name="light_control")
def node_controller(message):
    """
    async task : read message from mqtt,
    apply controller rules
    write on message on MQTT topic
    :param message:
    :return:
    """

    mqtt_client.reconnect()
    d: dict = parse_line(message + b" 0")
    tag: str = d["tags"]["tag"]

    Device.objects.update_or_create(tag=tag)

    Sensor.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={
            "lux_lvl": d["fields"]["lux_lvl"],
            "photo_resistor_raw": d["fields"]["photo_res_raw"],
            "photo_resistor_percent": d["fields"]["photo_res_perc"]
        }
    )
    # TODO:
    #   - get config type
    #   - if not config use default daily conf
    #   - depends on dail/calendar based
    #       retrieve on_at + off_at
    #       if in range  (on_at < x < off_att) > signal = true
    #       if force > signal = true
    #   - update controller model status

    # TODO use good values
    #  on_at=on_datetime_at.strftime("%H:%M:%S"),
    #  off_at=light.off_datetime_at.strftime("%H:%M:%S"),
    callback_d: dict = LightCtrlDict(
        cfg_type="planner",
        on_at="12:30:30",
        off_at="16:30:30",
        light_signal=0,
        force_signal=1
    )
    mqtt_client.publish(
        os.path.join(MQTT_LIGHT_CONTROLLER_TOPIC, tag),
        json.dumps(callback_d),
    )
