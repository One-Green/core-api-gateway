from typing import TypedDict


class LightCtrlDict(TypedDict):
    cfg_type: str
    on_at: str
    off_at: str
    light_signal: int
    force_signal: int
