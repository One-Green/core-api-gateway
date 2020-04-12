import os
import sys
from datetime import time
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', '..', os.path.dirname('__file__')))))
from core.controller import BaseTimeRangeController


class TestTimeRangeController(unittest.TestCase):

    def test_time_range(self):
        start_at = time(10, 0, 0)
        end_at = time(12, 0, 0)
        time_range_controller = BaseTimeRangeController(start_at, end_at)

        time_now = time(11, 0, 0)
        time_range_controller.set_current_time(time_now)
        self.assertTrue(time_range_controller.action)

        time_now = time(12, 15, 0)
        time_range_controller.set_current_time(time_now)
        self.assertFalse(time_range_controller.action)


if __name__ == '__main__':
    unittest.main()
