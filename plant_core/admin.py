from django.contrib import admin
from plant_core.models import (PlantSettings,
                               Enclosure,
                               PeltierCell,
                               VaporGenerator,
                               WaterTank,
                               ElectricalHeater,
                               UvLight,
                               CO2Valve,
                               Filters)
# Register your models here.

admin.site.register(PlantSettings)
admin.site.register(Enclosure)
admin.site.register(PeltierCell)
admin.site.register(VaporGenerator)
admin.site.register(WaterTank)
admin.site.register(ElectricalHeater)
admin.site.register(UvLight)
admin.site.register(CO2Valve)
admin.site.register(Filters)
