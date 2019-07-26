import os
import sys
from multiprocessing import Process
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_kiper.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))

# import all controller to run in parallel
from controllers import cooler, heater, vapor_generator, light

# Run controller every  LOOP_EVERY value
# value in second
LOOP_EVERY: int = 1


def run_parallel(*fns):
    """
    run multiprocessing function
    source = https://stackoverflow.com/questions/7207309/python-how-can-i-run-python-functions-in-parallel
    :param fns:
    :return:
    """
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


# Run all controllers
while True:
    run_parallel(cooler.main(),
                 heater.main(),
                 vapor_generator.main(),
                 light.main())
    time.sleep(LOOP_EVERY)
