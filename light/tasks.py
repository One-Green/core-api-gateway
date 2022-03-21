"""
Celery + Redis async tasks
"""
from datetime import datetime
from line_protocol_parser import parse_line
from light.models import (
    Device,
    Sensor,
    Config,
    ConfigType,
    DailyTimeRange,
    Controller,
    ForceController,
)
from light.config import set_default_config
from light.dict_def import LightCtrlDict
from project.settings import MQTT_HOST
from project.settings import MQTT_PORT
from project.settings import MQTT_USERNAME
from project.settings import MQTT_PASSWORD
from project.settings import MQTT_LIGHT_CONTROLLER_TOPIC
from celery import shared_task
import paho.mqtt.client as mqtt
import orjson as json
from posixpath import join

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

    # Create device based on tag
    # --------------------------
    Device.objects.update_or_create(tag=tag)

    # Save sensor status
    # --------------------------
    Sensor.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={
            "lux_lvl": d["fields"]["lux_lvl"],
            "photo_resistor_raw": d["fields"]["photo_res_raw"],
            "photo_resistor_percent": d["fields"]["photo_res_perc"],
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

    # check if light can up
    # --------------------------
    light_signal: bool = False
    on_at: str = "?"
    off_at: str = "?"
    if ConfigType.objects.get(id=cfg.config_type_id).name == "daily":
        # handle config type "daily"
        if (
            DailyTimeRange.objects.get(id=cfg.daily_config_id).on_at
            <= datetime.utcnow().time()
            <= DailyTimeRange.objects.get(id=cfg.daily_config_id).off_at
        ):
            light_signal = True
        on_at = DailyTimeRange.objects.get(id=cfg.daily_config_id).on_at.strftime(
            "%H:%M:%S"
        )
        off_at = DailyTimeRange.objects.get(id=cfg.daily_config_id).off_at.strftime(
            "%H:%M:%S"
        )
    elif ConfigType.objects.get(id=cfg.config_type_id).name == "planner":
        # handle config type "planner" > use calendar config
        for _ in cfg.planner_configs.all():
            if (
                datetime.combine(_.start_date_at, _.on_time_at)
                <= datetime.utcnow()
                <= datetime.combine(_.end_date_at, _.off_time_at)
            ):
                light_signal = True

        on_at = "planner"
        off_at = "planner"

    # check if force signal
    # --------------------------
    try:
        fctl = ForceController.objects.get(tag=Device.objects.get(tag=tag))
        if fctl.force_light_signal:
            light_signal = fctl.light_signal
    except ForceController.DoesNotExist:
        # create class to add force_light_signal attribute to mock
        # if ForceController object not found
        class A:
            pass

        fctl = A()
        fctl.force_light_signal = False

    # save controller  status
    # --------------------------
    Controller.objects.update_or_create(
        tag=Device.objects.get(tag=tag),
        defaults={"light_signal": light_signal},
    )

    callback_d: dict = LightCtrlDict(
        cfg_type=ConfigType.objects.get(id=cfg.config_type_id).name,
        on_at=on_at,
        off_at=off_at,
        light_signal=light_signal,
        force_signal=fctl.force_light_signal,
    )
    print(callback_d)
    mqtt_client.publish(
        join(MQTT_LIGHT_CONTROLLER_TOPIC, tag),
        json.dumps(callback_d),
    )
