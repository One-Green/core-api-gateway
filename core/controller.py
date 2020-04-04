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
    binary controller class
    """

    def __init__(
            self,
            _max: float = 0,
            _min: float = 0,
            reverse: bool = False
    ):

        assert isinstance(float(_max), float)
        assert isinstance(float(_min), float)
        assert isinstance(reverse, bool)

        self._max = _max
        self._min = _min
        self.reverse = reverse
        self.__validate()
        self.__swap_min_max()

    def __validate(self):
        if self._min > self._max:
            raise ValueError(f'{self._min} > {self._max}')
        if self._min == self._max:
            raise ValueError(f'{self._min} == {self._max}')

    def __swap_min_max(self):
        if self.reverse:
            _max = self._min
            _min = self._max
            self._max = _max
            self._min = _min

    def __apply_reverse(self, signal: int):
        if self.reverse and not signal:
            return 1
        elif self.reverse and signal:
            return 0
        else:
            return signal

    def get_signal(self, sensor: float):

        assert isinstance(float(sensor), float)
        signal: int = 0

        if sensor < self._min:
            signal = 1
        elif sensor > self._max:
            signal = 0

        return self.__apply_reverse(signal)


BinaryController(21, 20).get_signal(20)


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
