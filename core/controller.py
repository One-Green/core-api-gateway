"""
module information : Device controller collection

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

    def set_conf(
            self,
            _min: float,
            _max: float,
            reverse: bool = False
    ):

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

    def get_signal(self, sensor):
        assert isinstance(float(sensor), float)

        self.__lock(sensor)
        self.__unlock(sensor)

        if (
                self._min < sensor <= self._max
                and
                not self.lock
        ):
            return 1
        elif sensor <= self._min:
            return 1
        else:
            return 0


class BaseTimeRangeController:
    """
    Time based binary controller
    """

    def __init__(
            self,
            start_at: time,
            end_at: time,
            reverse: bool = False
    ):

        assert isinstance(start_at, time)
        assert isinstance(end_at, time)
        assert isinstance(reverse, bool)

        self.time_now: time = datetime.now().time()
        self.start_at: time = start_at
        self.end_at: time = end_at
        self.reverse: bool = reverse
        self.state: int = 0

    def set_current_time(
            self,
            time_now: time
    ):
        assert isinstance(time_now, time)
        self.time_now = time_now

    @property
    def action(self) -> int:
        if self.start_at <= self.time_now <= self.end_at:
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
