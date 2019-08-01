import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.join('..', '..', '..', os.path.dirname('__file__')))))
from core.controller import BaseController, BaseTimeRangeController


class TestBaseController(unittest.TestCase):

    def test_cut_out(self):
        # test cut out controller
        test_instance = BaseController(kind='CUT_OUT',
                                       neutral=20,
                                       delta_max=2,
                                       delta_min=0)

        # test no required action conditions
        for _ in range(19, 21):
            test_instance.set_sensor_value(_)
            self.assertFalse(test_instance.action)

        # test action required conditions
        for _ in range(22, 25):
            test_instance.set_sensor_value(_)
            self.assertTrue(test_instance.action)

    def test_cut_out_reversed(self):
        # test cut out controller with reverser behaviour
        test_instance = BaseController(kind='CUT_OUT',
                                       neutral=20,
                                       delta_max=0,
                                       delta_min=2,
                                       reverse=True)

        # test no required action conditions
        for _ in reversed(range(21, 25)):
            test_instance.set_sensor_value(_)
            self.assertFalse(test_instance.action)

        # test action required conditions
        for _ in reversed(range(18, 19)):
            test_instance.set_sensor_value(_)
            self.assertTrue(test_instance.action)

    def test_cut_in(self):
        pass


class TestTimeRangeController(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
