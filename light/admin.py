from django.contrib import admin

from .models import (
    Device,
    Controller,
    Config,
    ForceController,
    DailyTimeRange,
    CalendarRange,
)

admin.site.register(Device)
admin.site.register(Config)
admin.site.register(Controller)
admin.site.register(ForceController)
admin.site.register(DailyTimeRange)
admin.site.register(CalendarRange)
