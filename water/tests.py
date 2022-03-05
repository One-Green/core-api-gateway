from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from random import randint

REGISTRY_URL = reverse("water-registry")
TAGS = [
    {"tag": "test1"},
    {"tag": "test2"},
    {"tag": "test3"},
    {"tag": "test4"},
    {"tag": "test5"},
]


class WaterTest(APITestCase):
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
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        for _ in TAGS:
            url = reverse("water-config", args=[_["tag"]])
            data = {
                "ph_min_level": randint(1, 100),
                "ph_max_level": randint(1, 100),
                "tds_min_level": randint(1, 100),
                "tds_max_level": randint(1, 100),
            }
            # Post configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            self.assertEqual(data["ph_min_level"], r.data["ph_min_level"])
            self.assertEqual(data["ph_max_level"], r.data["ph_max_level"])
            self.assertEqual(data["tds_min_level"], r.data["tds_min_level"])
            self.assertEqual(data["tds_max_level"], r.data["tds_max_level"])

    def test_force_controller(self):
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        for _ in TAGS:
            url = reverse("water-force", args=[_["tag"]])
            data = {
                "force_water_pump_signal": randint(0, 1),
                "force_nutrient_pump_signal": randint(0, 1),
                "force_ph_downer_pump_signal": randint(0, 1),
                "force_mixer_pump_signal": randint(0, 1),
                "water_pump_signal": randint(0, 1),
                "nutrient_pump_signal": randint(0, 1),
                "ph_downer_pump_signal": randint(0, 1),
                "mixer_pump_signal": randint(0, 1),
            }
            # Post force configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get force configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            self.assertEqual(
                data["force_water_pump_signal"], r.data["force_water_pump_signal"]
            )
            self.assertEqual(
                data["force_nutrient_pump_signal"], r.data["force_nutrient_pump_signal"]
            )
            self.assertEqual(
                data["force_ph_downer_pump_signal"], r.data["force_ph_downer_pump_signal"]
            )
            self.assertEqual(
                data["force_mixer_pump_signal"], r.data["force_mixer_pump_signal"]
            )
            self.assertEqual(data["water_pump_signal"], r.data["water_pump_signal"])
            self.assertEqual(data["nutrient_pump_signal"], r.data["nutrient_pump_signal"])
            self.assertEqual(data["ph_downer_pump_signal"], r.data["ph_downer_pump_signal"])
