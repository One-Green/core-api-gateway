"""
Celery + Redis async tasks
"""

from line_protocol_parser import parse_line
from core.controller import BinaryController
from sprinkler.config import set_default_config, set_default_force_controller
from sprinkler.dict_def import SprinklerCtrlDict
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_SPRINKLER_CONTROLLER_TOPIC
from celery import shared_task
import paho.mqtt.client as mqtt
import orjson as json
from posixpath import join
from sprinkler.models import Device, Sensor, Config, Controller, ForceController
from water.models import Device as WaterDevice

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)


@shared_task(name="sprinkler_control")
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

    # Create device based on tag
    # --------------------------
    Device.objects.update_or_create(tag=tag)

    # Save sensor status
    # --------------------------
    Sensor.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={
            "soil_moisture_raw_adc": d["fields"]["soil_moisture_raw_adc"],
            "soil_moisture": d["fields"]["soil_moisture"],
        },
    )

    # Get or create default config then get config
    # --------------------------
    try:
        cfg = Config.objects.get(tag=Device.objects.get(tag=tag))
    except Config.DoesNotExist:
        set_default_config(tag=tag)
    finally:
        cfg = Config.objects.get(tag=Device.objects.get(tag=tag))

    # check if valve can open
    # --------------------------
    water_valve_signal: bool = False
    ctl = BinaryController()
    ctl.set_conf(
        _min=cfg.soil_moisture_min_level,
        _max=cfg.soil_moisture_max_level,
        reverse=False,
    )
    water_valve_signal = ctl.get_signal(d["fields"]["soil_moisture"])

    # save controller  status
    # --------------------------
    Controller.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={"water_valve_signal": water_valve_signal},
    )

    # check if force signal
    # --------------------------
    try:
        fctl = ForceController.objects.get(tag=Device.objects.get(tag=tag))
    except ForceController.DoesNotExist:
        set_default_force_controller(tag=tag)
    finally:
        fctl = ForceController.objects.get(tag=Device.objects.get(tag=tag))

    # generate JSON
    # --------------------------
    callback_d: dict = SprinklerCtrlDict(
        wtl=WaterDevice.objects.get(tag=cfg.water_tag_link).tag,
        wvs=int(water_valve_signal),
        fwv=int(fctl.water_valve_signal),
        fwvs=int(fctl.force_water_valve_signal),
        hmin=cfg.soil_moisture_min_level,
        hmax=cfg.soil_moisture_max_level
    )

    # Publish JSON to MQTT
    # --------------------------
    mqtt_client.publish(
        join(MQTT_SPRINKLER_CONTROLLER_TOPIC, tag),
        json.dumps(callback_d),
    )
