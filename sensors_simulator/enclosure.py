import os
import sys
import time
from typing import Union
from datetime import datetime
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))
django.setup()
from plant_core.models import Enclosure

# give a name for controlled device
# for printing / logging purpose
RELATED_SENSORS: str = 'ENCLOSURE'

# Print template
# generic template for logging/print (for log remove datetime_now)
PRINT_TEMPLATE = ('{datetime_now} ; {device} ; '
                  'T={temperature} ; HR(%)={hygrometry} ; '
                  '+ new sensors entry in database')

first_loop: bool = True
last_action: Union[bool, None] = None


def read_input():
    """
    function to read sensors input
    :return:
    """
    # if sensors values are not supplied by RESTful API
    # use this function to read sensors values and return
    # orm model values
    return {'enclosure_temperature': random.uniform(17., 25.),
            'enclosure_hygrometry': random.uniform(40., 70.),
            'enclosure_lightning':  random.uniform(10., 80.),
            'enclosure_air_co2_ppm':  random.uniform(400., 650.),
            'enclosure_cov_ppm':  random.uniform(700., 1000.)
            }


def main():
    new_read = read_input()
    Enclosure(enclosure_temperature=new_read['enclosure_temperature'],
              enclosure_hygrometry=new_read['enclosure_hygrometry'],
              enclosure_uv_index=new_read['enclosure_uv_index'],
              enclosure_cov_ppm=new_read['enclosure_cov_ppm'],
              enclosure_co2_ppm=new_read['enclosure_co2_ppm']).save()

    print(PRINT_TEMPLATE.format(datetime_now=datetime.now(),
                                device=RELATED_SENSORS,
                                temperature=new_read['enclosure_temperature'],
                                hygrometry=new_read['enclosure_hygrometry']))


if __name__ == '__main__':
    print(f'[!] Warning: {RELATED_SENSORS} sensors debug mode, use sensors/run.py to run all sensors write')
    while True:
        main()
        time.sleep(1/3)
