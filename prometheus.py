import os
import sys
import time
import random
import django
from prometheus_client import Gauge, start_http_server, Enum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname('__file__'))
django.setup()

from plant_kiper.settings import __version__, __current_repo__
from plant_core.models import Enclosure, Cooler, Heater
from core.deco import HEADER
from core.uv_helpers import UV_INDEX

SUB_SYS: str = 'Prometheus client'
INFO: str = 'Server created at http://localhost:8000, ensure Prometheus Server is running'

# Create sensors
enclosure_temperature = Gauge('enclosure_temperature', 'Enclosure temperature')
enclosure_hygrometry = Gauge('enclosure_hygrometry', 'Enclosure hygrometry')
enclosure_co2_ppm = Gauge('enclosure_co2_ppm', 'Enclosure CO2 ppm')
enclosure_voc_ppm = Gauge('enclosure_voc_ppm', 'Enclosure VOC ppm')
# enclosure_uv_index = Gauge('enclosure_uv_index', 'Enclosure UV index')
enclosure_uv_index = Enum('enclosure_uv_index', 'Enclosure UV index',
                          states=UV_INDEX)

# Devices status
cooler_status = Gauge('device_cooler_status', 'Cooler power status')
heater_cooler_status = Gauge('device_heater_status', 'Heater power status')


def main():
    """

    :return:
    """
    while True:
        enclosure_temperature.set(Enclosure.get_status()['enclosure_temperature'])
        # devices power status
        cooler_status.set(float(Cooler.get_status()['power_status']))
        heater_cooler_status.set(float(Heater.get_status()['power_status']))
        time.sleep(1)


def main_dummies():
    """
    populate fake metrics until first release
    :return:
    """
    while True:
        # enclosure sensors
        enclosure_temperature.set(float(random.randint(12, 30)))
        enclosure_hygrometry.set(float(random.randint(20, 90)))
        enclosure_co2_ppm.set(float(random.randint(300, 1500)))
        enclosure_voc_ppm.set(float(random.randint(500, 4000)))
        enclosure_uv_index.state(UV_INDEX[random.randint(0, 8)])

        # devices power status
        cooler_status.set(float(Cooler.get_status()['power_status']))
        heater_cooler_status.set(float(Heater.get_status()['power_status']))

        time.sleep(1)


if __name__ == '__main__':
    print(HEADER.format(version=__version__,
                        repo=__current_repo__,
                        sub_sys=SUB_SYS,
                        sub_sys_info=INFO))
    start_http_server(8000)
    main()
