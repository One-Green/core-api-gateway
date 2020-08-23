from typing import TypedDict


class WaterCtrlDict(TypedDict):
    water_pump_signal: bool
    nutrient_pump_signal: bool
    ph_downer_pump_signal: bool
