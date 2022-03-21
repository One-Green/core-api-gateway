from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    controller_type: str
    tag: str
    water_valve_signal: int
    force_water_valve_signal: int
    soil_moisture_min_level: float
    soil_moisture_max_level: float
