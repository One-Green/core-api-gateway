"""
module information : Many controller to one device aggregator

Author: Shanmugathas Vigneswaran
email: shanmugathas.vigneswaran@outlook.fr

Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
Licence:  https://creativecommons.org/licenses/by-nc/4.0/

"""

from typing import List
from .controller import BaseController


class BaseAggregator:
    """
    multi controller aggregation class
    """

    def __init__(
            self,
            controller_list: List[BaseController]
    ):
        """
        init with controller list
        :param controller_list:
        """
        assert isinstance(controller_list, list)
        self.controller_list: List[BaseController] = controller_list
        self.action_list: List[int] = []

    @property
    def action(self):
        """
        check all True in
        :return:
        """
        self.action_list = []
        for _ in self.controller_list:
            self.action_list.append(_.action)

        return 1 if 1 in self.action_list else 0
