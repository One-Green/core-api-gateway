from django.contrib import admin
from plant_core.models import (
    PlantSettings,
    Enclosure,
    Cooler,
    AirHumidifier,
    WaterPump,
    SprinklerTag,
    SprinklerSettings,
    SprinklerValve,
    Heater,
    UvLight,
    CO2Valve,
    Filters
)

# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(Enclosure)
admin.site.register(Cooler)
admin.site.register(AirHumidifier)
admin.site.register(WaterPump)
admin.site.register(SprinklerTag)
admin.site.register(SprinklerSettings)
admin.site.register(SprinklerValve)
admin.site.register(Heater)
admin.site.register(UvLight)
admin.site.register(CO2Valve)
admin.site.register(Filters)
