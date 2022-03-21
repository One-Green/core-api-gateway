from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from sprinkler.models import (
    Device,
    Config,
)


class SprinklerTests(APITestCase):
    def test_create_device(self):
        """
        Ensure we can create a new device
        """
        url = reverse("sprinkler:device-list")
        data = {"tag": "sprinkler-test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(Device.objects.get().tag, "sprinkler-test")

    def test_config(self):
        url = reverse("sprinkler:device-list")
        data = {"tag": "sprinkler-test"}
        tag_id = self.client.post(url, data, format="json").json()["id"]

        url = reverse("sprinkler:config-list")
        data = {
            "tag": tag_id,
            "soil_moisture_min_level": 10,
            "soil_moisture_max_level": 20,
            "water_tag_link": 1,
        }
        response = self.client.post(url, data, format="json").json()
        print(response)
