"""
Celery + Redis async tasks
"""
import orjson as json
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_WATER_CONTROLLER_TOPIC
from water.helpers import is_any_require_water, count_linked_sprinkler
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

    # check if  water pump must start
    # --------------------------
    water_pump_signal: bool = is_any_require_water(tag=tag)

    # check if force signal
    # --------------------------
    try:
        fctl = ForceController.objects.get(tag=Device.objects.get(tag=tag))
    except ForceController.DoesNotExist:
        class A:
            pass
        fctl = A()
        fctl.water_pump_signal = False
        fctl.nutrient_pump_signal = False
        fctl.ph_downer_pump_signal = False
        fctl.mixer_pump_signal = False
        fctl.force_water_pump_signal = False
        fctl.force_nutrient_pump_signal = False
        fctl.force_ph_downer_pump_signal = False
        fctl.force_mixer_pump_signal = False

    # generate JSON
    # --------------------------
    callback_d: dict = WaterCtrlDict(
        p1=int(water_pump_signal),
        fps1=int(fctl.force_water_pump_signal),
        fps2=int(fctl.force_nutrient_pump_signal),
        fps3=int(fctl.force_ph_downer_pump_signal),
        fps4=int(fctl.force_mixer_pump_signal),
        fp1=int(fctl.water_pump_signal),
        fp2=int(fctl.nutrient_pump_signal),
        fp3=int(fctl.ph_downer_pump_signal),
        fp4=int(fctl.mixer_pump_signal),
        tmax=cfg.tds_max_level,
        tmin=cfg.tds_min_level,
        pmax=cfg.ph_max_level,
        pmin=cfg.ph_min_level,
        spc=count_linked_sprinkler(tag)
    )

    # Publish JSON to MQTT
    # --------------------------
    mqtt_client.publish(join(MQTT_WATER_CONTROLLER_TOPIC, tag), json.dumps(callback_d))
