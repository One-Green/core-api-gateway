import os
import sys
import time
import random
import django
from prometheus_client import Gauge, start_http_server

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname('__file__'))
django.setup()

from plant_kiper.settings import __version__, __current_repo__
from plant_core.models import Enclosure
from core.deco import HEADER

SUB_SYS: str = 'PROMETHEUS REPORT'
INFO: str = 'Server created: localhost:8000 to expose open metrics data'

# Create sensors
enclosure_temperature = Gauge('enclosure_temperature', 'Enclosure temperature')


def main():
    while True:
        rand = float(random.randint(0, 100))
        enclosure_temperature.set(rand)


if __name__ == '__main__':
    print(HEADER.format(version=__version__,
                        repo=__current_repo__,
                        sub_sys=SUB_SYS))
    start_http_server(8000)
    main()
    time.sleep(1)
