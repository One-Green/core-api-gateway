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
            threshold: float = 0,
            reverse: bool = False
    ):

        assert isinstance(float(threshold), float)
        assert isinstance(reverse, bool)

        self.threshold = threshold
        self.reverse = reverse

    def get_signal(
            self,
            sensor: float
    ) -> int:

        assert isinstance(float(sensor), float)
        signal: int = 0

        if sensor <= self.threshold:
            signal = 1

        elif (
                self.threshold <= sensor
                and
                self.reverse
        ):
            signal = 0

        return signal


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
