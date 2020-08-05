from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    tag: str
    signal: bool


class SprinklerSensorDict(TypedDict):
    tag: str
    soil_moisture: float


class WaterCtrlDict(TypedDict):
    water_pump_signal: bool
    ph_down_pump_signal: bool
    nutrient_up_pump_signal: bool
