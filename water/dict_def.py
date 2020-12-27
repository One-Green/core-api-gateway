from typing import TypedDict


class WaterCtrlDict(TypedDict):
    tag: str
    water_pump_signal: int
    nutrient_pump_signal: int
    ph_downer_pump_signal: int
    tds_max_level: float
    tds_min_level: float
    ph_max_level: float
    ph_min_level: float
