from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from random import randint

REGISTRY_URL = reverse("sprinkler-registry")
TAGS = [
    {"tag": "test1"},
    {"tag": "test2"},
    {"tag": "test3"},
    {"tag": "test4"},
    {"tag": "test5"},
]


class SprinklerTests(APITestCase):
    def test_tag_registration(self):
        """
        Test new tag registration
        :return:
        """
        for i, _ in enumerate(TAGS):
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            cnt = len(self.client.get(REGISTRY_URL).data)
            self.assertEqual(cnt, i + 1)

    def test_configuration(self):
        """
        Test tag configuration
        :return:
        """

        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Configure sprinklers
        for _ in TAGS:
            url = reverse("sprinkler-config", args=[_["tag"]])
            data = {
                "soil_moisture_min_level": randint(10, 30),
                "soil_moisture_max_level": randint(50, 100),
            }
            # Post configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertEqual(
                data["soil_moisture_min_level"], r.data["soil_moisture_min_level"]
            )
            self.assertEqual(
                data["soil_moisture_min_level"], r.data["soil_moisture_min_level"]
            )

    def test_delete(self):
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Delete Tag in registry
        for _ in TAGS:
            r = self.client.delete(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Count and assert if all Tags are removed
        cnt = len(self.client.get(REGISTRY_URL).data)
        self.assertEqual(cnt, 0)

    def test_force_controller(self):
        """
        Test override controller action
        :return:
        """
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        for _ in TAGS:
            url = reverse("sprinkler-force", args=[_["tag"]])
            data = {
                "force_water_valve_signal": randint(0, 1),
                "water_valve_signal": randint(0, 1),
            }
            # Post configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertEqual(
                data["force_water_valve_signal"], r.data["force_water_valve_signal"]
            )
            self.assertEqual(data["water_valve_signal"], r.data["water_valve_signal"])
