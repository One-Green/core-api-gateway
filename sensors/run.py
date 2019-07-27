import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', os.path.dirname('__file__')))))

from core.helpers import run_parallel
# import all controller to run in parallel
from sensors import enclosure

# Run controller every  LOOP_EVERY value
# value in second
LOOP_EVERY: int = 1

# Run all sensors read
while True:
    run_parallel(enclosure.main())
    time.sleep(LOOP_EVERY)
