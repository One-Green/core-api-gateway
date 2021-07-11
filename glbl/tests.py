from rest_framework import status
from rest_framework.test import APITestCase
from glbl.models import Config
from django.urls import reverse


class GlobalConfigTest(APITestCase):
    def test_create_timezone(self):
        url = reverse("global-config")
        data = {"timezone": "Europe/Paris"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(Config.objects.get().timezone, "Europe/Paris")
