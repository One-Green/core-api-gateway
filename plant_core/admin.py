from django.contrib import admin
from plant_core.models import (
    PlantSettings,
    SprinklerSensor,
    SprinklerSettings,
    SprinklerTag,
    SprinklerController,
    WaterController,
    WaterSensor,
    HeaterSensor,
    HeaterController,
    CoolerSensor,
    CoolerController,
    AirHumidifierSensor,
    AirHumidifierController,
)

# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(SprinklerSensor)
admin.site.register(SprinklerSettings)
admin.site.register(SprinklerTag)
admin.site.register(SprinklerController)
admin.site.register(WaterController)
admin.site.register(WaterSensor)
admin.site.register(HeaterSensor)
admin.site.register(HeaterController)
admin.site.register(CoolerSensor)
admin.site.register(CoolerController)
admin.site.register(AirHumidifierSensor)
admin.site.register(AirHumidifierController)
