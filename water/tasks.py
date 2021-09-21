"""
Celery + Redis async tasks
"""
from django.core.exceptions import ObjectDoesNotExist
import orjson as json
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.controller import BinaryController
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
from sprinkler.models import Sprinklers
from water.conf_def import WATER_CONTROLLER
from water.models import Water
from water.dict_def import WaterCtrlDict
from celery.decorators import task

CONTROLLED_DEVICE: str = "water"


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)


@task(name="water_control")
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
    w = Water()
    nutrient_ctl = BinaryController()
    ph_ctl = BinaryController()

    try:
        w.get_config()
    except ObjectDoesNotExist:
        w.update_config(
            ph_min_level=WATER_CONTROLLER["pH"]["min_level"],
            ph_max_level=WATER_CONTROLLER["pH"]["max_level"],
            tds_min_level=WATER_CONTROLLER["tds"]["max_level"],
            tds_max_level=WATER_CONTROLLER["tds"]["max_level"],
        )
        w.get_config()

    # Get actuator force configuration
    force_controller = Water().get_controller_force()
    # Nutrient control -----------
    nutrient_ctl.set_conf(_min=w.tds_min_level, _max=w.tds_max_level, reverse=False)
    nutrient_signal = nutrient_ctl.get_signal(d["fields"]["tds_level"])
    if force_controller["force_nutrient_pump_signal"]:
        nutrient_signal = int(force_controller["nutrient_pump_signal"])
    # pH downer control -----------
    ph_ctl.set_conf(_min=w.ph_min_level, _max=w.ph_max_level, reverse=False)
    ph_signal = ph_ctl.get_signal(d["fields"]["ph_level"])
    if force_controller["force_ph_downer_pump_signal"]:
        ph_signal = int(force_controller["ph_downer_pump_signal"])
    # water pump control ----------
    water_signal = int(Sprinklers().is_any_require_water())
    if force_controller["force_water_pump_signal"]:
        water_signal = int(force_controller["water_pump_signal"])
    # mixer pump control ----------
    mixer_signal = 0
    if force_controller["force_mixer_pump_signal"]:
        mixer_signal = int(force_controller["mixer_pump_signal"])

    pub_d: dict = WaterCtrlDict(
        tag="water",
        water_pump_signal=water_signal,
        nutrient_pump_signal=int(nutrient_signal),
        ph_downer_pump_signal=int(ph_signal),
        mixer_pump_signal=mixer_signal,
        tds_max_level=w.tds_max_level,
        tds_min_level=w.tds_min_level,
        ph_max_level=w.ph_max_level,
        ph_min_level=w.ph_min_level,
    )
    mqtt_client.publish(MQTT_WATER_CONTROLLER_TOPIC, json.dumps(pub_d))
