from django.contrib import admin

from .models import Device, Controller, Config, ForceController

admin.site.register(Device)
admin.site.register(Config)
admin.site.register(Controller)
admin.site.register(ForceController)
