"""
multi controller for one device aggregator handler
Author : Shanmugathas Vigneswaran
"""

from typing import List
from .controller import BaseController


class BaseAggregator:
    """
    multi controller aggregation class
    """

    def __init__(self, controller_list: List[BaseController]):
        """
        init with controller list
        :param controller_list:
        """
        assert isinstance(controller_list, list)
        self.controller_list: List[BaseController] = controller_list
        self.action_list: List[bool] = []

    @property
    def action(self):
        """
        check all True in
        :return:
        """
        self.action_list = []
        for _ in self.controller_list:
            self.action_list.append(_.action)

        return True if True in self.action_list else False
