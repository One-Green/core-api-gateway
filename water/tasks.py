"""
Celery + Redis async tasks
"""
import orjson as json
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.controller import BinaryController
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
from water.helpers import is_any_require_water
from water.config import set_default_config
from water.dict_def import WaterCtrlDict
from celery import shared_task
from posixpath import join
from water.models import Device, Sensor, Config, Controller, ForceController

CONTROLLED_DEVICE: str = "water"

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)


@shared_task(name="water_control")
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
            "ph_voltage": d["fields"]["ph_voltage"],
            "tds_voltage": d["fields"]["tds_voltage"],
            "ph_level": d["fields"]["ph_level"],
            "tds_level": d["fields"]["tds_level"],
            "water_tk_lvl": d["fields"]["water_tk_lvl"],
            "nutrient_tk_lvl": d["fields"]["nutrient_tk_lvl"],
            "ph_downer_tk_lvl": d["fields"]["ph_downer_tk_lvl"],
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

    # check if :
    #       - water pump can start
    #       - nutrient pump can start
    #       - pH downer pump can start
    #       - mixer pump can start
    # --------------------------
    water_pump_signal: bool = is_any_require_water(tag=tag)
    nutrient_pump_signal: bool
    ph_downer_pump_signal: bool
    mixer_pump_signal: bool = False

    nutrient_ctl = BinaryController()
    nutrient_ctl.set_conf(_min=cfg.tds_min_level, _max=cfg.tds_max_level, reverse=False)
    nutrient_pump_signal = nutrient_ctl.get_signal(d["fields"]["tds_level"])

    ph_ctl = BinaryController()
    ph_ctl.set_conf(_min=cfg.ph_min_level, _max=cfg.ph_max_level, reverse=False)
    ph_downer_pump_signal = ph_ctl.get_signal(d["fields"]["ph_level"])

    # check if force signal
    # --------------------------
    class A:
        pass

    try:
        fctl = ForceController.objects.get(tag=Device.objects.get(tag=tag))
        if fctl.force_water_pump_signal:
            water_pump_signal = fctl.water_pump_signal
        if fctl.force_nutrient_pump_signal:
            nutrient_pump_signal = fctl.nutrient_pump_signal
        if fctl.force_ph_downer_pump_signal:
            ph_downer_pump_signal = fctl.ph_downer_pump_signal
        if fctl.force_mixer_pump_signal:
            mixer_pump_signal = fctl.mixer_pump_signal
    except ForceController.DoesNotExist:
        fctl = A()
        fctl.force_water_pump_signal = False
        fctl.force_nutrient_pump_signal = False
        fctl.force_ph_downer_pump_signal = False
        fctl.force_mixer_pump_signal = False

    # save controller  status
    # --------------------------
    Controller.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={
            "water_pump_signal": water_pump_signal,
            "nutrient_pump_signal": nutrient_pump_signal,
            "ph_downer_pump_signal": ph_downer_pump_signal,
            "mixer_pump_signal": mixer_pump_signal,
        },
    )

    # generate JSON
    # --------------------------
    pub_d: dict = WaterCtrlDict(
        tag=tag,
        water_pump_signal=water_pump_signal,
        nutrient_pump_signal=nutrient_pump_signal,
        ph_downer_pump_signal=ph_downer_pump_signal,
        mixer_pump_signal=mixer_pump_signal,
        force_water_pump_signal=fctl.force_water_pump_signal,
        force_nutrient_pump_signal=fctl.force_nutrient_pump_signal,
        force_ph_downer_pump_signal=fctl.force_ph_downer_pump_signal,
        force_mixer_pump_signal=fctl.force_mixer_pump_signal,
        tds_max_level=cfg.tds_max_level,
        tds_min_level=cfg.tds_min_level,
        ph_max_level=cfg.ph_max_level,
        ph_min_level=cfg.ph_min_level,
    )

    # Publish JSON to MQTT
    # --------------------------
    mqtt_client.publish(join(MQTT_WATER_CONTROLLER_TOPIC, tag), json.dumps(pub_d))
