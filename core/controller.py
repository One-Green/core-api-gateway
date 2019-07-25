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
        assert isinstance(float(neutral), float)
        assert isinstance(float(delta_max), float)
        assert isinstance(float(delta_min), float)

        self.kind: str = kind
        self.neutral: float = float(neutral)
        self.delta_max: float = float(delta_max)
        self.delta_min: float = float(delta_min)
        self.max_point = neutral + delta_max
        self.min_point = neutral - delta_min
        self.state: bool = False
        self.current_value: float = 0.0

    def get_action(self, current_value: float) -> bool:
        """
        call this method for chose action
        :return:
        """

        self.current_value = current_value

        if self.kind == 'CUT_IN':
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

        if self.kind == 'CUT_OUT':
            # neutral point => do nothing
            if self.min_point <= self.current_value <= self.max_point:
                self.state = False
            # mini point reached , cut out => activate
            elif self.current_value <= self.min_point:
                self.state = False
            elif self.current_value >= self.max_point:
                self.state = True

        return self.state
