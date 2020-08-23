from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    tag: str
    water_valve_signal: bool


class SprinklerSensorDict(TypedDict):
    tag: str
    soil_moisture: float
