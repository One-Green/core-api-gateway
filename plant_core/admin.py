from django.contrib import admin
from plant_core.models import (
    PlantSettings,
    SprinklerSoilHumiditySensor,
    SprinklerSettings,
    SprinklerTag,
    SprinklerValve,
    WaterPump,
    WaterTankSensor
)

# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(SprinklerSoilHumiditySensor)
admin.site.register(SprinklerSettings)
admin.site.register(SprinklerTag)
admin.site.register(SprinklerValve)
admin.site.register(WaterPump)
admin.site.register(WaterTankSensor)
