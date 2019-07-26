"""
O/I controller
Author : Shanmugathas Vigneswaran
"""


class BaseController:
    """
    binary controller class
    """

    def __init__(self, kind: str, neutral: float,
                 delta_max: float = 0, delta_min: float = 0,
                 reverse: bool = False):
        assert isinstance(kind, str)
        assert kind in ('CUT_IN', 'CUT_OUT')
        assert isinstance(float(neutral), float)
        assert isinstance(float(delta_max), float)
        assert isinstance(float(delta_min), float)
        assert isinstance(reverse, bool)

        self.kind: str = kind
        self.neutral: float = float(neutral)
        self.delta_max: float = float(delta_max)
        self.delta_min: float = float(delta_min)
        self.max_point = neutral + delta_max
        self.min_point = neutral - delta_min
        self.state: bool = False
        self.current_value: float = 0.0
        self.reverse = reverse

    def set_sensor_value(self, current_value: float) -> None:
        """
        set read sensor value
        :param current_value:
        :return:
        """
        self.current_value = current_value

    def __cut_in_handler(self):
        """
        cut in kind handler
        :return:
        """
        # neutral point => do nothing
        # or condition can be used here (less readable)
        if self.min_point <= self.current_value <= self.max_point:
            self.state = False
        # mini point reached, cut in => deactivate
        if self.current_value <= self.min_point:
            self.state = True
        # max point reached, cut in => activate
        elif self.current_value >= self.max_point:
            self.state = False

    def __cut_out_handler(self):
        """
        cut out kind handler
        :return:
        """
        if self.current_value <= self.min_point:
            if self.reverse:
                self.state = True
            else:
                self.state = False
        if self.current_value >= self.max_point:
            if self.reverse:
                self.state = False
            else:
                self.state = True

    def __pid_handler(self):
        pass

    @property
    def action(self) -> bool:
        """
        get action to do
        :return:
        """
        if self.kind == 'CUT_IN':
            self.__cut_in_handler()
            return self.state

        if self.kind == 'CUT_OUT':
            self.__cut_out_handler()
            return self.state
