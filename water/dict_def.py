from typing import TypedDict


class WaterCtrlDict(TypedDict):
    p1: int  # water pump signal
    fps1: int  # force water pump signal
    fps2: int  # force nutrient pump signal
    fps3: int  # force ph_downer_pump signal
    fps4: int  # force mixer pump signal
    fp1: int  # force water pump ON
    fp2: int  # force nutrient pump ON
    fp3: int  # force ph_downer_pump ON
    fp4: int  # force mixer pump ON
    tmax: float  # tds ppm max
    tmin: float  # tds ppm min
    pmax: float  # ph max
    pmin: float  # ph min
    spc: int  # count number of connected sprinkler
