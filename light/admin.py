from django.contrib import admin

from .models import (
    Device,
    Sensor,
    Controller,
    Config,
    ConfigType,
    ForceController,
    DailyTimeRange,
    CalendarRange,
)

admin.site.register(Device)
admin.site.register(Sensor)
admin.site.register(Config)
admin.site.register(ConfigType)
admin.site.register(Controller)
admin.site.register(ForceController)
admin.site.register(DailyTimeRange)
admin.site.register(CalendarRange)
