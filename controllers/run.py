import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))

from core.helpers import run_parallel
# import all controller to run in parallel
from controllers import cooler, heater, vapor_generator, light

# Run controller every  LOOP_EVERY value
# value in second
LOOP_EVERY: int = 1

# Run all controllers
while True:
    run_parallel(cooler.main(),
                 heater.main(),
                 vapor_generator.main(),
                 light.main())
    time.sleep(LOOP_EVERY)
