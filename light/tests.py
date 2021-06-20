from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime
from random import randint
import pytz

tz = pytz.timezone("Europe/Paris")

REGISTRY_URL = reverse("light-registry")
TAGS = [
    {'tag': 'test1'},
    {'tag': 'test2'},
    {'tag': 'test3'},
    {'tag': 'test4'},
    {'tag': 'test5'},
]


class LightTests(APITestCase):

    def __set_global_configuration(self):
        """
        Private method to set global configuration
        "data" need to be aligned with "glbl" apps
        :return:
        """
        url = reverse("global-config")
        data = {'timezone': 'Europe/Paris'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_registration(self):
        """
        Test new tag registration
        :return:
        """
        for i, _ in enumerate(TAGS):
            r = self.client.post(REGISTRY_URL, _, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            cnt = (len(self.client.get(REGISTRY_URL).data))
            self.assertEqual(cnt, i + 1)

    def test_configuration(self):
        """
        Test tag configuration
        :return:
        """
        self.__set_global_configuration()
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Configure sprinklers
        for _ in TAGS:
            url = reverse("light-config", args=[_["tag"]])
            data = {
                "on_datetime_at": tz.localize(datetime.utcnow()).isoformat(),
                "off_datetime_at": tz.localize(datetime.utcnow()).isoformat()
            }
            # Post configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Create and delete tags
        :return:
        """
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Delete Tag in registry
        for _ in TAGS:
            r = self.client.delete(REGISTRY_URL, _, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Count and assert if all Tags are removed
        cnt = (len(self.client.get(REGISTRY_URL).data))
        self.assertEqual(cnt, 0)

    def test_force_controller(self):
        """
        Test override controller action
        :return:
        """
        # Create Tag in registry
        for _ in TAGS:
            r = self.client.post(REGISTRY_URL, _, format='json')
            self.assertEqual(r.status_code, status.HTTP_200_OK)

        for _ in TAGS:
            url = reverse("light-force", args=[_["tag"]])
            data = {
                "force_light_signal": randint(0, 1),
                "light_signal": randint(0, 1)
            }
            # Post configuration
            r = self.client.post(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            # Get configuration
            r = self.client.get(url, data, format="json")
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertEqual(data["force_light_signal"], r.data["force_light_signal"])
            self.assertEqual(data["light_signal"], r.data["light_signal"])
