from django.contrib import admin
from plant_core.models import (
    PlantSettings,
    SprinklerSensor,
    SprinklerSettings,
    SprinklerTag,
    SprinklerController,
    WaterPumpController,
    WaterPumpSensor,
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
admin.site.register(WaterPumpController)
admin.site.register(WaterPumpSensor)
admin.site.register(HeaterSensor)
admin.site.register(HeaterController)
admin.site.register(CoolerSensor)
admin.site.register(CoolerController)
admin.site.register(AirHumidifierSensor)
admin.site.register(AirHumidifierController)
