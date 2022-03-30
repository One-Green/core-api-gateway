from typing import TypedDict


class WaterCtrlDict(TypedDict):
    p1: int  # water pump signal
    p2: int  # nutrient pump signal
    p3: int  # ph downer pump signal
    p5: int  # mixer pump signal
    fp1: int  # force water pump signal
    fp2: int  # force nutrient pump signal
    fp3: int  # force ph_downer_pump signal
    fp5: int  # force mixer pump signal
    tmax: float  # tds ppm max
    tmin: float  # tds ppm min
    pmax: float  # ph max
    pmin: float  # ph min
    spc: int  # count number of connected sprinkler
