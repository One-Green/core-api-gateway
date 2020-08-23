from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    tag: str
    water_valve_signal: bool


class SprinklerSensorDict(TypedDict):
    tag: str
    soil_moisture: float


class WaterCtrlDict(TypedDict):
    water_pump_signal: bool
    nutrient_pump_signal: bool
    ph_downer_pump_signal: bool
