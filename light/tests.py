"""
Light Api tests cases

from pprint import pprint
<run light.urls> and retrieve router urls
pprint(router.get_urls())
[<URLPattern '^device/$' [name='device-list']>,
 <URLPattern '^device\.(?P<format>[a-z0-9]+)/?$' [name='device-list']>,
 <URLPattern '^device/(?P<pk>[^/.]+)/$' [name='device-detail']>,
 <URLPattern '^device/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='device-detail']>,
 <URLPattern '^config/$' [name='config-list']>,
 <URLPattern '^config\.(?P<format>[a-z0-9]+)/?$' [name='config-list']>,
 <URLPattern '^config/(?P<pk>[^/.]+)/$' [name='config-detail']>,
 <URLPattern '^config/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='config-detail']>,
 <URLPattern '^config-daily/$' [name='dailytimerange-list']>,
 <URLPattern '^config-daily\.(?P<format>[a-z0-9]+)/?$' [name='dailytimerange-list']>,
 <URLPattern '^config-daily/(?P<pk>[^/.]+)/$' [name='dailytimerange-detail']>,
 <URLPattern '^config-daily/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='dailytimerange-detail']>,
 <URLPattern '^config-calendar/$' [name='calendarrange-list']>,
 <URLPattern '^config-calendar\.(?P<format>[a-z0-9]+)/?$' [name='calendarrange-list']>,
 <URLPattern '^config-calendar/(?P<pk>[^/.]+)/$' [name='calendarrange-detail']>,
 <URLPattern '^config-calendar/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='calendarrange-detail']>,
 <URLPattern '^controller/$' [name='controller-list']>,
 <URLPattern '^controller\.(?P<format>[a-z0-9]+)/?$' [name='controller-list']>,
 <URLPattern '^controller/(?P<pk>[^/.]+)/$' [name='controller-detail']>,
 <URLPattern '^controller/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='controller-detail']>,
 <URLPattern '^controller-force/$' [name='forcecontroller-list']>,
 <URLPattern '^controller-force\.(?P<format>[a-z0-9]+)/?$' [name='forcecontroller-list']>,
 <URLPattern '^controller-force/(?P<pk>[^/.]+)/$' [name='forcecontroller-detail']>,
 <URLPattern '^controller-force/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='forcecontroller-detail']>,
 <URLPattern '^$' [name='api-root']>,
 <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>]
"""

from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from light.models import (
    Device,
    DailyTimeRange,
    CalendarRange,
    Config,
    Controller,
    ForceController,
)


class LightTests(APITestCase):
    def test_create_device(self):
        """
        Ensure we can create a new device
        """
        url = reverse("light:device-list")
        data = {"tag": "tag-test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(Device.objects.get().tag, "tag-test")

    def test_daily_time_range_config(self):
        url = reverse("light:dailytimerange-list")
        data = {
            "name": "test-daily-config",
            "on_at": "12:30",
            "off_at": "14:30",
            "on_monday": True,
            "on_tuesday": True,
            "on_wednesday": True,
            "on_thursday": True,
            "on_friday": True,
            "on_saturday": True,
            "on_sunday": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyTimeRange.objects.count(), 1)
        self.assertEqual(DailyTimeRange.objects.get().name, "test-daily-config")

    def test_calendar_config(self):
        url = reverse("light:calendarrange-list")
        data = {
            "name": "test-calendar-config",
            "start_date_at": "2022-03-15",
            "end_date_at": "2022-03-15",
            "on_time_at": "12:30",
            "off_time_at": "12:40",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CalendarRange.objects.count(), 1)
        self.assertEqual(CalendarRange.objects.get().name, "test-calendar-config")

    def test_link_device_config(self):
        """
        ensure device, default config, planner config can be created,
        then linked to device config
        """

        # create device
        url = reverse("light:device-list")
        data = {"tag": "tag-test"}
        device_id = self.client.post(url, data, format="json").json()["id"]

        # create daily config
        url = reverse("light:dailytimerange-list")
        data = {
            "name": "test-daily-config",
            "on_at": "12:30",
            "off_at": "14:30",
            "on_monday": True,
            "on_tuesday": True,
            "on_wednesday": True,
            "on_thursday": True,
            "on_friday": True,
            "on_saturday": True,
            "on_sunday": True,
        }
        default_config_id = self.client.post(url, data, format="json").json()["id"]

        # create calendar config
        url = reverse("light:calendarrange-list")
        data = {
            "name": "test-calendar-config",
            "start_date_at": "2022-03-15",
            "end_date_at": "2022-03-15",
            "on_time_at": "12:30",
            "off_time_at": "12:40",
        }
        planner_config_id = self.client.post(url, data, format="json").json()["id"]

        # link them all into device config
        url = reverse("light:config-list")
        data = {
            "use_default_config": True,
            "use_planner_config": False,
            "tag": device_id,
            "default_config": default_config_id,
            "planner_configs": [planner_config_id],
        }
        response = self.client.post(url, data, format="json")
        config_id = response.json()["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(Config.objects.get().id, config_id)
