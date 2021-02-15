from typing import TypedDict
from datetime import time


class LightCtrlDict(TypedDict):
    controller_type: str
    tag: str
    on_time_at: time
    off_time_at: time
