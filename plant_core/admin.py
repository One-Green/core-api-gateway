from django.contrib import admin
from plant_core.models import (PlantSettings,
                               Enclosure,
                               Cooler,
                               VaporGenerator,
                               WaterPump,
                               Heater,
                               UvLight,
                               CO2Valve,
                               Filters)
# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(Enclosure)
admin.site.register(Cooler)
admin.site.register(VaporGenerator)
admin.site.register(WaterPump)
admin.site.register(Heater)
admin.site.register(UvLight)
admin.site.register(CO2Valve)
admin.site.register(Filters)
