from typing import TypedDict


class SprinklerCtrlDict(TypedDict):
    wtl: str  # water tag link
    wvs: int  # water_valve_signal
    fwv: int  # force_water_valve
    fwvs: int  # force_water_valve_signal
    hmin: float  # soil_moisture_min_level
    hmax: float  # soil_moisture_max_level
