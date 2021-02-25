from typing import TypedDict


class LightCtrlDict(TypedDict):
    controller_type: str
    tag: str
    on_time_at: str
    off_time_at: str
    light_signal: bool
