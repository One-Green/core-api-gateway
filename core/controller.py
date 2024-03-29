"""
Device controller collection

Author: Shanmugathas Vigneswaran
email: shanmugathas.vigneswaran@outlook.fr

Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
Licence:  https://creativecommons.org/licenses/by-nc/4.0/

"""

from datetime import time, datetime


class BinaryController:
    """
    Binary controller class
    eg for soil humidity controller
    settings :
        - soil humidity minimum = 20
        - soil humidity maximum = 70
        - reverse = False

    if sensor = 21  will return signal=1 until sensor reach 70
    when reached 70, lock to return signal=0 until sensor reach 20.
    Lock is used to reduce the rate of switch OFF/ON by minutes
    in order to increase durability of component
    """

    def __init__(self):
        self._min = None
        self._max = None
        self.lock = None
        self.reverse = None

    def set_conf(self, _min: float, _max: float, reverse: bool = False) -> None:
        """
        Set configurations

        :param _min:  minimum value in neutral point
        :param _max:  maximum value in neutral point
        :param reverse:  reverse signal action (used for Cooler)
        :return:
        """
        assert isinstance(float(_min), float)
        assert isinstance(float(_max), float)
        assert isinstance(reverse, bool)

        self._min: float = _min
        self._max: float = _max
        self.reverse: bool = reverse

        self.lock: bool = False

    def __lock(self, sensor):
        if sensor >= self._max:
            self.lock = True

    def __unlock(self, sensor):
        if sensor <= self._min:
            self.lock = False

    def get_signal(self, sensor: float) -> bool:
        """
        Get power signal by using sensor value

        :param sensor: sensor signal value
        :return: O= power OFF, 1= power ON
        """
        assert isinstance(float(sensor), float)

        self.__lock(sensor)
        self.__unlock(sensor)

        if not self.reverse:
            if self._min < sensor <= self._max and not self.lock:
                return True
            elif sensor <= self._min:
                return True
            else:
                return False

        if self.reverse:
            if self._min < sensor <= self._max and not self.lock:
                return True

            elif sensor >= self._min:
                return True
            else:
                return False


class TimeRangeController:
    """
    Time based binary controller
    """

    def __init__(self, reverse: bool = False):

        self.end_at = None
        self.start_at = None
        self.time_now = None
        self.time_now: datetime
        self.start_at: datetime
        self.end_at: datetime
        self.reverse: bool = reverse
        self.state: int = 0

    def set_conf(self, start_at, end_at):
        self.start_at = start_at
        self.end_at = end_at

    def set_current_datetime(self, time_now: datetime):
        self.time_now: datetime = time_now

    def get_signal(self) -> int:
        if self.start_at.time() <= self.time_now.time() <= self.end_at.time():
            if self.reverse:
                self.state = 0
            else:
                self.state = 1
        else:
            if self.reverse:
                self.state = 1
            else:
                self.state = 0
        return self.state
