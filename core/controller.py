"""
O/I controller
Author : Shanmugathas Vigneswaran
"""


class BaseController:
    """
    binary controller class
    """

    def __init__(self, kind: str, neutral: float, delta_max: float, delta_min: float):
        assert isinstance(kind, str)
        assert kind in ('CUT_IN', 'CUT_OUT')
        assert isinstance(delta_max, float)
        assert isinstance(delta_min, float)

        self.kind: str = kind
        self.neutral: float = neutral
        self.delta_max: float = delta_max
        self.delta_min: float = delta_min
        self.max_point = neutral + delta_max
        self.min_point = neutral - delta_min
        self.state: int = 0
        self.current_value: float = 0.0

    def set_current_value(self, current_value: float):
        """
        set current value
        :param current_value:
        :return:
        """
        self.current_value = current_value

    def controller(self) -> int:
        """
        call this method for chose action
        :param current_value:
        :return:
        """
        if self.kind == 'CUT_IN':
            # neutral point => do nothing
            # or condition can be used here (less readable)
            if self.min_point <= self.current_value <= self.max_point:
                self.state = 0
            # mini point reached, cut in => deactivate
            if self.current_value <= self.min_point:
                self.state = 1
            # max point reached, cut in => activate
            elif self.current_value >= self.max_point:
                self.state = -1

        elif self.kind == 'CUT_OUT':
            # neutral point => do nothing
            if self.min_point <= self.current_value <= self.max_point:
                self.state = 0
            # mini point reached , cut out => activate
            elif self.current_value <= self.min_point:
                self.state = -1
            elif self.current_value >= self.max_point:
                self.state = 1

        return self.state
