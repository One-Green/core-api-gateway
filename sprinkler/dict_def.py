from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    tag: str
    water_valve_signal: bool
    soil_moisture_min_level: float
    soil_moisture_max_level: float


class SprinklerSensorDict(TypedDict):
    tag: str
    soil_moisture: float
