from django.contrib import admin
from plant_core.models import (
    PlantSettings,
    SprinklerSoilHumiditySensor, SprinklerSettings,
    SprinklerTag,
    SprinklerValve,
    WaterPump, WaterTankSensor,
    HeaterSensor, Heater,
    CoolerSensor, Cooler,
    AirHumidifierSensor, AirHumidifier
)

# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(SprinklerSoilHumiditySensor)
admin.site.register(SprinklerSettings)
admin.site.register(SprinklerTag)
admin.site.register(SprinklerValve)
admin.site.register(WaterPump)
admin.site.register(WaterTankSensor)
admin.site.register(HeaterSensor)
admin.site.register(Heater)
admin.site.register(CoolerSensor)
admin.site.register(Cooler)
admin.site.register(AirHumidifierSensor)
admin.site.register(AirHumidifier)
