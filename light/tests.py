"""
Light Api tests cases

"""

from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from light.models import (
    Device,
    DailyTimeRange,
    CalendarRange,
    Config,
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

        # create config type
        url = reverse("light:configtype-list")
        data = {"name": "daily"}
        config_type_id = self.client.post(url, data, format="json").json()["id"]

        # link them all into device config
        url = reverse("light:config-list")
        data = {
            "config_type": config_type_id,
            "daily_config": default_config_id,
            "tag": device_id,
            "planner_configs": [planner_config_id],
        }
        response = self.client.post(url, data, format="json")
        config_id = response.json()["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(Config.objects.get().id, config_id)
