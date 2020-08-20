import redis
import orjson as json
import rom
import paho.mqtt.client as mqtt
from line_protocol_parser import parse_line
from core.utils import get_now
from pprint import pprint
from core.controller_default_config import WATER_CONTROLLER
from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import MQTT_HOST
from settings import MQTT_PORT
from core.pk_rom.sprinkler import Sprinklers
from core.pk_dict import WaterCtrlDict

CONTROLLED_DEVICE: str = "water"

REDIS_CONTROLLER_CONFIG_KEY: str = f"{CONTROLLED_DEVICE}_config"
DEFAULT_CONFIG: dict = WATER_CONTROLLER

MQTT_SENSOR_TOPIC: str = f'{CONTROLLED_DEVICE}/sensor'
MQTT_CONTROLLER_TOPIC: str = f'{CONTROLLED_DEVICE}/controller'


BONJOUR: str = f'''
M""MMM""MMM""M MMP"""""""MM M""""""""M MM""""""""`M MM"""""""`MM          MM'""""'YMM M""""""""M M""MMMMMMMM 
M  MMM  MMM  M M' .mmmm  MM Mmmm  mmmM MM  mmmmmmmM MM  mmmm,  M          M' .mmm. `M Mmmm  mmmM M  MMMMMMMM 
M  MMP  MMP  M M         `M MMMM  MMMM M`      MMMM M'        .M          M  MMMMMooM MMMM  MMMM M  MMMMMMMM 
M  MM'  MM' .M M  MMMMM  MM MMMM  MMMM MM  MMMMMMMM MM  MMMb. "M 88888888 M  MMMMMMMM MMMM  MMMM M  MMMMMMMM 
M  `' . '' .MM M  MMMMM  MM MMMM  MMMM MM  MMMMMMMM MM  MMMMM  M          M. `MMM' .M MMMM  MMMM M  MMMMMMMM 
M    .d  .dMMM M  MMMMM  MM MMMM  MMMM MM        .M MM  MMMMM  M          MM.     .dM MMMM  MMMM M         M 
MMMMMMMMMMMMMM MMMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMMM MMMMMMMMMMMM          MMMMMMMMMMM MMMMMMMMMM MMMMMMMMMMM 
MM
MM {REDIS_HOST=}
MM {REDIS_PORT=}
MM {REDIS_CONTROLLER_CONFIG_KEY=}
MM -------------
MM
MM {MQTT_HOST=}
MM {MQTT_PORT=}
MM {MQTT_SENSOR_TOPIC=}
MM {MQTT_CONTROLLER_TOPIC=}
MM ------------

Controller starting 
'''

print(BONJOUR)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
rom.util.set_connection_settings(host=REDIS_HOST, port=REDIS_PORT, db=0)

controller_config = redis_client.get(REDIS_CONTROLLER_CONFIG_KEY)
if not controller_config:
    print(
        f"[{get_now()}] [REDIS] [ERROR] [{CONTROLLED_DEVICE}]"
        f" Cannot find configuration for key {REDIS_CONTROLLER_CONFIG_KEY=}"
    )
    redis_client.get(REDIS_CONTROLLER_CONFIG_KEY)
    redis_client.set(
        REDIS_CONTROLLER_CONFIG_KEY,
        json.dumps(DEFAULT_CONFIG)
    )
    print(
        f"[{get_now()}] [REDIS] [{CONTROLLED_DEVICE}]"
        f" Using default configuration"
    )
    pprint(
        json.loads(
            redis_client.get(
                REDIS_CONTROLLER_CONFIG_KEY
            )
        )
    )


def on_connect(client, userdata, flags, rc):
    print(f"[{get_now()}] [MQTT] [OK] [{CONTROLLED_DEVICE}] Connected with result code {rc}")
    client.subscribe(MQTT_SENSOR_TOPIC)


def on_message(client, userdata, msg):
    """
    Water supply pump I/O  callback
    Nutrient supply pump I/O callback
    pH down supply pump I/O callback
    :param client:
    :param userdata:
    :param msg:
    :return:
    """

    d: dict = parse_line(msg.payload + b' 0')
    # TODO: Nutrient controller
    # TODO: pH downer controller
    pub_d: dict = WaterCtrlDict(
        water_pump_signal=Sprinklers().is_any_require_water(),
        nutrient_pump_signal=False,
        ph_downer_pump_signal=False
        )
    client.publish(
        MQTT_CONTROLLER_TOPIC,
        json.dumps(pub_d)
    )


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
